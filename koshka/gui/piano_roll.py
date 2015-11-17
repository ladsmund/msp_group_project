__author__ = 'mads'

from Tkinter import *
import ttk
# from tkinter import ttk

from functools import partial

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 300

frequency_resolution = 5
time_resolution = 20


class PianoRoll(Canvas):
    def __init__(self, master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT):
        Canvas.__init__(self, master, width=width, height=height)
        self.width = width
        self.height = height

        self.x_last = None
        self.y_last = None
        self.click_type = None

        # Draw grid lines
        for i in range(0, CANVAS_WIDTH, time_resolution):
            self.create_line(i, 0, i, CANVAS_HEIGHT, fill="#EEEEEE")

        for i in range(0, CANVAS_HEIGHT, frequency_resolution):
            self.create_line(0, i, CANVAS_WIDTH, i)

        # Draw piano keyboard
        key = 0
        for i in range(0, CANVAS_HEIGHT, frequency_resolution):
            if key in [1, 3, 6, 8, 10]:
                self.create_rectangle(0, i, CANVAS_WIDTH, i + frequency_resolution, fill="#EEEEEE")
                self.create_rectangle(0, i, 20, i + frequency_resolution, fill="black", outline='')
            key = (key + 1) % 12

    def click(self, event, obj):
        self.x_last = self.canvasx(event.x)
        self.y_last = self.canvasy(event.y)

        (ul_x, ul_y, lr_x, lr_y) = self.coords(obj)
        if lr_x - self.x_last < 5:
            self.click_type = 'resize_r'
        elif self.x_last - ul_x < 5:
            self.click_type = 'resize_l'
        else:
            self.click_type = 'move'

    def move_rect(self, event, obj):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)

        dx = x - self.x_last
        dy = y - self.y_last
        dx = time_resolution * (int(dx) / time_resolution)
        dy = frequency_resolution * (int(dy) / frequency_resolution)
        self.x_last += dx
        self.y_last += dy

        (ul_x, ul_y, lr_x, lr_y) = self.coords(obj)

        if self.click_type == 'resize_r':
            self.coords(obj, ul_x, ul_y, lr_x + dx, lr_y)
        elif self.click_type == 'resize_l':
            self.coords(obj, ul_x + dx, ul_y, lr_x, lr_y)
        elif self.click_type == 'move':
            self.move(obj, dx, dy)

    def add_node(self, tone, time, length=time_resolution):
        y = frequency_resolution * tone + frequency_resolution
        x = time * time_resolution + time_resolution
        note_rect = self.create_rectangle((x, y, x + time_resolution, y + frequency_resolution), fill="green")

        self.tag_bind(note_rect, "<Button-1>", partial(self.click, obj=note_rect))
        self.tag_bind(note_rect, "<B1-Motion>", partial(self.move_rect, obj=note_rect))
        self.tag_bind(note_rect, "<Enter>", lambda _: self.config(cursor="hand"))
        self.tag_bind(note_rect, "<Leave>", lambda _: self.config(cursor=""))


root = Tk()
piano_roll = PianoRoll(root)
piano_roll.grid(column=0, row=0, sticky=(N, E, S, W))

time = 0
for tone in [27, 25, 23, 22, 20, 18, 16, 15]:
    piano_roll.add_node(tone, time)
    time += 1

time = 0
for tone in [20, 18, 16, 15, 13, 11, 10, 8]:
    piano_roll.add_node(tone, time)
    time += 1

root.mainloop()
