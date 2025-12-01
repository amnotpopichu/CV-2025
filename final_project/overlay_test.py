from tkinter import *
from Foundation import NSObject
from AppKit import NSApplication
from PyObjCTools import AppHelper

root = Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f'{screen_width}x{screen_height}+0+0')
root.overrideredirect(True)
root.attributes('-transparent', True)
root.config(bg='systemTransparent')

l = Label(root, text="HI this is an overlay", fg="white", font=("Arial", 20), 
          bg='systemTransparent')
l.pack()

root.wm_attributes("-topmost", 1)

def make_clickthrough():
    root.update()
    for window in NSApplication.sharedApplication().windows():
        window.setIgnoresMouseEvents_(True)

root.after(100, make_clickthrough)

root.mainloop()