#!/usr/bin/python

import sys
from time import sleep

from koshka.sequencers.sequencer import Sequencer

if __name__ == "__main__":

    with Sequencer() as sequencer:
        sequencer.load(sys.argv[1])
        sequencer.play(False)

        while (sequencer.running):
            sleep(0.1)
        print("Exit")

    exit()
