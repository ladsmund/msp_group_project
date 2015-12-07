from Tkinter import Tk, Button, Frame, Label, IntVar, RIDGE, CENTER, StringVar, Canvas
from ttk import Button, Frame, Label, Style, Checkbutton, OptionMenu, Entry
from instrument_frame import get_instrument_frame
import time
import threading


class Key:
    OCTAVE_KEYS = [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0]
    KEY_HEIGHT = 70
    KEY_WIDTH = 20
    MIN_UPDATE_TIME = .04

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
        # self.pressed = False

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
    HEIGHT = Key.KEY_HEIGHT+10
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

    def terminate(self):
        for t in self.keyboard_keys.values():
            t.terminate()
        print "All keyes terminated"

    def destroy(self):
        print "Destroy"
        Frame.destroy(self)
        self.terminate()

    def create_key(self, tone):

        x0 = tone * Key.KEY_WIDTH
        y0 = 0

        key = Key(tone, self.instrument, self.canvas, x0, y0)

        self.canvas.tag_bind(id, "<Button-1>", key.press)
        self.canvas.tag_bind(id, "<ButtonRelease-1>", key.release)

        if 0 <= tone < len(self.INPUT_KEYS):
            input_key = self.INPUT_KEYS[tone]
            self.master.bind_all("<Key-%s>" % input_key, key.press)
            self.master.bind_all("<KeyRelease-%s>" % input_key, key.release)

        return key


if __name__ == '__main__':
    from dac import DAC
    import instruments

    root = Tk()

    dac = DAC(bufferSize=2 ** 11)
    instrument = instruments.parse(['ScaleSynth', 'EvenTempered', '264'],
                                   dac.sample_rate,
                                   dac.buffer_size)

    dac.connect(instrument.callback)

    instrument_frame = get_instrument_frame(root,instrument)
    instrument_frame.grid(column=0, row=0, sticky='nesw')

    keyboard = KeyboardView(root, instrument)
    keyboard.grid(column=0, row=1, sticky='nesw')
    keyboard.focus_set()

    from scale_plot import ScalePlot
    scale_plot = ScalePlot(root, Key.KEY_WIDTH)
    scale_plot.draw_scale(instrument.scale)
    scale_plot.grid(column=0, row=2, sticky='nesw')

    dac.start()

    try:
        root.mainloop()
    finally:
        print "Closing"
        dac.stop()
        print "terminated"

    exit(0)
