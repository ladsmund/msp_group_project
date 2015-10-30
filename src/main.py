#!/usr/bin/python

import sys
from time import sleep

from dac import DAC
from mixer import Mixer
from instruments import SineSynth
from instruments import Sampler

import parser

if __name__ == "__main__":

    (speed, length, subdivision, samplerate, buffersize, instruments, rhythms, gains) = parser.parse(sys.argv[1])

    beat_interval = 60. / (speed * subdivision)
    dac = DAC(buffersize)

    mixer = Mixer()
    mixer.setVolume(1.)

    dac.connect(mixer.callback)
    dac.start()


    for instrument in instruments:
        channel = mixer.addDevice(instrument)
        # print instrument

    i = 0
    # while True:
    for j in range(64):
        print "Beat"

        oscilator_index = 0
        for j in range(0, len(mixer.channels)):
            gain = gains[j]
            rhythm = rhythms[j]
            channel = mixer.channels[j]
            channel.gain = gain[i]

            print "%3i, %i: trigger: %i, gain: %0.2f" % (i,j,rhythm[i],gain[i])
            if rhythm[i]:
                channel.device.trigger(.05)

        sleep(beat_interval)

        i += 1
        i %= length

    dac.stop()
    exit()
