from tkinter import *
from Foundation import NSObject
from AppKit import NSApplication
from PyObjCTools import AppHelper
#initialize tkinter 
#turns out root has no inherent meaning, its just like the root of all child processes so its known as such
root = Tk()
#get screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#set size
root.geometry(f'{screen_width}x{screen_height}+0+0')

#no window stuff aka no title bar no clickable buttons no borders
root.overrideredirect(True)

#makes background transparent
root.attributes('-transparent', True)
root.config(bg='systemTransparent')

l = Label(root, text="HI this is an overlay", fg="white", font=("Arial", 20), 
          bg='systemTransparent')
l.pack()

#sets it to the topmost window, aka makes it an overlay. the one js means true
root.wm_attributes("-topmost", 1)


def make_clickthrough():
    root.update()
    #quite honestly I don't understand this well, but from my understanding it is macos specific
    #this is because it utilizes PyObjC and AppKit which seem to be macos specific
    #pretty much, for every window, or process in this application, which is the tk window, it should ignore all mouse clicks, making it just an overlay
    for window in NSApplication.sharedApplication().windows():
        window.setIgnoresMouseEvents_(True)

#js makes the it actaully clickthroughable
root.after(100, make_clickthrough)

#update
root.mainloop()