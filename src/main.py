#!/usr/bin/python

from time import sleep
from dac import DAC
from mixer import Mixer
from oscilator import Oscilator
import numpy as np
from fractions import Fraction
from instrument import Instrument

DEFAULT_BEAT_INTERVAL = 0.2
BUFFER_SIZE = 2 ** 10

if __name__ == "__main__":

    oscilator_list = []
    frequencies = [2000, 300, 400, 410, 880, 1000]

    rythms = []
    rythms.append([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    rythms.append([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
    rythms.append([0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
    rythms.append([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
    rythms.append([1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1])
    rythms.append([0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1])

    gains = []
    gains.append([1, .0, .1, .5, .0, .1, .5, .0, .1, .5, .0, .1])
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

    for i in range(0, len(frequencies)):
        f = frequencies[i]
        instrument = Instrument(dac.getSamplerate(), dac.getBufferSize())
        instrument.setFreq(f)
        instrument.start()
        mixer.addDevice(instrument)
        oscilator_list.append(instrument)

    print len(oscilator_list)

    i = 0
    while True:

        oscilator_index = 0
        for j in range(0, len(oscilator_list)):
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
