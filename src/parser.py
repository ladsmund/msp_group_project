__author__ = 'mads'

from instruments.sampler import SingleSoundSampler
from instruments.sinesynth import SineSynth


# example = "parameters\nspeed 150\nsamplerate 44100\nbuffersize 1024\ninstruments\nSampler ./instruments/samples/un_TC-03-G1-05.wav\nSineSynth 423\nrhythm\n1 1 1 1\n0 1 1 0\n\ngains\n.1 .2 .5 . 6\n.1 .1 .1 .1"

def parse(file_path):
    file = open(file_path, 'r')
    data = file.read()
    file.close()

    lines = data.split("\n")

    line = lines.pop(0)
    while line != 'parameters':
        print "not parameter " + line_array
        line = lines.pop(0)

    # Reading parameters
    speed = None
    length = None
    subdivision = None
    samplerate = None
    buffersize = None
    while len(lines) > 0 and line != 'instruments':
        if len(line) > 0 and line[0] != '#':
            line_array = line.split(' ')
            if line_array[0] == 'speed':
                speed = int(line_array[1])
            elif line_array[0] == 'length':
                length = int(line_array[1])
            elif line_array[0] == 'subdivision':
                subdivision = int(line_array[1])
            elif line_array[0] == 'samplerate':
                samplerate = int(line_array[1])
            elif line_array[0] == 'buffersize':
                buffersize = int(line_array[1])
        line = lines.pop(0)

    # Reading instrumnets
    instruments = []
    line = lines.pop(0)
    while len(lines) > 0 and line != 'rhythm':
        if len(line) > 0 and line[0] != '#':
            line_array = line.split(' ')
            if line_array[0] == 'Sampler':
                instruments.append(SingleSoundSampler(line_array[1]))
            elif line_array[0] == 'SineSynth':
                instrument = SineSynth(samplerate, buffersize)
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

    return (speed, length, subdivision, samplerate, buffersize, instruments, rhythms, gains)
