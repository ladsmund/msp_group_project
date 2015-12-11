#!/usr/bin/python

import Tkinter
from Tkinter import Tk, RIDGE, IntVar, Menu, StringVar
import tkFileDialog
from ttk import Button, Frame, Label, Scale, Entry, Style
from sequencers.grid_sequencer import GridSequencer
from sequencer_frame import SequencerFrame
import mixer_gui
import keyboard
import webbrowser


URL_HELP_DOC = "https://github.com/ladsmund/msp_group_project/blob/master/koshka/help.md"

from dac import DAC


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

        menu.add_cascade(label="Help", menu=filemenu)
        filemenu.add_command(label="Online Help...", command=lambda: webbrowser.open_new_tab(URL_HELP_DOC))


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

        # print("Stop DAC...")
        self.dac.stop()
        # print("Stop DAC...done")


        if self.sequencer_frame:
            self.sequencer_frame.destroy()
        if self.mixer_window:
            self.mixer_window.destroy()
        if self.scale_window is not None:
            self.scale_window.destroy()


        # print("Reset sequencer...")
        if self.sequencer is not None:
            self.sequencer.stop()
            self.sequencer.remove_all_observers()
            for i in self.sequencer.instruments:
                i.remove_all_observers()
        # print("Reset sequencer...done")

        # print("Connect sequencder...")
        self.sequencer = sequencer
        self.dac.connect(self.sequencer.callback)
        # print("Connect sequencder...done")

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
