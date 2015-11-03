#!/usr/bin/python

import sys

from dac import DAC

from sequencer import Sequencer

from gui.main_window import MainWindow
from Tkinter import Tk

if __name__ == "__main__":

    with Sequencer() as sequencer:
        sequencer.load(sys.argv[1])

        root = Tk()
        window = MainWindow(root, sequencer)
        root.mainloop()

        window = None
        print("Exit")

    exit()
