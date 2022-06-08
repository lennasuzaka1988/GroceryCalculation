import io
import base64
import tkinter as tk
from urllib.request import urlopen

root = tk.Tk()
root.title('display a website image')
w = 520
h = 320
x = 80
y = 100

root.geometry('%dx%d+%d+%d' % (w, h, x, y))

image_url =