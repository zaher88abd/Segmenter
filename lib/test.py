from tkinter import *
from PIL import Image
from PIL import ImageTk
import tkinter.filedialog as fd
from filter import *
import cv2

root = Tk()
original = Frame(root)
filterd = Frame(root)

original.pack(side=LEFT)
filterd.pack(side=RIGHT)


