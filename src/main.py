#!/usr/bin/python

import sys

from dac import DAC

from sequencer import Sequencer

from gui.main_window import MainWindow
from Tkinter import Tk

if __name__ == "__main__":

    with Sequencer() as sequencer:
        sequencer.load(sys.argv[1])

        window = MainWindow(sequencer)
        window.mainloop()
        window = None

        print("Exit")

    exit()
