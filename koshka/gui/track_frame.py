from Tkinter import IntVar, Button, Canvas
from ttk import Frame, Label, Style, Checkbutton, Button

_RHYTHM_BUTTON_WIDTH = 1

COLOR_ACTIVE = 'green'
COLOR_INACTIVE = 'gray30'

class RhythmButton(Canvas):
    def __init__(self, master, track, beat):

        Canvas.__init__(self,
                        master,
                        width=20,
                        height=20,
                        highlightthickness=0)

        self.bind('<Button-1>', lambda _: self.command())

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
            self.config(bg=COLOR_ACTIVE)
        else:
            self.config(bg=COLOR_INACTIVE)


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
    track.mute = not mute_var.get()


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

        mute_var.set(not track.mute)

        rhythm_frame = Frame(self)
        rhythm_frame.pack(side='right')

        for b in range(0, len(self.track.rhythms)):
            button = RhythmButton(rhythm_frame, track, b)
            # self.buttons.append(button)
            button.grid(row=0, column=b, padx=1)
