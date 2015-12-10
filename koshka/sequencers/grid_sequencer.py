from os import path
from time import sleep
from exceptions import Exception
import threading

from mixer import Mixer
import instruments


class TimeEvent:
    def __init__(self, time):
        self.time = time


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
    DEFAULT_STRESS_GAIN = 1.
    DEFAULT_NON_STRESS_GAIN = .7

    def __init__(self, score_path, buffer_size=512, sample_rate=44100):
        Mixer.__init__(self)

        self.sample_rate = sample_rate
        self.buffer_size = buffer_size

        self.speed = self.DEFAULT_SPEED
        self.measure_resolution = self.DEFAULT_MEASURE_RESOLUTION
        self.beats_per_measure = self.DEFAULT_BEATS_PER_MEASURE
        self._update_sleep_interval()

        self.stress_gain = self.DEFAULT_STRESS_GAIN
        self.non_stress_gain = self.DEFAULT_NON_STRESS_GAIN
        self.current_gain = 1.

        self.running = False
        self.loop = 0
        self.sleep_interval = None
        self.total_frame_count = 0
        self.sleep_frames = 0

        self.instruments = []
        self.instrument_id_counter = 0
        self.tracks = []

        # Load score file
        data = open(score_path, 'r').read()
        self._parse(data)

        self.observers = set()

    def add_observer(self, observer):
        self.observers.add(observer)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def remove_all_observers(self):
        self.observers = set()

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

    def notify_observers(self, event):
        for observer in self.observers:
            observer.notify(event)

    def change_measures(self, beats_per_measure, measure_resolution):
        print "grid sequencer: change_measures"
        self.stop()
        if measure_resolution % beats_per_measure == 0:
            self.beats_per_measure = beats_per_measure
            self.measure_resolution = measure_resolution
            for t in self.tracks:
                if len(t.rhythms) < self.measure_resolution:
                    t.rhythms.extend([0] * (self.measure_resolution - len(t.rhythms)))
                else:
                    t.rhythms = t.rhythms[0:self.measure_resolution]
            self._update_sleep_interval()
        else:
            raise Exception('This measure resolution has to be divisible with beeats_per_measure')

    def _update_sleep_interval(self):
        if self.measure_resolution % self.beats_per_measure == 0:
            sleep_time = 60. / (self.speed * self.measure_resolution / self.beats_per_measure)
            # print sleep_time
            self.sleep_interval = self.sample_rate * sleep_time
        else:
            raise Exception('This measure resolution has to be divisible with beeats_per_measure')

    def update(self, frame_count):
        self.total_frame_count += frame_count
        self.sleep_frames -= frame_count
        if self.sleep_frames <= 0:
            i = int(self.total_frame_count // self.sleep_interval)
            i %= self.measure_resolution

            # self.notify_observers(TimeEvent(i))

            offset = -self.sleep_frames

            is_stressed = not i % (self.measure_resolution / self.beats_per_measure)
            self.current_gain = self.stress_gain if is_stressed else self.non_stress_gain

            for track in self.tracks:

                gain = track.gains
                rhythm = track.rhythms
                tone = track.instrument_tone
                instrument = self.instruments[track.instrument_id]

                if not track.mute and rhythm[i] != 0:
                    instrument.on(tone, time=offset)
                    # track.instrument.on(rhythm[i])
                else:
                    # track.instrument.off()
                    instrument.off(tone, time=offset)

            self.sleep_frames += self.sleep_interval

        pass

    def callback(self, in_data, frame_count, time_info, status):
        # time = time_info['output_buffer_dac_time']
        if self.running:
            self.update(frame_count)
        res = Mixer.callback(self, in_data, frame_count, time_info, status)
        if res is None:
            return res
        else:
            return res * self.current_gain

    def play(self, loop=INFINIT_LOOP):
        self.total_frame_count = 0
        self.sleep_frames = 0
        self.running = True

    def stop(self):
        self.running = False
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
                instrument = instruments.parse(line.split(' '), self.sample_rate, self.buffer_size)
                self.add_instrument(instrument)
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
            file.write("%2i %3i: " %
                       (track.instrument_id,
                        track.instrument_tone)
                       )
            file.write("  ".join(map(str, track.rhythms)))
            file.write("\n")

        file.flush()
        file.close()
