#!/usr/bin/python

import sys
from time import sleep

import numpy as np

from dac import DAC
from mixer import Mixer

import parser

DEFAULT_BEAT_INTERVAL = 0.2
BUFFER_SIZE = 2 ** 10

if __name__ == "__main__":

    (speed, length, subdivision, samplerate, buffersize, instruments, rhythms, gains) = parser.parse(sys.argv[1])

    dac = DAC(buffersize)

    mixer = Mixer()
    mixer.setVolume(0)

    dac.connect(mixer.callback)
    dac.start()

    mixer.setVolume(.8)

    for instrument in instruments:
        mixer.addDevice(instrument)

    # instrument = Sampler('./instruments/samples/un_TC-03-G1-05.wav')
    # mixer.addDevice(instrument)
    #
    # for i in range(1, len(frequencies)):
    #     f = frequencies[i]
    #     instrument = SineSynth(dac.getSamplerate(), dac.getBufferSize())
    #     instrument.setFreq(f)
    #     instrument.start()
    #     mixer.addDevice(instrument)

    i = 0
    while True:

        oscilator_index = 0
        for j in range(0, len(mixer.channels)):
            gain = gains[j]
            rythm = rhythms[j]
            channel = mixer.channels[j]
            channel.gain = gain[i]
            if rythm[i]:
                channel.device.trigger(.1)
                # channel.mute = False
                # else:
                # channel.mute = True

        sleep(DEFAULT_BEAT_INTERVAL)

        i += 1
        i %= 8
