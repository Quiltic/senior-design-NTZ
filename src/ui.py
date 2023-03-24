
from tkinter import *
from tkinter import filedialog
import summarization_poc
from tkinter.ttk import *



def browse_files():
    filename = filedialog.askopenfile( title = "Select a File", filetypes = [("All files", ".mp3 .mp4")])
    
    
    label_file_explorer.configure(text="File Opened: "+ str(filename))


# creates a Tk() object
master = Tk()
 
# sets the geometry of main
# root window
master.geometry("900x700")

 
label = Label(master, text ="Welcome to P.A.N.T.S", font=("Times New Roman", 25))
label.pack(pady = 10)
 
# a button widget which will open a new window on button click
btn = Button(master, text ="Run Speech To Text", command = None)#openNewWindow7)
btn.place(x=25, y=100)

btn = Button(master, text ="Run Text to Notes", command = summarization_poc.test_func)
btn.place(x=200, y=100)

btn = Button(master, text ="Run All", command = None)#openNewWindow7)
btn.place(x=350, y=100)

btn = Button(master, text ="Save", command = None)#openNewWindow7)
btn.place(x=500, y=100)

btn = Button(master, text ="Load", command = None)#openNewWindow7)
btn.place(x=650, y=100)

btn = Button(master, text = "Browse Files", command = browse_files)
btn.place(x=750, y=100)




# Create a File Explorer label
label_file_explorer = Label(master, text = None)
label_file_explorer.pack(pady = 10)
  
      


# mainloop, runs infinitely
mainloop()