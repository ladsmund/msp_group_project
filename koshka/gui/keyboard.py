from Tkinter import Tk, Button, Frame, Label, IntVar, RIDGE, CENTER, StringVar, Canvas
from ttk import Button, Frame, Label, Style, Checkbutton, OptionMenu, Entry
import scales
from instruments import instrument, ScaleSynth
from instruments.instrument import ToneOnEvent, ToneOffEvent
from instruments.scalesynth import NewScaleEvent
from instrument_frame import get_instrument_frame
import time
import threading


MIN_TONE = 0
MAX_TONE = 17

KEY_HEIGHT = 120
KEY_WIDTH = 80
KEYBOARD_HEIGHT = KEY_HEIGHT + 1
KEYBOARD_WIDTH = (MAX_TONE-MIN_TONE) * KEY_WIDTH

SCALE_COLOR = 'dark red'
SCALE_PLOT_HEIGHT = 100
TONE_RADIUS = 10
TONE_Y = 50
TONE_COLOR = 'green'



class Key:
    OCTAVE_KEYS = [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0]
    MIN_UPDATE_TIME = .04

    def __init__(self, tone, instrument, canvas, x0, y0):
        self.tone = tone
        self.canvas = canvas
        self.instrument = instrument
        self.color, self.active_outline, self.pressed_fill = Key.get_key_color(tone)

        x = x0 + KEY_WIDTH
        y = y0 + KEY_HEIGHT
        self.widget = self.canvas.create_rectangle(
            x0, y0, x, y,
            fill=self.color,
            activeoutline=self.active_outline)

        self.pressed = False
        self.running = True
        self.press_time = 0
        self.release_time = time.time()
        self.worker_thread = threading.Thread(target=self._worker)
        self.worker_thread.daemon = True
        self.worker_thread.start()

    def terminate(self):
        self.running = False
        self.worker_thread.join()

    def _worker(self):

        while self.running:
            active_press = self.release_time < self.press_time
            if active_press:
                if not self.pressed and time.time() - self.press_time:
                    self.instrument.on(self.tone)
                    self.canvas.itemconfigure(self.widget, fill=self.pressed_fill)
                    self.pressed = True
            else:
                if self.pressed and time.time() - self.release_time:
                    self.instrument.off(self.tone)
                    self.canvas.itemconfigure(self.widget, fill=self.color)
                    self.pressed = False

            time.sleep(.1)

    def press(self, event):
        self.press_time = time.time()

    def release(self, event):
        self.release_time = time.time()

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


class KeyboardView(Frame):
    INPUT_KEYS = 'q2w3er5t6y7ui9o0pzsxdcfvbhnjm'

    def __init__(self, master, instrument):
        Frame.__init__(self, master)
        self.instrument = instrument

        self.canvas = Canvas(self,
                             width=KEYBOARD_WIDTH,
                             height=KEYBOARD_HEIGHT,
                             background='gray',
                             highlightthickness=0
                             )
        self.canvas.pack()

        self.keyboard_keys = {}

        for tone in range(MIN_TONE, MAX_TONE):
            self.keyboard_keys[tone] = self.create_key(tone)

    def terminate(self):
        for t in self.keyboard_keys.values():
            t.terminate()
        print "All keyes terminated"

    # def destroy(self):
    #     print "Destroy"
    #     Frame.destroy(self)
    #     self.terminate()

    def create_key(self, tone):
        x0 = tone * KEY_WIDTH
        y0 = 0

        key = Key(tone, self.instrument, self.canvas, x0, y0)

        self.canvas.tag_bind(key.widget, "<Button-1>", key.press)
        self.canvas.tag_bind(key.widget, "<ButtonRelease-1>", key.release)

        if 0 <= tone < len(self.INPUT_KEYS):
            input_key = self.INPUT_KEYS[tone]
            self.master.bind_all("<Key-%s>" % input_key, key.press)
            self.master.bind_all("<KeyRelease-%s>" % input_key, key.release)

        return key


class ScalePlot(Canvas):

    def __init__(self, master, tone_width):
        Canvas.__init__(self,
                        master,
                        background='gray',
                        height=SCALE_PLOT_HEIGHT,
                        highlightthickness=0)
        self.tone_width = tone_width
        self.offset = int(tone_width / 2)
        self.min_tone = MIN_TONE
        self.max_tone = MAX_TONE

        self.scales = {}
        for width in range(13,1,-2):
            color = "gray%i"%(30 + 3*width)
            self.draw_scale(scales.EvenTempered(528), color=color, width=width, add_to_scales=False)

        self.tones = {}

    def notify(self, event):
        if isinstance(event, ToneOnEvent):
            if isinstance(event.instrument, ScaleSynth):
                cents = event.instrument.scale.get_cents(event.tone)
                x = int(self.tone_width * cents / 100.) + self.offset
                id = self.create_oval(
                    x - TONE_RADIUS,
                    TONE_Y - TONE_RADIUS,
                    x + TONE_RADIUS,
                    TONE_Y + TONE_RADIUS,
                    fill=TONE_COLOR)

                if event.tone in self.tones:
                    self.delete(self.tones[event.tone])
                self.tones[event.tone] = id
        elif isinstance(event, ToneOffEvent):
            if event.tone in self.tones:
                self.delete(self.tones[event.tone])
        elif isinstance(event, NewScaleEvent):
            self.delete_scale(event.old_scale)
            self.draw_scale(event.new_scale)

    def delete_scale(self, scale):
        if type(scale) in self.scales:
            for l in self.scales[type(scale)]:
                self.delete(l)
            del self.scales[type(scale)]

    def draw_scale(self, scale, color=SCALE_COLOR, width=2, add_to_scales=True):
        if not type(scale) in self.scales:
            lines = []

            for tone in range(self.min_tone, self.max_tone):
                cents = scale.get_cents(tone)
                x = int(self.tone_width * cents / 100.) + self.offset
                # x = self.tone_width * tone + self.offset
                lines.append(self.create_line(x, 0, x, SCALE_PLOT_HEIGHT, fill=color, width=width))

            if add_to_scales:
                self.scales[type(scale)] = lines


if __name__ == '__main__':
    from dac import DAC
    import instruments

    root = Tk()

    dac = DAC()



    instrument = instruments.parse(['ScaleSynth', 'EvenTempered', '264'],
                                   dac.sample_rate,
                                   dac.buffer_size)
    instrument2 = instruments.parse(['ScaleSynth', 'EvenTempered', '264'],
                                   dac.sample_rate,
                                   dac.buffer_size)

    dac.connect(instrument.callback)

    instrument_frame = get_instrument_frame(root, instrument)
    instrument_frame.grid(column=0, row=0, sticky='nesw')

    keyboard = KeyboardView(root, instrument)
    keyboard.grid(column=0, row=1, sticky='nesw')
    keyboard.focus_set()

    scale_plot = ScalePlot(root, KEY_WIDTH)
    scale_plot.draw_scale(instrument.scale)
    scale_plot.grid(column=0, row=2, sticky='nesw')

    instrument.add_observer(scale_plot)

    scale_plot2 = ScalePlot(root, KEY_WIDTH)
    scale_plot2.draw_scale(instrument2.scale)
    scale_plot2.grid(column=0, row=3, sticky='nesw')

    instrument2.add_observer(scale_plot2)

    dac.start()

    try:
        root.mainloop()
    finally:
        print "Closing"
        dac.stop()
        print "terminated"

    exit(0)
