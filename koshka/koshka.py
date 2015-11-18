#!/usr/bin/python

import argparse
from time import sleep

from sequencers.grid_sequencer import GridSequencer

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Kosha - MSP project')

    parser.add_argument('score', type=str)
    parser.add_argument('--no_gui', type=bool, default=False, const=True, nargs='?')
    parser.add_argument('-l','--loop', type=int, default=0, const=GridSequencer.INFINIT_LOOP, nargs='?')
    namespace = parser.parse_args()

    print namespace
    with GridSequencer() as sequencer:
        sequencer.load(namespace.score)

        if namespace.no_gui:
            sequencer.play(namespace.loop)
            while (sequencer.running):
                sleep(0.1)
        else:
            from gui.main_window import MainWindow

            window = MainWindow(sequencer)
            window.mainloop()
            window = None

    exit()
