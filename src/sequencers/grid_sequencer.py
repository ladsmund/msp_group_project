from src.mixer import Mixer
from time import sleep
from exceptions import Exception
import threading

from src.dac import DAC

from src.instruments.sampler import SingleSoundSampler
from src.instruments.sinesynth import SineSynth
from src.instruments.scalesynth import ScaleSynth
from src.instruments.perfect_triads import PerfectTriads
from src import instruments
from src.scales.pythag_series import PythagSeriesDodecaphpnic, PythagSeriesSevenNoteScale
from src.scales.even_tempered import EvenTempered


class Track():
    def __init__(self, instrument_id, instrument_tone, rhythm, gains, id):
        self.instrument_id = instrument_id
        self.instrument_tone = instrument_tone
        self.rhythms = rhythm
        self.gains = gains
        self.id = id
        self.mute = False


class GridSequencer(Mixer):
    def __init__(self, buffer_size=512, sample_rate=44100):
        Mixer.__init__(self)
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size

        self.speed = None
        self.measure_resolution = None
        self.beats_per_measure = None
        self.sleep_interval = None

        self.running = False;
        self.loop = False
        self._worker_thread = None

        self.instruments = []
        self.instrument_id_counter = 0
        self.tracks = []

        self.dac = DAC(self.buffer_size, self.sample_rate)
        self.dac.connect(self.callback)
        self.dac.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.dac.stop()

    def __enter__(self):
        return self

    def add_instrument(self, instrument, id=None):
        if id is None:
            id = len(self.instruments)
            self.instruments.append(instrument)
            self.add_device(instrument)
        return id

    def add_track(self, track):
        self.tracks.append(track)
        self.tracks.sort(lambda _, t: t.instrument_id)

    def _worker(self):
        i = 0
        while self.running:
            # print "Beat"

            oscilator_index = 0
            for track in self.tracks:

                gain = track.gains
                rhythm = track.rhythms
                tone = track.instrument_tone
                instrument = self.instruments[track.instrument_id]

                if not track.mute and rhythm[i] != 0:
                    instrument.on(tone)
                    # track.instrument.on(rhythm[i])
                else:
                    # track.instrument.off()
                    instrument.off(tone)

            sleep(self.sleep_interval)

            i += 1
            i %= self.measure_resolution
            if not self.loop and not i:
                self.running = False
                break

    def play(self, loop=True):
        print("Sequencer: Play")
        if self._worker_thread is None:
            self.running = True
            self.loop = loop
            self._worker_thread = threading.Thread(target=self._worker)
            self._worker_thread.start()

    def stop(self):
        print("Sequencer: Stop")
        if self.running:
            self.running = False
            self.loop = False
            self._worker_thread.join()
            self._worker_thread = None
            [i.off() for i in self.instruments]

    def load(self, file_name):
        file = open(file_name, 'r')
        data = file.read()
        file.close()
        self._parse(data)
        pass

    def _parse(self, data):
        lines = data.split("\n")

        line = lines.pop(0)
        while line != 'parameters':
            print "not parameter " + line
            line = lines.pop(0)

        # Reading parameters
        while len(lines) > 0 and line != 'instruments':
            if len(line) > 0 and line[0] != '#':
                line_array = line.split(' ')
                if line_array[0] == 'speed':
                    self.speed = int(line_array[1])
                elif line_array[0] == 'measure_resolution':
                    self.measure_resolution = int(line_array[1])
                elif line_array[0] == 'beats_per_measure':
                    self.beats_per_measure = int(line_array[1])
            line = lines.pop(0)

        if self.measure_resolution % self.beats_per_measure == 0:
            self.sleep_interval = 60. / (self.speed * self.measure_resolution / self.beats_per_measure)
        else:
            raise Exception('This measure resolution has to be divisible with beeats_per_measure')

        # Reading instruments
        line = lines.pop(0)
        while len(lines) > 0 and line != 'rhythm':
            if len(line) > 0 and line[0] != '#':
                self.add_instrument(instruments.parse(line.split(' '), self.sample_rate, self.buffer_size))
            line = lines.pop(0)

        # Reading Rhythm pattern
        line = lines.pop(0)
        while len(lines) > 0 and line != 'gains':
            if len(line) > 0 and line[0] != '#':
                line = line.split('|')[-1]

                instr_str = line.split(':')[0].split()
                instrument_id = int(instr_str[0])
                instrument_tone = int(instr_str[1])

                rhythm = line.split(':')[1].split()[0:self.measure_resolution]
                rhythm = [int(c) for c in rhythm]

                track = Track(instrument_id, instrument_tone, rhythm, rhythm, 'name')
                self.add_track(track)

            line = lines.pop(0)
