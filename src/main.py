#!/usr/bin/python

import sys

from dac import DAC

from sequencer import Sequencer

if __name__ == "__main__":

    sequencer = Sequencer()
    sequencer.load(sys.argv[1])

    dac = DAC(sequencer.buffersize)

    dac.connect(sequencer.callback)
    dac.start()

    sequencer.play()

    dac.stop()
    exit()
