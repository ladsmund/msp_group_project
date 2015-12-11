from Tkinter import IntVar, Button, Canvas
from ttk import Frame, Label, Style, Checkbutton, Button

_RHYTHM_BUTTON_WIDTH = 1

COLOR_ACTIVE = 'green'
COLOR_ACTIVE_STRESS = 'dark green'
COLOR_INACTIVE = 'gray30'
COLOR_INACTIVE_STRESS = 'gray15'

COLOR_PLAYING_ACTIVE = 'light green'
COLOR_PLAYING_ACTIVE_STRESS = 'green'
COLOR_PLAYING_INACTIVE = 'gray40'
COLOR_PLAYING_INACTIVE_STRESS = 'gray25'

class RhythmButton(Canvas):
    def __init__(self, master, track, beat, is_stressed):

        Canvas.__init__(self,
                        master,
                        width=20,
                        height=20,
                        highlightthickness=0)

        self.bind('<Button-1>', lambda _: self.command())
        self.bind('<<Toggle-Visual>>', lambda _: self.toggle_visual())

        self.track = track
        self.beat = beat
        self.playing = False
        self.is_stressed = is_stressed
        self.toggle_visual()

        self.changed = True

    def command(self):
        if self.track.rhythms[self.beat]:
            self.track.rhythms[self.beat] = 0
        else:
            self.track.rhythms[self.beat] = 1
        self.toggle_visual()

    def toggle_visual(self):
        if self.track.rhythms[self.beat]:
            if self.is_stressed:
                if self.playing:
                    self.config(bg=COLOR_PLAYING_ACTIVE_STRESS)
                else:
                    self.config(bg=COLOR_ACTIVE_STRESS)
            else:
                if self.playing:
                    self.config(bg=COLOR_PLAYING_ACTIVE)
                else:
                    self.config(bg=COLOR_ACTIVE)
        else:
            if self.is_stressed:
                if self.playing:
                    self.config(bg=COLOR_PLAYING_INACTIVE_STRESS)
                else:
                    self.config(bg=COLOR_INACTIVE_STRESS)
            else:
                if self.playing:
                    self.config(bg=COLOR_PLAYING_INACTIVE)
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
    def __init__(self, master, track, sequencer):
        TrackFrame.__init__(self, master, track)

        self.id_label = Label(self, text=str(track.id))
        self.id_label.pack(side='left')

        self.instrument_label = Label(self, text=str(track.instrument_tone), width=3)
        self.instrument_label.pack(side='left')

        mute_var = IntVar()

        self.mute_toggle = Checkbutton(self, command=lambda: check_cmd(track, mute_var), variable=mute_var)
        self.mute_toggle.pack(side='left')

        mute_var.set(not track.mute)

        rhythm_frame = Frame(self)
        rhythm_frame.pack(side='right')

        subdivision = sequencer.measure_resolution / sequencer.beats_per_measure

        self.buttons = []

        for b in range(0, len(self.track.rhythms)):
            button = RhythmButton(rhythm_frame, track, b, not b % subdivision)
            self.buttons.append(button)
            button.grid(row=0, column=b, padx=1)

        self.beat = 0

    def set_time(self, beat):
        self.buttons[self.beat].playing = False
        self.buttons[self.beat].toggle_visual()
        self.beat = beat
        self.buttons[self.beat].playing = True
        self.buttons[self.beat].toggle_visual()

    def destroy(self):
        return TrackFrame.destroy(self)