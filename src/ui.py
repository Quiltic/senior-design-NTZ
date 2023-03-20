
import tkinter as tk
from summarization_poc import summarization_poc
from tkinter.ttk import *

 
# creates a Tk() object
master = tk.Tk()
 
# sets the geometry of main
# root window
master.geometry("900x700")
 
 
# function to open a new window
# on a button click
def openNewWindow7():
     
    # Toplevel object which will
    # be treated as a new window
    newWindow = tk.Toplevel(master)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("New Window")
 
    # sets the geometry of toplevel
    newWindow.geometry("900x700")
 
    # A Label widget to show in toplevel
    Label(newWindow, text ="This is a new window").pack()
 
 
label = Label(master, text ="This is the main window")
label.pack(pady = 10)
 
# a button widget which will open a new window on button click
btn = Button(master, text ="Run Speech To Text", command = openNewWindow7)
btn.pack(pady = 5)

btn = Button(master, text ="Run Text to Notes", command = summarization_poc)
btn.pack(pady = 5)

btn = Button(master, text ="Run All", command = openNewWindow7)
btn.pack(pady = 5)

btn = Button(master, text ="Click to open a new window", command = openNewWindow7)
btn.pack(pady = 5)
 
# mainloop, runs infinitely
tk.mainloop()