#!/usr/bin/python

from Tkinter import *


class RhythmButton(Button):
    def __init__(self, master, sequencer, i, b):
        Button.__init__(self, master, text="%i:%i" % (i, b), command=self.command)
        self.sequencer = sequencer
        self.instrument = i
        self.beat = b
        self.update_visual()

    def command(self):
        instrument = self.instrument
        beat = self.beat
        self.sequencer.rhythms[instrument][beat] = not self.sequencer.rhythms[instrument][beat];
        self.update_visual()

    def update_visual(self):
        if self.sequencer.rhythms[self.instrument][self.beat]:
            self.config(text="x")
        else:
            self.config(text=" ")


class RhythmFrame(Frame):
    def __init__(self, master, sequencer):
        Frame.__init__(self, master)

        self.sequencer = sequencer
        self.buttons = []
        rhythm = sequencer.rhythms[0]

        for i in range(0, len(sequencer.rhythms)):
            for b in range(0, len(rhythm)):
                button = RhythmButton(self, sequencer, i, b)
                self.buttons.append(button)
                button.grid(row=i, column=b)

    def set_rhythm(self, instrument, beat):
        # self.sequencer.rhythms[instrument][beat] = not self.sequencer.rhythms[instrument][beat]
        self.sequencer.rhythms[instrument][beat] = 4
        print("instrumnet: %i, beat: %i" % (instrument, beat))
        for b in self.sequencer.rhythms[instrument]:
            sys.stdout.write(str(b))
        sys.stdout.write('\n')


class MainWindow():
    def __init__(self, master, sequencer):
        self.sequencer = sequencer
        self.master = master
        self.control_panel = Frame(master)
        self.start_button = Button(self.control_panel, text="Start")
        self.stop_button = Button(self.control_panel, text="Stop")
        self.quit_button = Button(self.control_panel, text="Quit")
        self.start_button.config(command=self.sequencer.play)
        self.stop_button.config(command=self.sequencer.stop)
        self.quit_button.config(command=self._quit)
        self.start_button.pack()
        self.stop_button.pack()
        self.quit_button.pack()
        self.control_panel.grid(row=0, column=0)
        self.rhythm_frame = RhythmFrame(master, sequencer)
        self.rhythm_frame.grid(row=0, column=1)

    def _quit(self):
        print("MainWindow: _quit")
        self.master.destroy()
        self.master.quit()
