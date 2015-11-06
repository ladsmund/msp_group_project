from mixer import Mixer
from time import sleep
from exceptions import Exception
import threading

from dac import DAC

from instruments.sampler import Sampler
from instruments.sinesynth import SineSynth


class Sequencer(Mixer):
    def __init__(self, buffersize=128, samplerate=44100):
        print("Sequencer: __init__")
        Mixer.__init__(self)
        self.samplerate = samplerate
        self.buffersize = buffersize

        self.tracks = []
        self.speed = None
        self.measure_resolution = None
        self.beats_per_measure = None
        self.sleep_interval = None
        self.running = False;
        self._worker_thread = None

        self.dac = DAC(self.buffersize, self.samplerate)
        self.dac.connect(self.callback)
        self.dac.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.dac.stop()

    def __enter__(self):
        return self

    def _worker(self):
        i = 0
        while self.running:
            # print "Beat"

            oscilator_index = 0
            for track in self.tracks:


                gain = track.gains
                rhythm = track.rhythms
                # channel = self.channels[j]
                # channel.gain = gain[i]

                # print "%3i, %i: trigger: %i, gain: %0.2f" % (i, j, rhythm[i], gain[i])
                if rhythm[i] != 0:
                    track.instrument.trigger(rhythm[i], .05)

            sleep(self.sleep_interval)

            i += 1
            i %= self.measure_resolution

    def play(self):
        print("Sequencer: Play")
        if self._worker_thread is None:
            self.running = True
            self._worker_thread = threading.Thread(target=self._worker)
            self._worker_thread.start()

    def stop(self):
        print("Sequencer: Stop")
        if self.running:
            self.running = False
            self._worker_thread.join()
            self._worker_thread = None

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


        # Reading instrumnets
        instruments = []
        line = lines.pop(0)
        while len(lines) > 0 and line != 'rhythm':
            if len(line) > 0 and line[0] != '#':
                line_array = line.split(' ')
                if line_array[0] == 'Sampler':
                    instrument = Sampler(line_array[1])
                    instruments.append(instrument)
                elif line_array[0] == 'SineSynth':
                    instrument = SineSynth(self.samplerate, self.buffersize)
                    instrument.setFreq(int(line_array[1]))
                    instruments.append(instrument)

            line = lines.pop(0)



        # Reading Rhythm pattern
        rhythms = []
        line = lines.pop(0)
        while len(lines) > 0 and line != 'gains':
            if len(line) > 0 and line[0] != '#':
                line_array = line.split(' ')
                rhythms.append([int(c) for c in line_array])

            line = lines.pop(0)

        # Reading gain pattern
        gains = []
        line = lines.pop(0)
        while len(lines) > 0:
            if len(line) > 0 and line[0] != '#':
                line_array = line.split(' ')
                gains.append([float(c) for c in line_array])
            line = lines.pop(0)

        for i in range(0, len(instruments)):
            track = Track(instruments[i], rhythms[i], gains[i])
            self.add_track(track)

    def add_track(self, track):
        self.tracks.append(track)
        self.add_device(track.instrument)


class Track():
    def __init__(self, instrument, rhythms, gains):
        self.instrument = instrument
        self.rhythms = rhythms
        self.gains = gains
