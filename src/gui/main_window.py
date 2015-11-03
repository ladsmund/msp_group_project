#!/usr/bin/python

from Tkinter import *


class MainWindow():
    def __init__(self, master, sequencer):
        self.sequencer = sequencer
        self.master = master
        self.start_button = Button(master, text="Start")
        self.stop_button = Button(master, text="Stop")
        self.quit_button = Button(master, text="Quit")
        self.start_button.config(command=self.sequencer.play)
        self.stop_button.config(command=self.sequencer.stop)
        self.quit_button.config(command=self._quit)
        self.start_button.pack()
        self.stop_button.pack()
        self.quit_button.pack()

    def _quit(self):
        print("MainWindow: _quit")
        self.master.destroy()
        self.master.quit()
