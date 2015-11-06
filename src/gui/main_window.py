#!/usr/bin/python

from Tkinter import Tk, Button, Frame, Label
# from ttk import Button, Frame, Label

_RHYTHM_BUTTON_WIDTH = 4

class RhythmButton(Button):
    def __init__(self, master, track, beat):
        Button.__init__(self, master, text="--", command=self.command, width=_RHYTHM_BUTTON_WIDTH)
        self.track = track
        self.beat = beat
        self.toggle_visual()

    def command(self):
        self.track.rhythms[self.beat] = not self.track.rhythms[self.beat];
        self.toggle_visual()

    def toggle_visual(self):
        if self.track.rhythms[self.beat]:
            self.config(text=str(self.track.rhythms[self.beat]))
        else:
            self.config(text=" ")


class RhythmTrackFrame(Frame):
    def __init__(self, master, track):
        Frame.__init__(self, master)
        self.track = track

        instrument_frame = Frame(self)
        instrument_frame.grid(row=0, column=1)

        id_label = Label(instrument_frame, text=str(track.id))
        id_label.grid(row=0, column=0)

        Button(instrument_frame, text="load wav file").grid(row=1, column=0)


        rhythm_frame = Frame(self)
        rhythm_frame.grid(row=0, column=2)

        for b in range(0, len(self.track.rhythms)):
            button = RhythmButton(rhythm_frame, track, b)
            # self.buttons.append(button)
            button.grid(row=0, column=b)


class SequencerFrame(Frame):
    def __init__(self, master, sequencer):
        Frame.__init__(self, master)
        self.sequencer = sequencer

        row = 0;
        for track in sequencer.tracks:
            RhythmTrackFrame(self, track).grid(row=row, column=0)
            row += 1


class MainWindow(Tk):
    def __init__(self, sequencer):
        Tk.__init__(self)
        self.sequencer = sequencer

        self.control_panel = Frame(self)
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

        self.sequencer_frame = SequencerFrame(self, sequencer)
        self.sequencer_frame.grid(row=0, column=1)

    def _quit(self):
        self.destroy()
        self.quit()
