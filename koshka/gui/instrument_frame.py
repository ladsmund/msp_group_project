from Tkinter import Tk, Button, Frame, Label, IntVar, RIDGE, CENTER, StringVar
import tkFileDialog
from ttk import Button, Frame, Label, Style, Checkbutton, OptionMenu, Entry
import os.path
import instruments
import scales

_INSTRUMENT_LABEL_WIDTH = 25
_FILE_BUTTON_WIDTH = 3


class Instrument(Frame):
    def __init__(self, master, instrument):
        Frame.__init__(self, master, relief=RIDGE)
        self.instrument = instrument

        Label(self,
              text=instrument.name,
              width=_INSTRUMENT_LABEL_WIDTH,
              ).grid(row=0, padx=3, pady=3)


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

class DrumsetFrame(Instrument):
    def __init__(self, master, instrument = instruments.Drumset()):
        Instrument.__init__(self, master, instrument)

        row = 1
        for ch in instrument:
            ch_frame = SamplerFrame(self,ch.device).grid(row=row, padx=3)
            # Label(self,text="%s"%ch.device.filename).grid(row=row, padx=3)
            row += 1




class ScaleSynthFrame(Instrument):

    def find_scale(self, name):
        for s in scales.SCALES:
            if s.__name__ == name:
                return s
        return None

    def find_scale_constructor(self, scale_instance):
        for s in scales.SCALES:
            if isinstance(scale_instance, s):
                return s
        return None

    def set_scale(self, scale_name):
        freq = self.instrument.scale.base_frequency
        scale = self.find_scale(scale_name)(freq)
        self.instrument.set_scale(scale)

    def set_frequncy(self):
        print "set frequency: %s" % self.freq_var.get()
        try:
            freq = int(self.freq_var.get())
            scale = self.find_scale_constructor(self.instrument.scale)(freq)
            self.instrument.set_scale(scale)
        except:
            self.freq_var.set(self.instrument.scale.base_frequency)

    def __init__(self, master, instrument):
        Instrument.__init__(self, master, instrument)

        scale_name = [s.__name__ for s in scales.SCALES]
        scale_name = [scale_name[0]] + scale_name

        variable = StringVar(self)
        # variable.set()  # default value

        w = OptionMenu(self, variable, *scale_name, command=self.set_scale)
        w.grid(row=1, sticky="W", padx=3)

        freq_frame = Frame(self)
        freq_frame.grid(row=2, sticky="W", padx=3)
        Label(freq_frame, text='Base Frequency: ').pack(side='left')

        self.freq_var = StringVar(self)
        self.freq_var.set(str(instrument.scale.base_frequency))
        freq_entry = Entry(freq_frame, textvariable=self.freq_var, width=5)
        freq_entry.pack(side='left')

        freq_update = Button(freq_frame, text='Update', command=self.set_frequncy)
        freq_update.pack(side='left')


def get_instrument_frame(master, instrument):
    # if isinstance(instrument, instruments.sampler.Sampler):
    #     return SamplerFrame(master, instrument)
    if isinstance(instrument, instruments.ScaleSynth):
        return ScaleSynthFrame(master, instrument)
    elif isinstance(instrument, instruments.Drumset):
        return DrumsetFrame(master, instrument)
    else:
        return Instrument(master, instrument)
