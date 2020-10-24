
import io

# allows for image formats other than gif

from PIL import Image, ImageTk

try:

  # Python2

  import Tkinter as tk

  from urllib2 import urlopen

except ImportError:

  # Python3

  import tkinter as tk

  from urllib.request import urlopen

root = tk.Tk()

url = 'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/126/126-bigskin-4.jpg'
image_bytes = urlopen(url).read()
# internal data file
data_stream = io.BytesIO(image_bytes)

# open as a PIL image object

pil_image = Image.open(data_stream)

# optionally show image info

# get the size of the image

w, h = pil_image.size

width = 615
height = 440

# split off image file name

fname = url.split('/')[-1]

sf = "{} ({}x{})".format(fname, w, h)

root.title(sf)

screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)

# convert PIL image object to Tkinter PhotoImage object

tk_image = ImageTk.PhotoImage(pil_image)

# put the image on a typical widget

label = tk.Label(root, image=tk_image, bg='brown')

label.pack(padx=5, pady=5)

root.mainloop()