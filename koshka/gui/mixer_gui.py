import Tkinter
from Tkinter import Tk, RIDGE, IntVar, Menu, Toplevel, Canvas, StringVar
from ttk import Button, Label, Scale, Sizegrip, Scrollbar, Frame

FADER_WIDTH = 120
FADER_HEIGHT = 200


class AudioFader(Frame):
    def __init__(self, master, get_gain, set_gain, label=''):
        Frame.__init__(self, master, width=FADER_WIDTH, height=FADER_HEIGHT)
        self.get_gain = get_gain
        self._set_gain = set_gain

        if isinstance(label, StringVar):
            Label(self, textvar=label, width=15).pack()
        else:
            Label(self, text=label, width=15).pack()
        self.gain_label = Label(self)

        gain_scale = Scale(self, from_=1, to=0, command=self.set_gain, orient='vertical')
        gain_scale.set(self.get_gain())
        gain_scale.pack()

        self.gain_label.pack()

    def set_gain(self, value):
        gain = float(value)
        self._set_gain(gain)
        self.gain_label.config(text='%1.2f' % gain)


class MixerFrame(Frame):
    def __init__(self, master, mixer):
        Frame.__init__(self, master)

        scrollbar_h = Scrollbar(self, orient='horizontal')
        scrollbar_v = Scrollbar(self, orient='vertical')
        self.canvas = Canvas(self,
                             background='gray',
                             scrollregion=(0, 0, (3 + len(mixer) * FADER_WIDTH), FADER_HEIGHT),
                             yscrollcommand=scrollbar_v.set,
                             xscrollcommand=scrollbar_h.set)

        scrollbar_v.config(command=self.canvas.yview)
        scrollbar_h.config(command=self.canvas.xview)

        self.canvas.bind("<MouseWheel>",
                         lambda e: self.canvas.yview_scroll(-e.delta, 'units'))
        self.canvas.bind("<Shift-MouseWheel>",
                         lambda e: self.canvas.xview_scroll(-e.delta, 'units'))

        Sizegrip(self).grid(column=2, row=1, sticky='se')
        self.canvas.grid(column=0, row=0, sticky='nwes')
        scrollbar_h.grid(column=0, row=1, sticky='we')
        scrollbar_v.grid(column=1, row=0, sticky='sn')

        master_fader = AudioFader(self, mixer.getVolume, mixer.setVolume, "Master")
        master_fader.grid(column=2, row=0, sticky='nwes')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        for i, channel in enumerate(mixer):
            if channel.device.id_variable is not None:
                name = channel.device.id_variable
            else:
                name = channel.device.name_id

            fader = AudioFader(self.canvas, channel.get_gain, channel.set_gain, name)
            self.canvas.create_window(i * FADER_WIDTH, 0, anchor='nw', window=fader)


class MixerWindow(Toplevel):
    def __init__(self, master, mixer):
        Toplevel.__init__(self, master, width=400)
        mixer_frame = MixerFrame(self, mixer)
        mixer_frame.grid(row=0, column=0, sticky='nwes')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


if __name__ == '__main__':

    from mixer import Mixer
    from instruments import Drumset

    root = Tk()
    mixer = Mixer()
    for _ in range(10):
        mixer.add_device(Drumset())

    mixer_frame = MixerWindow(root, mixer)
    root.mainloop()

    pass
