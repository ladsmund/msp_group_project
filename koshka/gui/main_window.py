#!/usr/bin/python

import Tkinter
from Tkinter import Tk, RIDGE, IntVar, Menu
import tkFileDialog
from ttk import Button, Frame, Label, Scale
from instrument_frame import get_instrument_frame
from track_frame import RhythmTrackFrame
from sequencers.grid_sequencer import GridSequencer
import mixer_gui

from dac import DAC


class SequencerFrame(Frame):
    def __init__(self, master, sequencer):
        Frame.__init__(self, master)
        self.sequencer = sequencer

        self.control_panel = MainControlFrame(self, sequencer)
        self.control_panel.grid(row=0, column=0, sticky='ns')

        self.instrument_panel = Frame(self)
        self.instrument_panel.grid(row=0, column=1)

        for id, instrument in enumerate(sequencer.instruments):
            instrument_frame = get_instrument_frame(self.instrument_panel, instrument)
            instrument_frame.grid(row=id, column=0, sticky="NSEW")

            instrument_track_frame = Frame(self.instrument_panel)
            instrument_track_frame.grid(row=id, column=1, sticky="NSEW", padx=3, pady=3)

            tracks = [track for track in sequencer.tracks if track.instrument_id == id]
            for row, track in enumerate(tracks):
                RhythmTrackFrame(instrument_track_frame, track).grid(row=row, column=0, sticky="EW")


class MainControlFrame(Frame):
    def __init__(self, master, sequencer):
        Frame.__init__(self, master)
        self.sequencer = sequencer

        self.control_label = Label(self, text="Control")

        self.start_button = Button(self, text="Start")
        self.stop_button = Button(self, text="Stop")

        self.start_button.config(command=self.sequencer.play)
        self.stop_button.config(command=self.sequencer.stop)

        self.control_label.pack()
        self.start_button.pack()
        self.stop_button.pack()

        Label(self, text='Tempo').pack()
        self.tempo_label = Label(self)
        self.tempo_label.pack()

        def set_tempo(v):
            tempo = float(v)
            self.sequencer.set_speed(tempo)
            self.tempo_label.config(text='%3.0f' % tempo)

        tempo_scale = Scale(self, from_=400, to=5, command=set_tempo, orient='vertical')
        tempo_scale.set(self.sequencer.speed)
        tempo_scale.pack()

        # master_fader = mixer_frame.AudioFader(self, sequencer.getVolume, sequencer.setVolume)
        # master_fader.pack()

    def start_stop(self, event=None):
        if self.sequencer.running:
            self.sequencer.play()
        else:
            self.sequencer.stop()


class MainWindow(Tk):
    def __init__(self, namespace):
        Tk.__init__(self, className="Koshka")

        self.dac = DAC()
        self.dac.start()

        self.score_path = namespace.score

        self.sequencer_frame = None
        self.mixer_window = None
        self._open_sequencer(self.score_path)

        menu = Menu(self)
        self.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open...", command=self.open, accelerator="meta-o")
        filemenu.add_command(label="Save", command=self.save, accelerator="meta-s")
        filemenu.add_command(label="Save As...", command=self.save_as, accelerator="meta-shift-s")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)

        # Note: This is only implemented and tested for Mac OS
        self.bind_all("<Command-o>", self.open)
        self.bind_all("<Command-s>", self.save)
        self.bind_all("<Command-Shift-s>", self.save_as)
        self.bind_all("<Meta-o>", self.open)
        self.bind_all("<Meta-s>", self.save)
        self.bind_all("<Meta-Shift-s>", self.save_as)

        # self.wm_attributes("-titlepath",'What is this?')

    def __delete__(self, instance):
        print "__delete__"
        self._quit()

    def quit(self):
        print "tk quit"
        Tk.quit(self)
        pass

    def _quit(self):
        print "_quit"
        self.dac.stop()
        self.destroy()
        self.quit()

    def _open_sequencer(self, score_path):
        self.score_path = score_path
        self.dac.stop()
        self.sequencer = GridSequencer(score_path,
                                       buffer_size=self.dac.bufferSize,
                                       sample_rate=self.dac.getSamplerate())
        self.dac.connect(self.sequencer.callback)

        if self.sequencer_frame:
            self.sequencer_frame.destroy()
        self.sequencer_frame = SequencerFrame(self, self.sequencer)
        self.sequencer_frame.pack()

        if self.mixer_window:
            self.mixer_window.destroy()
        self.mixer_window = mixer_gui.MixerWindow(self, self.sequencer)

        self.dac.start()

    def open(self, val=Tkinter.Event()):
        score_path = tkFileDialog.askopenfilename(filetypes=[('Text file', '.txt')])
        if score_path:
            self._open_sequencer(score_path)

    def save(self, val=None):
        self.sequencer.save(self.score_path)
        # self.wm_attributes("-modified", 0)

    def save_as(self, val=None):
        self.score_path = tkFileDialog.asksaveasfilename(filetypes=[('Text file', '.txt')])
        self.save()
