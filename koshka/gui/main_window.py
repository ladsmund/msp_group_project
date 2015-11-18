#!/usr/bin/python

from Tkinter import Tk, Button, Frame, Label, IntVar, RIDGE, CENTER
from ttk import Button, Frame, Label, Style, Checkbutton
from instrument_frame import get_instrument_frame

_RHYTHM_BUTTON_WIDTH = 1
_FILE_BUTTON_WIDTH = 3


class RhythmButton(Button):
    def __init__(self, master, track, beat):
        Button.__init__(self, master, text="--", command=self.command, width=_RHYTHM_BUTTON_WIDTH)
        self.track = track
        self.beat = beat
        self.toggle_visual()

    def command(self):
        if self.track.rhythms[self.beat]:
            self.track.rhythms[self.beat] = 0
        else:
            self.track.rhythms[self.beat] = 1
        # self.track.rhythms[self.beat] = not self.track.rhythms[self.beat];
        self.toggle_visual()

    def toggle_visual(self):
        if self.track.rhythms[self.beat]:
            self.config(text="X")
        else:
            self.config(text=" ")


class TrackFrame(Frame):
    def __init__(self, master, track):
        Frame.__init__(self, master)
        self.track = track

        self.style_class = Style()
        self.style_class.configure('Track.TFrame',
                                   background='black',
                                   borderwidth=2,
                                   # relief='raised',
                                   )

        self.config(style='Track.TFrame')


def check_cmd(track, mute_var):
    track.mute = mute_var.get()


class RhythmTrackFrame(TrackFrame):
    def __init__(self, master, track):
        TrackFrame.__init__(self, master, track)

        self.id_label = Label(self, text=str(track.id))
        self.id_label.pack(side='left')

        # self.instrument_label = Label(self, text=str(track.instrument_id))
        # self.instrument_label.pack(side='left')

        self.instrument_label = Label(self, text=str(track.instrument_tone), width=3)
        self.instrument_label.pack(side='left')

        mute_var = IntVar()

        self.mute_toggle = Checkbutton(self, command=lambda: check_cmd(track, mute_var), variable=mute_var)
        self.mute_toggle.pack(side='left')

        mute_var.set(track.mute)

        rhythm_frame = Frame(self)
        rhythm_frame.pack(side='right')

        for b in range(0, len(self.track.rhythms)):
            button = RhythmButton(rhythm_frame, track, b)
            # self.buttons.append(button)
            button.grid(row=0, column=b)


class SequencerFrame(Frame):
    def __init__(self, master, sequencer):
        Frame.__init__(self, master)
        self.sequencer = sequencer

        row = 0
        for id, instrument in enumerate(sequencer.instruments):
            instrument_frame = get_instrument_frame(self, instrument)
            instrument_frame.grid(row=id, column=0, sticky="NSEW")
            track_frame = Frame(self)
            track_frame.grid(row=id, column=1)

            tracks = [track for track in sequencer.tracks if track.instrument_id == id]
            for row, track in enumerate(tracks):
                RhythmTrackFrame(track_frame, track).grid(row=row, column=0, sticky="EW")


class MainWindow(Tk):
    def __init__(self, sequencer):
        Tk.__init__(self, className="Koshka")
        self.sequencer = sequencer

        self.control_panel = Frame(self)
        self.control_label = Label(self.control_panel, text="Control")

        self.start_button = Button(self.control_panel, text="Start")
        self.stop_button = Button(self.control_panel, text="Stop")
        self.quit_button = Button(self.control_panel, text="Quit")

        self.start_button.config(command=self.sequencer.play)
        self.stop_button.config(command=self.sequencer.stop)
        self.quit_button.config(command=self._quit)

        self.control_label.pack()
        self.start_button.pack()
        self.stop_button.pack()
        self.quit_button.pack()

        self.control_panel.grid(row=0, column=0, sticky='ns')

        self.sequencer_frame = SequencerFrame(self, sequencer)
        self.sequencer_frame.grid(row=0, column=1)

    def _quit(self):
        self.destroy()
        self.quit()
