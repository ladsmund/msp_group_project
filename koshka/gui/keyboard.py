from Tkinter import Tk, Button, Frame, Label, IntVar, RIDGE, CENTER, StringVar, Canvas, Toplevel
from ttk import Button, Frame, Label, Style, Checkbutton, OptionMenu, Entry, Radiobutton
import scales
from instruments import ScaleSynth
from instruments.instrument import ToneOnEvent, ToneOffEvent
from instruments.scalesynth import NewScaleEvent
import time



MIN_TONE = 0
MAX_TONE = 29

KEY_HEIGHT = 120
KEY_WIDTH = 30
KEYBOARD_HEIGHT = KEY_HEIGHT + 1
KEYBOARD_WIDTH = (MAX_TONE - MIN_TONE) * KEY_WIDTH

SCALE_COLOR = 'blue'
SCALE_PLOT_HEIGHT = 50
SCALE_PLOT_LINE_HEIGHT = 40
TONE_RADIUS = 10
TONE_Y = 25
TONE_COLOR = 'green'

CONTROL_FRAME_ACTIVE = 'light blue'
CONTROL_FRAME_INACTIVE = 'gray'

KEY_ON_TAG = "<<KEY_ON>>"
KEY_OFF_TAG = "<<KEY_OFF>>"

UPDATE_INTERVAL = 10


class Key:
    OCTAVE_KEYS = [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0]
    MIN_UPDATE_TIME = .04

    def __init__(self, tone, keyboard, canvas, x0, y0):
        self.tone = tone
        self.canvas = canvas
        self.keyboard = keyboard
        # self.instrument = instrument
        self.color, self.active_outline, self.pressed_fill = Key.get_key_color(tone)

        x = x0 + KEY_WIDTH
        y = y0 + KEY_HEIGHT
        self.widget = self.canvas.create_rectangle(
            x0, y0, x, y,
            fill=self.color,
            activeoutline=self.active_outline)

        self.pressed = False
        self.press_time = 0
        self.release_time = time.time()

    def work(self):
        active_press = self.release_time < self.press_time
        if active_press:
            if not self.pressed and time.time() - self.press_time > self.MIN_UPDATE_TIME:
                self.pressed = True
                self._press()
        else:
            if self.pressed and time.time() - self.release_time > self.MIN_UPDATE_TIME:
                self.pressed = False
                self._release()

    def _press(self, event=None):

        if self.keyboard.instrument is not None:
            self.keyboard.instrument.on(self.tone)
            self.canvas.itemconfigure(self.widget, fill=self.pressed_fill)
        pass

    def _release(self, event=None):
        if self.keyboard.instrument is not None:
            self.keyboard.instrument.off(self.tone)
            self.canvas.itemconfigure(self.widget, fill=self.color)
        pass

    def press(self, event=None):
        self.press_time = time.time()

    def release(self, event=None):
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

    def __init__(self, master, instrument=None):
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

        self.running = True
        self._worker()

    def _worker(self):
        if not self.running:
            return
        for k in self.keyboard_keys.values():
            k.work()
        self.after(UPDATE_INTERVAL, self._worker)


    def set_instrument(self, new_instrument):
        # print "set_instrument: %s" % str(new_instrument)
        for key in self.keyboard_keys.values():
            key.release()
        old_instrument = self.instrument
        self.instrument = new_instrument

        if not old_instrument is None:
            old_instrument.off()

    def create_key(self, tone):
        x0 = tone * KEY_WIDTH
        y0 = 0

        key = Key(tone, self, self.canvas, x0, y0)

        self.canvas.tag_bind(key.widget, "<Button-1>", key.press)
        self.canvas.tag_bind(key.widget, "<ButtonRelease-1>", key.release)

        if 0 <= tone < len(self.INPUT_KEYS):
            input_key = self.INPUT_KEYS[tone]
            self.bind_all("<Key-%s>" % input_key, key.press)
            self.bind_all("<KeyRelease-%s>" % input_key, key.release)

        return key

    def destroy(self):
        self.running = False
        return Frame.destroy(self)


class ScalePlot(Canvas):
    def __init__(self, master, tone_width=KEY_WIDTH):
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
        for width in range(16, 1, -2):
            color = "gray%i" % (20 + 3 * width)
            self.draw_scale(scales.EvenTempered(528), color=color, width=width, add_to_scales=False)

        self.tones = {}
        self.events = []
        self.running = True
        self.consume()

    def destroy(self):
        self.running = False
        return Canvas.destroy(self)

    def notify(self, event):
        self.events.append(event)

    def consume(self):
        if not self.running:
            return
        while len(self.events):
            event = self.events.pop()
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
        self.after(UPDATE_INTERVAL,self.consume)

    def delete_scale(self, scale):
        if type(scale) in self.scales:
            for l in self.scales[type(scale)]:
                self.delete(l)
            del self.scales[type(scale)]

    def draw_scale(self, scale, color=SCALE_COLOR, width=3, add_to_scales=True):
        if not type(scale) in self.scales:
            scale_objects = []

            for tone in range(self.min_tone, self.max_tone):
                cents = scale.get_cents(tone)
                x = int(self.tone_width * cents / 100.) + self.offset
                # x = s_elf.tone_width * tone + self.offset
                scale_objects.append(self.create_line(
                    x,
                    0,
                    x,
                    SCALE_PLOT_LINE_HEIGHT,
                    fill=color,
                    width=width))

                if add_to_scales:
                    scale_objects.append(self.create_text(
                        x,
                        SCALE_PLOT_LINE_HEIGHT + 5,
                        text="%.0f" % cents, font="Helvetica 10",
                        justify='center'))

            if add_to_scales:
                self.scales[type(scale)] = scale_objects


class ScaleWindow(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.keyboard_view = KeyboardView(self)
        self.keyboard_view.grid(column=1, row=0, sticky='nesw')
        self.keyboard_view.focus_set()
        self.row = 1
        self.instruments = []
        self.scale_plots = []
        self.control_frames = []
        self.activate_buttons = []

        self.radio_btn_var = IntVar()

        self.control_frames_style = Style()
        self.control_frames_style.configure('Active.TFrame', background=CONTROL_FRAME_ACTIVE)
        self.control_frames_style.configure('Inactive.TFrame', background=CONTROL_FRAME_INACTIVE)

    def activate_instrument(self):
        indx = self.radio_btn_var.get()
        for cf in self.control_frames:
            cf.config(style='Inactive.TFrame')
        self.control_frames[indx].config(style='Active.TFrame')

        instrument = self.instruments[indx]
        self.keyboard_view.set_instrument(instrument)

    def add_instrument(self, instrument):
        if not isinstance(instrument, ScaleSynth):
            return

        index = len(self.instruments)
        self.instruments.append(instrument)

        scale_plot = ScalePlot(self)
        scale_plot.draw_scale(instrument.scale)
        scale_plot.grid(column=1, row=self.row, sticky='nesw')
        self.scale_plots.append(scale_plot)
        instrument.add_observer(scale_plot)

        control_frame = Frame(self)
        self.control_frames.append(control_frame)

        activate_button = Radiobutton(control_frame,
                                      # text=str(instrument.name),
                                      textvar=instrument.id_variable,
                                      variable=self.radio_btn_var,
                                      value=index,
                                      command=self.activate_instrument,
                                      width=15,
                                      )
        activate_button.pack()

        self.radio_btn_var.set(index)
        self.activate_instrument()

        control_frame.grid(column=0, row=self.row, sticky='nesw')

        self.row += 1

    def destroy(self):
        for sp in self.scale_plots:
            sp.destroy()
        return Toplevel.destroy(self)
