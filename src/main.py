#!/usr/bin/python

import sys

from src.sequencers.grid_sequencer import GridSequencer
from gui.main_window import MainWindow

if __name__ == "__main__":
    with GridSequencer() as sequencer:

        print sys.argv

        sequencer.load(sys.argv[1])



        window = MainWindow(sequencer)
        window.mainloop()
        window = None

        print("Exit")

    exit()
