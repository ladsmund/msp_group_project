#!/usr/bin/python

from time import sleep

import numpy as np

from dac import DAC
from mixer import Mixer
from src.instruments.sinesynth import SineSynth
from src.instruments.sampler import Sampler

DEFAULT_BEAT_INTERVAL = 0.2
BUFFER_SIZE = 2 ** 10

if __name__ == "__main__":

    oscilator_list = []
    frequencies = [2000, 300, 400, 410, 880, 1000]

    rythms = []
    rythms.append([1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0])
    rythms.append([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
    rythms.append([0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
    rythms.append([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
    rythms.append([1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1])
    rythms.append([0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1])

    gains = []
    gains.append([.1, .1, .1, .1, .1, .1, .1, .1, .1, .1, .1, .1])
    # gains.append([1, .0, .1, .5, .0, .1, .5, .0, .1, .5, .0, .1])
    gains.append([1, .0, .1, .5, .0, .1, .5, .0, .1, .5, .0, .1])
    gains.append([1, .0, .1, .5, .0, .1, .5, .0, .1, .5, .0, .1])
    gains.append([1, .0, .1, .5, .0, .1, .5, .0, .1, .5, .0, .1])
    gains.append(0 * np.arange(0, 12) / 12.)
    gains.append(0 * np.arange(0, 12) / 12.)

    dac = DAC(BUFFER_SIZE)

    mixer = Mixer()
    mixer.setVolume(0)

    dac.connect(mixer.callback)
    dac.start()

    mixer.setVolume(.8)

    instrument = Sampler('./instruments/samples/un_TC-03-G1-05.wav')
    mixer.addDevice(instrument)

    for i in range(1, len(frequencies)):
        f = frequencies[i]
        instrument = SineSynth(dac.getSamplerate(), dac.getBufferSize())
        instrument.setFreq(f)
        instrument.start()
        mixer.addDevice(instrument)

    i = 0
    while True:

        oscilator_index = 0
        for j in range(0, len(mixer.channels)):
            gain = gains[j]
            rythm = rythms[j]
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
