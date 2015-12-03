from os import path
from time import sleep
from exceptions import Exception
import threading

from mixer import Mixer
import instruments


class Track():
    def __init__(self, instrument_id, instrument_tone, rhythm, gains, id):
        self.instrument_id = instrument_id
        self.instrument_tone = instrument_tone
        self.rhythms = rhythm
        self.gains = gains
        self.id = id
        self.mute = False


class GridSequencer(Mixer):
    INFINIT_LOOP = -1
    DEFAULT_SPEED = 60
    DEFAULT_MEASURE_RESOLUTION = 8
    DEFAULT_BEATS_PER_MEASURE = 4

    def __init__(self, score_path, buffer_size=512, sample_rate=44100):
        Mixer.__init__(self)

        self.sample_rate = sample_rate
        self.buffer_size = buffer_size

        self.speed = self.DEFAULT_SPEED
        self.measure_resolution = self.DEFAULT_MEASURE_RESOLUTION
        self.beats_per_measure = self.DEFAULT_BEATS_PER_MEASURE
        self.sleep_interval = None
        self._update_sleep_interval()

        self.running = False;
        self.loop = 0
        self._worker_thread = None

        self.instruments = []
        self.instrument_id_counter = 0
        self.tracks = []

        # Load score file
        data = open(score_path, 'r').read()
        self._parse(data)

    def add_instrument(self, instrument, id=None):
        if id is None:
            id = len(self.instruments)
            self.instruments.append(instrument)
            self.add_device(instrument)
        return id

    def add_track(self, track):
        self.tracks.append(track)
        self.tracks.sort(lambda i, j: i.instrument_id - j.instrument_id)

    def set_speed(self, speed):
        self.speed = speed
        self._update_sleep_interval()

    def _update_sleep_interval(self):
        if self.measure_resolution % self.beats_per_measure == 0:
            self.sleep_interval = 60. / (self.speed * self.measure_resolution / self.beats_per_measure)
        else:
            raise Exception('This measure resolution has to be divisible with beeats_per_measure')

    def _sleep(self):
        sleep(self.sleep_interval)

    def _worker(self):
        i = 0
        while self.running:

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

            self._sleep()

            i += 1
            i %= self.measure_resolution
            if not i:
                if not self.loop:
                    self.running = False
                    break
                else:
                    self.loop -= 1

    def play(self, loop=INFINIT_LOOP):
        # print("Sequencer: Play")
        if self._worker_thread is None:
            self.running = True
            self.loop = loop
            self._worker_thread = threading.Thread(target=self._worker)
            self._worker_thread.start()

    def stop(self):
        # print("Sequencer: Stop")
        if self.running:
            self.running = False
            self.loop = 0
            self._worker_thread.join()
            self._worker_thread = None
            [i.off() for i in self.instruments]

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
        self._update_sleep_interval()


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

                track = Track(instrument_id, instrument_tone, rhythm, rhythm, '')
                self.add_track(track)

            line = lines.pop(0)

    def save(self, score_path):
        print "Saving to %s" % score_path

        folder, file = path.split(score_path)

        file = open(path.join(folder, file), 'w')

        file.write('parameters\n')
        file.write('speed %i\n' % self.speed)
        file.write('measure_resolution %i\n' % self.measure_resolution)
        file.write('beats_per_measure %i\n' % self.beats_per_measure)
        file.write('samplerate %i\n' % self.sample_rate)
        file.write('buffersize %i\n' % self.buffer_size)

        file.write('\ninstruments\n')
        for id, instrument in enumerate(self.instruments):
            file.write(str(instrument))
            file.write("\n")

        file.write('\nrhythm\n')
        for id, track in enumerate(self.tracks):
            file.write("%i %i: " %
                       (track.instrument_id,
                        track.instrument_tone)
                       )
            file.write("  ".join(map(str,track.rhythms)))
            file.write("\n")

        file.flush()
        file.close()
