#!/usr/bin/python

import sys

from sequencer import Sequencer
from time import sleep

if __name__ == "__main__":

    with Sequencer() as sequencer:
        sequencer.load(sys.argv[1])
        sequencer.play(False)

        while (sequencer.running):
            sleep(0.1)
        print("Exit")

    exit()
