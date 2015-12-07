from Tkinter import Tk, Button, Frame, Label, IntVar, RIDGE, CENTER, StringVar, Canvas
from ttk import Button, Frame, Label, Style, Checkbutton, OptionMenu, Entry
import time
import threading


class Key:
    OCTAVE_KEYS = [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0]
    KEY_HEIGHT = 70
    KEY_WIDTH = 10
    SLEEP_TIME = 1

    def __init__(self, tone, instrument, canvas, x0, y0):
        self.tone = tone
        self.canvas = canvas
        self.instrument = instrument
        self.color, self.active_outline, self.pressed_fill = Key.get_key_color(tone)

        x = x0 + self.KEY_WIDTH
        y = y0 + self.KEY_HEIGHT
        self.widget = self.canvas.create_rectangle(
            x0, y0, x, y,
            fill=self.color,
            activeoutline=self.active_outline)

        self.pressed = False

    def press(self, event):
        if not self.pressed:
            # print "key_pressed: %i" % self.tone
            self.instrument.on(self.tone)
            self.canvas.itemconfigure(self.widget, fill=self.pressed_fill)
            self.pressed = True

    def release(self, event):
        if self.pressed:
            # print "key_release: %i" % self.tone
            self.instrument.off(self.tone)
            self.canvas.itemconfigure(self.widget, fill=self.color)
            self.pressed = False

    @staticmethod
    def get_key_color(tone):
        if Key.OCTAVE_KEYS[tone % 12]:
            color = 'black'
            pressed_fill = 'gray40'
        else:
            color = 'white'
            pressed_fill = 'gray70'
        active_outline = pressed_fill
        return color, active_outline, pressed_fill


class Keyboard_view(Frame):
    INPUT_KEYS = 'q2w3er5t6y7ui9o0pzsxdcfvbhnjm'
    HEIGHT = 100
    WIDTH = 37 * Key.KEY_WIDTH
    MIN_TONE = 0
    MAX_TONE = 37

    def __init__(self, master, instrument, tone_offset=0):
        Frame.__init__(self, master)
        self.instrument = instrument

        self.canvas = Canvas(self,
                             width=self.WIDTH,
                             height=self.HEIGHT,
                             background='gray',
                             highlightthickness=0
                             )
        self.canvas.pack()

        self.tone_offset = tone_offset
        self.keyboard_keys = {}

        for tone in range(self.MIN_TONE, self.MAX_TONE):
            self.keyboard_keys[tone] = self.create_key(tone)

    def create_key(self, tone):

        x0 = tone * Key.KEY_WIDTH
        y0 = 0

        x_line = int(x0 + Key.KEY_WIDTH / 2)
        self.canvas.create_line(x_line, 0, x_line, self.HEIGHT, fill='gray52')

        key = Key(tone, self.instrument, self.canvas, x0, y0)

        self.canvas.tag_bind(id, "<Button-1>", key.press)
        self.canvas.tag_bind(id, "<ButtonRelease-1>", key.release)

        if 0 <= tone < len(self.INPUT_KEYS):
            input_key = self.INPUT_KEYS[tone]
            self.bind_all("<Key-%s>" % input_key, key.press)
            self.bind_all("<KeyRelease-%s>" % input_key, key.release)

        return key


if __name__ == '__main__':
    import time
    from dac import DAC
    import instruments

    root = Tk()

    dac = DAC(bufferSize=2 ** 11)
    instrument = instruments.parse(['ScaleSynth', 'EvenTempered', '264'],
                                   dac.sample_rate,
                                   dac.buffer_size)

    dac.connect(instrument.callback)
    keyboard = Keyboard_view(root, instrument)
    keyboard.grid(column=0, row=0, sticky='nesw')

    keyboard.focus_set()

    dac.start()
    root.mainloop()

    dac.stop()
    time.sleep(.1)

    exit(0)
