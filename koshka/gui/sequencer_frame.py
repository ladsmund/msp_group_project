import sys
import Tkinter
from Tkinter import Tk, RIDGE, IntVar, Menu, StringVar
import tkFileDialog
from ttk import Button, Frame, Label, Scale, Entry, Style
from instrument_frame import get_instrument_frame
from track_frame import RhythmTrackFrame


UPDATE_INTERVAL = 10


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

        self.events = []
        sequencer.add_observer(self)

        self.running = True
        self.consume()


    def consume(self):
        if not self.running:
            return
        while len(self.events) > 0:
            time = self.events.pop().time
            for rt in self.rythm_track_frames:
                rt.set_time(time)
        self.after(UPDATE_INTERVAL,self.consume)

    def notify(self, event):
        self.events.append(event)

    def destroy(self):
        self.running = False
        return Frame.destroy(self)