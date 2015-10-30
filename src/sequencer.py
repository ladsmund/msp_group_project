from mixer import Mixer
from time import sleep
from exceptions import Exception

from instruments.sampler import Sampler
from instruments.sinesynth import SineSynth


class Sequencer(Mixer):
    def __init__(self):
        Mixer.__init__(self)
        self.instruments = []
        self.rhythms = []
        self.gains = []
        self.speed = None
        self.measure_resolution = None
        self.beats_per_measure = None
        self.samplerate = 44100
        self.buffersize = 128
        self.sleep_interval = None

    def play(self):
        i = 0
        # while True:
        for _ in range(64):
            print "Beat"

            oscilator_index = 0
            for j in range(0, len(self.channels)):
                gain = self.gains[j]
                rhythm = self.rhythms[j]
                channel = self.channels[j]
                channel.gain = gain[i]

                print "%3i, %i: trigger: %i, gain: %0.2f" % (i, j, rhythm[i], gain[i])
                if rhythm[i]:
                    channel.device.trigger(.05)

            sleep(self.sleep_interval)

            i += 1
            i %= self.measure_resolution

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
                elif line_array[0] == 'samplerate':
                    self.samplerate = int(line_array[1])
                elif line_array[0] == 'buffersize':
                    self.buffersize = int(line_array[1])
            line = lines.pop(0)

        if self.measure_resolution % self.beats_per_measure == 0:
            self.sleep_interval = 60. / (self.speed * self.measure_resolution / self.beats_per_measure)
        else:
            raise Exception('This measure resolution has to be divisible with beeats_per_measure')


        # Reading instrumnets
        line = lines.pop(0)
        while len(lines) > 0 and line != 'rhythm':
            if len(line) > 0 and line[0] != '#':
                line_array = line.split(' ')
                if line_array[0] == 'Sampler':
                    instrument = Sampler(line_array[1])
                    self.instruments.append(instrument)
                    self.addDevice(instrument)
                elif line_array[0] == 'SineSynth':
                    instrument = SineSynth(samplerate, buffersize)
                    instrument.setFreq(int(line_array[1]))
                    self.instruments.append(instrument)
                    self.addDevice(instrument)

            line = lines.pop(0)



        # Reading Rhythm pattern
        line = lines.pop(0)
        while len(lines) > 0 and line != 'gains':
            if len(line) > 0 and line[0] != '#':
                line_array = line.split(' ')
                self.rhythms.append([int(c) for c in line_array])

            line = lines.pop(0)

        # Reading gain pattern
        line = lines.pop(0)
        while len(lines) > 0:
            if len(line) > 0 and line[0] != '#':
                line_array = line.split(' ')
                self.gains.append([float(c) for c in line_array])
            line = lines.pop(0)