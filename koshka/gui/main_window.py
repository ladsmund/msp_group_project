#!/usr/bin/python

from Tkinter import Tk, RIDGE, IntVar
from ttk import Button, Frame, Label, Scale
from instrument_frame import get_instrument_frame
from track_frame import RhythmTrackFrame


class SequencerFrame(Frame):
    def __init__(self, master, sequencer):
        Frame.__init__(self, master)
        self.sequencer = sequencer

        for id, instrument in enumerate(sequencer.instruments):
            instrument_frame = get_instrument_frame(self, instrument)
            instrument_frame.grid(row=id, column=0, sticky="NSEW")

            instrument_track_frame = Frame(self)
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
            self.tempo_label.config(text='%3.0f'%tempo)

        tempo_scale = Scale(self, from_=400, to=5, command=set_tempo, orient='vertical')
        tempo_scale.set(self.sequencer.speed)
        tempo_scale.pack()



class MainWindow(Tk):
    def __init__(self, sequencer):
        Tk.__init__(self, className="Koshka")
        self.sequencer = sequencer


        # self.quit_button = Button(self, text="Quit")
        # self.quit_button.config(command=master._quit)
        # self.quit_button.pack()


        self.control_panel = MainControlFrame(self, sequencer)
        self.control_panel.grid(row=0, column=0, sticky='ns')
        self.sequencer_frame = SequencerFrame(self, sequencer)
        self.sequencer_frame.grid(row=0, column=1)

    def _quit(self):
        self.destroy()
        self.quit()
