"""
Created on August 14 2020
@author: Yigit GUNDUC
"""

from tkinter import *
import tkinter.ttk as ttk 
from tkinter import colorchooser
from tkinter import filedialog
import PIL
from PIL import Image , ImageDraw ,ImageGrab , ImageTk
from tkinter import messagebox
import matplotlib.pyplot as plt
import cv2
import random as r
import numpy as np
from tensorflow.keras import models

root = Tk()
root.title("Paint Clone")
root.geometry("500x600")

brush_color = "black"

def Paint(e):
    
    Brush_width = '%0.0f' % float(my_slider.get())
    brush_type2 = brush_type.get() #ROUND,PROJECTING
    
    x1 = e.x - 3
    y1 = e.y - 3 

    x2 = e.x + 3
    y2 = e.y + 3

    my_canvas.create_line(x1,y1,x2,y2,fill = brush_color,width = Brush_width,capstyle = brush_type2,smooth = True)

def chage_brush_size(thing):
    sliderLabel.config(text ='%0.0f' % float(my_slider.get()))

def change_brush_color():
    global brush_color 
    brush_color = colorchooser.askcolor(color=brush_color)[1]

def change_canvas_color():
    global bg_color 
    bg_color = "white"
    bg_color = colorchooser.askcolor(color=bg_color)[1]
    my_canvas.config(bg = bg_color)

def clear_screen():
    my_canvas.delete(ALL)
    my_canvas.config(bg = "white")

def clear_cancvas():
    my_canvas.delete(ALL)

def save():
    result = filedialog.asksaveasfilename(initialdir = "c:",filetypes = (("png files","*.png"),("all files","*.*")))

    if result.endswith(".png"):
        pass
    else :
        result += ".png"

    x = root.winfo_rootx()+my_canvas.winfo_x()
    y = root.winfo_rooty()+my_canvas.winfo_y()
    x1 = x + my_canvas.winfo_width()
    y1 = y + my_canvas.winfo_height()
    ImageGrab.grab().crop((x,y,x1,y1)).save(result)

    messagebox.showinfo("image saved","Your image has been suscessfully saved!")

def predict():
    result = "predicted{}.png".format(r.randint(0,10000)) 

    path = "path"

    x = root.winfo_rootx()+my_canvas.winfo_x()
    y = root.winfo_rooty()+my_canvas.winfo_y()
    x1 = x + my_canvas.winfo_width()
    y1 = y + my_canvas.winfo_height()
    ImageGrab.grab().crop((x,y,x1,y1)).save(path + result)

    loadedimage = cv2.imread(path + result,0)
    img = cv2.resize(loadedimage,(28,28))
    img[np.where(img != 255)] = 1
    img[np.where(img == 255)] = 0
    img = img.flatten()
    max = np.max(img)
    img = img / max
    img = np.array(img)[np.newaxis]
    my_model = models.load_model("path")
    p = my_model.predict_classes(img)
    
    messagebox.showinfo("prediction","prediction = {}".format(p))

w = 400
h = 400
my_canvas = Canvas(root,width=w,height=h,bg="white")
my_canvas.pack(pady=20) 

my_canvas.bind("<B1-Motion>" , Paint)

brush_option_frame = Frame(root)#bg = "red"
brush_option_frame.pack(pady=20)

brush_size_frame = LabelFrame(brush_option_frame,text = "Brush Size")


my_slider = ttk.Scale(brush_size_frame,from_ = 1,to = 100,orient = VERTICAL,value = 10, command = chage_brush_size)


sliderLabel = Label(brush_size_frame,text = my_slider.get())
sliderLabel.pack(pady = 5)

brush_type_frame = LabelFrame(brush_option_frame,text = "Brush type")


brush_type = StringVar()
brush_type.set("round")
my_slider.set(15)

change_color_frame = LabelFrame(brush_option_frame,text = "Change Color")

brush_color_button = Button(change_color_frame,text = "Change Brush Color",command = change_brush_color)


canvas_color_button = Button(change_color_frame,text = "Change canvas Color",command = change_canvas_color)

options_menu = LabelFrame(brush_option_frame,text = "Preferances")

clear_button = Button(root,text = "clear screen",command = clear_screen).place(x = 50, y = 500)

save_image = Button(root,text = "save as png",command = save).place(x = 220, y = 500)

predict_image = Button(root,text = "predict number",command = predict).place(x = 380, y = 500)

root.mainloop()