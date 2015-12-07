from Tkinter import Tk, Button, Frame, Label, IntVar, RIDGE, CENTER, StringVar, Canvas
from ttk import Button, Frame, Label, Style, Checkbutton, OptionMenu, Entry

import scales

class ScalePlot(Canvas):
    MIN_TONE = 0
    MAX_TONE = 37
    SCALE_COLOR = 'dark green'
    HEIGTH = 100

    def __init__(self, master, tone_width, min_tone=MIN_TONE, max_tone=MAX_TONE):
        Canvas.__init__(self,
                        master,
                        background='gray',
                        # relief=RIDGE,
                        highlightthickness=0)
        self.tone_width = tone_width
        self.min_tone = min_tone
        self.max_tone = max_tone

        self.scales = {}
        self.draw_scale(scales.EvenTempered(528), color='gray46', width=5)
        self.scales = {}


    def draw_scale(self, scale, color=SCALE_COLOR, width=1):
        if not type(scale) in self.scales:
            lines = []

            for tone in range(self.min_tone, self.max_tone):
                x = self.tone_width * tone + int(self.tone_width/2)
                lines.append(self.create_line(x, 0, x, ScalePlot.HEIGTH, fill=color, width=width))

            self.scales[type(scale)] = lines
