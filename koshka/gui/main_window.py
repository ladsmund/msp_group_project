#!/usr/bin/python

import sys
import Tkinter
from Tkinter import Tk, RIDGE, IntVar, Menu, StringVar
import tkFileDialog
from ttk import Button, Frame, Label, Scale, Entry, Style
from instrument_frame import get_instrument_frame
from track_frame import RhythmTrackFrame
from sequencers.grid_sequencer import GridSequencer
import mixer_gui
import keyboard
import threading

from dac import DAC


class SequencerFrame(Frame):
    def __init__(self, master, sequencer):
        Frame.__init__(self, master)
        self.sequencer = sequencer

        self.control_panel = MainControlFrame(self, sequencer)
        self.control_panel.grid(row=0, column=0, sticky='ns')

        self.instrument_panel = Frame(self)
        self.instrument_panel.grid(row=0, column=1)

        self.rythm_track_frames = []

        for id, instrument in enumerate(sequencer.instruments):
            instrument_frame = get_instrument_frame(self.instrument_panel, instrument)
            instrument_frame.grid(row=id, column=0, sticky="NSEW")

            instrument_track_frame = Frame(self.instrument_panel)
            instrument_track_frame.grid(row=id, column=1, sticky="NSEW", padx=3, pady=3)

            tracks = [track for track in sequencer.tracks if track.instrument_id == id]
            for row, track in enumerate(tracks):
                rt_frame = RhythmTrackFrame(instrument_track_frame, track, sequencer)
                rt_frame.grid(row=row, column=0, sticky="EW")
                self.rythm_track_frames.append(rt_frame)

        self.bind('<<New-Time>>', self.consume)
        self.event_condition = threading.Condition()
        self.events = []
        self.running = True
        self.thread = threading.Thread(target=self._worker)
        self.thread.daemon = True
        self.thread.start()

        sequencer.add_observer(self)


    def consume(self, _):
        while len(self.events) > 0:
            time = self.events.pop().time
            for rt in self.rythm_track_frames:
                rt.set_time(time)

    def _worker(self):
        while self.running:
            self.event_condition.acquire()
            self.event_condition.wait(.5)
            if len(self.events) > 0:
                self.event_generate('<<New-Time>>')
            self.event_condition.release()

    def notify(self, event):
        self.event_condition.acquire()
        self.events.append(event)
        self.event_condition.notify_all()
        self.event_condition.release()

    def destroy(self):
        self.running = False
        self.thread.join()
        return Frame.destroy(self)


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

        measure_control_frame = Frame(self)
        measure_control_frame.pack()

        self.measure_resolution = StringVar(measure_control_frame)
        self.measure_resolution.set(self.sequencer.measure_resolution)
        self.beats_per_measure = StringVar(measure_control_frame)
        self.beats_per_measure.set(self.sequencer.beats_per_measure)

        Label(measure_control_frame, text='Resolution').grid(row=0, column=0, sticky='E')
        measure_resolution_entry = Entry(measure_control_frame, textvariable=self.measure_resolution, width=3)
        measure_resolution_entry.grid(row=0, column=1)

        Label(measure_control_frame, text='Beats').grid(row=1, column=0, sticky='E')
        beats_per_measure_entry = Entry(measure_control_frame, textvariable=self.beats_per_measure, width=3)
        beats_per_measure_entry.grid(row=1, column=1)

        change_measure_update = Button(measure_control_frame, text='Update Measure', command=self.change_measures)
        change_measure_update.grid(row=2, columnspan=2)

        # master_fader = mixer_frame.AudioFader(self, sequencer.getVolume, sequencer.setVolume)
        # master_fader.pack()

    def start_stop(self, event=None):
        if self.sequencer.running:
            self.sequencer.play()
        else:
            self.sequencer.stop()

    def change_measures(self):

        old_measure_resolution = self.sequencer.measure_resolution
        old_beats_per_measure = self.sequencer.beats_per_measure

        try:
            measure_resolution = int(self.measure_resolution.get())
            beats_per_measure = int(self.beats_per_measure.get())

            self.sequencer.change_measures(beats_per_measure, measure_resolution)
            print "ready to reload seq"
            self.master.master._open_sequencer(self.sequencer)
        except Exception as e:
            print e
            self.measure_resolution.set(old_measure_resolution)
            self.beats_per_measure.set(old_beats_per_measure)
            pass


class MainWindow(Tk):
    def __init__(self, namespace):
        Tk.__init__(self, className="Koshka")

        self.dac = DAC()
        self.dac.start()

        self.score_path = namespace.score

        self.sequencer = None
        self.sequencer_frame = None
        self.mixer_window = None
        self.scale_window = None
        self._open_score(self.score_path)

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

    def _open_sequencer(self, sequencer):
        print "\nMainWindow: _open_sequencer"

        print("Stop DAC...")
        self.dac.stop()
        print("Stop DAC...done")


        if self.sequencer_frame:
            self.sequencer_frame.destroy()
        if self.mixer_window:
            self.mixer_window.destroy()
        if self.scale_window is not None:
            self.scale_window.destroy()


        print("Reset sequencer...")
        if self.sequencer is not None:
            self.sequencer.stop()
            self.sequencer.remove_all_observers()
            for i in self.sequencer.instruments:
                i.remove_all_observers()
        print("Reset sequencer...done")

        print("Connect sequencder...")
        self.sequencer = sequencer
        self.dac.connect(self.sequencer.callback)
        print("Connect sequencder...done")

        for i in sequencer.instruments:
            i.id_variable = StringVar()
            i.id_variable.set(i.name_id)

        self.sequencer_frame = SequencerFrame(self, self.sequencer)
        self.sequencer_frame.pack()

        self.mixer_window = mixer_gui.MixerWindow(self, self.sequencer)

        self.scale_window = keyboard.ScaleWindow(self)
        for i in sequencer.instruments:
            self.scale_window.add_instrument(i)

        self.dac.start()
        pass

    def _open_score(self, score_path):
        self.score_path = score_path
        sequencer = GridSequencer(score_path,
                                  buffer_size=self.dac.bufferSize,
                                  sample_rate=self.dac.getSamplerate())

        self._open_sequencer(sequencer)

    def open(self, val=Tkinter.Event()):
        score_path = tkFileDialog.askopenfilename(filetypes=[('Text file', '.txt')])
        if score_path:
            self._open_score(score_path)

    def save(self, val=None):
        self.sequencer.save(self.score_path)
        # self.wm_attributes("-modified", 0)

    def save_as(self, val=None):
        self.score_path = tkFileDialog.asksaveasfilename(filetypes=[('Text file', '.txt')])
        self.save()
