#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
from PIL import ImageTk

root=Tk()

canvas = Canvas(root,width = 600, height = 400, bg = 'blue')
canvas.pack(expand = YES, fill = BOTH)

image = ImageTk.PhotoImage(file = r".\01.gif")
canvas.create_image(0, 0, image = image, anchor = NW)

root.mainloop()