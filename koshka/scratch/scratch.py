from Tkinter import *
import ttk
# from tkinter import ttk

root = Tk()

h = ttk.Scrollbar(root, orient=HORIZONTAL)
v = ttk.Scrollbar(root, orient=VERTICAL)
canvas = Canvas(root, scrollregion=(0, 0, 1000, 1000), yscrollcommand=v.set, xscrollcommand=h.set)
h['command'] = canvas.xview
v['command'] = canvas.yview
ttk.Sizegrip(root).grid(column=1, row=1, sticky=(S, E))

canvas.grid(column=0, row=0, sticky=(N, W, E, S))
h.grid(column=0, row=1, sticky=(W, E))
v.grid(column=1, row=0, sticky=(N, S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

lastx, lasty = 0, 0


def xy(event):
    global lastx, lasty
    lastx, lasty = canvas.canvasx(event.x), canvas.canvasy(event.y)


def setColor(newcolor):
    global color
    color = newcolor
    canvas.dtag('all', 'paletteSelected')
    canvas.itemconfigure('palette', outline='white')
    canvas.addtag('paletteSelected', 'withtag', 'palette%s' % color)
    canvas.itemconfigure('paletteSelected', outline='#999999')


def addLine(event):
    global lastx, lasty
    x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)
    canvas.create_line((lastx, lasty, x, y), fill=color, width=5, tags='currentline')
    lastx, lasty = x, y


def doneStroke(event):
    canvas.itemconfigure('currentline', width=1)


# canvas.bind("<Button-1>", xy)
# canvas.bind("<B1-Motion>", addLine)
# canvas.bind("<B1-ButtonRelease>", doneStroke)

# id = canvas.create_rectangle((10, 10, 30, 30), fill="red", tags=('palette', 'palettered'))
# canvas.tag_bind(id, "<Button-1>", lambda x: setColor("red"))
# id = canvas.create_rectangle((10, 35, 30, 55), fill="blue", tags=('palette', 'paletteblue'))
# canvas.tag_bind(id, "<Button-1>", lambda x: setColor("blue"))
# id = canvas.create_rectangle((10, 60, 30, 80), fill="black", tags=('palette', 'paletteblack', 'paletteSelected'))
# canvas.tag_bind(id, "<Button-1>", lambda x: setColor("black"))
id = canvas.create_rectangle((10, 85, 30, 105), fill="gray", tags=('palette', 'palettegray'))
canvas.tag_bind(id, "<Button-1>", lambda x: setColor("gray"))


def move_obj(event):
    # objects = canv.find_overlapping(canvas.coords(ball)[0], canv.coords(ball)[1], canv.coords(ball)[2], canv.coords(ball)[3])

    (ul_x, ul_y, lr_x, lr_y) = canvas.coords(id)
    obj_x = (ul_x + lr_x) / 2
    obj_y = (ul_y + lr_y) / 2

    new_x = 10 * (int(event.x - obj_x) / 10)
    new_y = 10 * (int(event.y - obj_y) / 10)

    print("%i,%i" % (new_x, new_y))

    canvas.move(id, new_x, new_y)
    # canvas.update()


canvas.tag_bind(id, "<B1-Motion>", lambda x: move_obj(x))

setColor('black')
canvas.itemconfigure('palette', width=5)
root.mainloop()
