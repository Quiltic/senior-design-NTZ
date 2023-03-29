
from tkinter import *
from tkinter import filedialog
import summarization_poc
import speech_to_text
from tkinter.ttk import *


def browse_files():
    filename = filedialog.askopenfile( title = "Select a File", filetypes = [("All files", ".mp3 .mp4 .wav")])    
    label_file_explorer.configure(text="File Opened: "+ str(filename))


# creates a Tk() object
master = Tk()
 
# sets the geometry of main
# root window
master.geometry("900x700")

 
label_main = Label(master, text ="Welcome to P.A.N.T.S", font=("Times New Roman", 25))
label_main.pack(pady = 10)

transcribed_text = Text(master, height=25, width=50, wrap=WORD)
transcribed_text.place(x=25, y=200)
#transcribed_text.config(state=DISABLED)

notes_text = Text(master, height=25, width=50, wrap=WORD)
notes_text.place(x=450, y=200)
 
# a button widget which will open a new window on button click
btn_run_speech_to_text = Button(master, text ="Run Speech To Text", command=lambda: speech_to_text.transcribe_file(transcribed_text, master))
btn_run_speech_to_text.place(x=25, y=100)

btn = Button(master, text ="Run Text to Notes", command=lambda: summarization_poc.generate_summary(notes_text, master))
btn.place(x=200, y=100)


btn_run_all = Button(master, text ="Run All", command = None)
btn_run_all.place(x=350, y=100)

btn_save = Button(master, text ="Save", command = None)
btn_save.place(x=500, y=100)

btn_load = Button(master, text ="Load", command = None)
btn_load.place(x=650, y=100)

btn_browse = Button(master, text = "Browse Files", command = browse_files)
btn_browse.place(x=750, y=100)



# Create a File Explorer label
label_file_explorer = Label(master, text = None)
label_file_explorer.pack(pady = 10)

transcription_label = Label(master, text = "TRANSCRIBED FILE")
transcription_label.place(x=150, y = 170)

notes_label = Label(master, text = "NOTES")
notes_label.place(x=600, y = 170)
  
      
# mainloop, runs infinitely
mainloop()