#!/usr/bin/python

from Tkinter import Tk, Button, Frame, Label
import tkFileDialog
from ttk import Button, Frame, Label, Style
import ttk
import os.path
import instruments.sampler
import sys

_RHYTHM_BUTTON_WIDTH = 4
_FILE_BUTTON_WIDTH = 8


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

class Instrument(Frame):
    def __init__(self, master, instrument):
        Frame.__init__(self, master)
        self.instrument = instrument
        # self.config(width=200)

class SineSynthFrame(Instrument):
    def __init__(self, master, instrument):
        Instrument.__init__(self, master, instrument)


        self.frequency_label = Label(self, text=str(self.instrument.frequency))
        self.frequency_label.grid(row=0, column=0)


class SamplerFrame(Instrument):
    def __init__(self, master, instrument):
        Instrument.__init__(self, master, instrument)

        file_name = os.path.basename(self.instrument.filename)
        self.load_file_button = Button(self, text=file_name, command=self.load_file,
                                       width=_FILE_BUTTON_WIDTH)
        self.load_file_button.grid(row=0, column=1)

    def load_file(self):
        file_path = tkFileDialog.askopenfile(filetypes=[('audio files', '.wav')])
        if file_path:
            file_name = os.path.basename(file_path.name)
            self.instrument.load_file(file_path.name)
            self.load_file_button.config(text=file_name)


class TrackFrame(Frame):
    def __init__(self, master, track):
        Frame.__init__(self, master)
        self.track = track

        self.style_class = Style()
        self.style_class.configure('Track.TFrame',
                                   background='black',
                                   borderwidth=2,
                                   relief='raised',
                                   )

        self.config(style='Track.TFrame')


class RhythmTrackFrame(TrackFrame):
    def __init__(self, master, track):
        TrackFrame.__init__(self, master, track)


        self.id_label = Label(self, text=str(track.id))
        self.id_label.pack(side='left')#(row=0, column=0, stick='W')

        if isinstance(track.instrument, instruments.sampler.Sampler):
            instrument_frame = SamplerFrame(self, track.instrument)
        elif isinstance(track.instrument, instruments.sinesynth.SineSynth):
            instrument_frame = SineSynthFrame(self, track.instrument)
        else:
            instrument_frame = Instrument(self, track.instrument)

        instrument_frame.pack(side='left', expand=True)


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
        for track in sequencer.tracks:
            RhythmTrackFrame(self, track).grid(row=row, column=0,sticky="EW")
            # RhythmTrackFrame(self, track).pack(side='right', column=0, fill="both", expand=True)
            row += 1


class MainWindow(Tk):
    def __init__(self, sequencer):
        Tk.__init__(self)
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

        self.control_panel.grid(row=0,column=0, sticky='ns')

        self.sequencer_frame = SequencerFrame(self, sequencer)
        self.sequencer_frame.grid(row=0,column=1)

    def _quit(self):
        self.destroy()
        self.quit()
