
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import summarization_poc
import speech_to_text
import run_all
import os
import re

current_path = os.getcwd()
parent_path = os.path.abspath(os.path.join(current_path, os.pardir))
transcription_path = parent_path+ '\\transcription_files\\'
summary_training_output_path = parent_path +'\\summary_files\\'


def please_run_me_over_with_a_rusty_bus(file_name, final_string):
    f = open(file_name, 'w', encoding='utf-8')
    f.write(final_string)
    f.close()

def run_pants_multiple_times_for_data():
    with open('train.txt', encoding='utf-8') as f:
        content = f.read().splitlines() 

    end_str = ''
    for each in content:
        try:
            if each != " ":
                each = each.lstrip().rstrip()
                if each[0] == "=":
                    end_str_final = end_str
                    end_str = ''
                    file_name = ''
                    for x in each:
                        if x != "=":
                            file_name += x
                    file_name = file_name.lstrip().rstrip()
                    file_name += '.txt'
                    file_name = transcription_path + file_name
                    # print(end_str_final)
                    print('---------------------' + file_name + '---------------------')
                    please_run_me_over_with_a_rusty_bus(file_name, end_str_final)

                else:
                    end_str += each
        except:
            pass

    

def get_summary_training_data(transcription_path, summary_output_path):

    for filename in os.listdir(transcription_path):

        try:
            f = os.path.join(transcription_path, filename)
            if os.path.isfile(f):
                in_file = f
                out_file = summary_output_path + f.split('\\')[-1]
                summarization_poc.generate_summary_training_data(in_file, out_file)
        except:
            pass

get_summary_training_data(transcription_path ,summary_training_output_path)


# opened_file = ''

# def browse_files():
#     filename = filedialog.askopenfile( title = "Select a File", filetypes = [("All files", ".mp3 .mp4 .wav")])   
#     opened_file = os.path.basename(str(filename))
#     opened_file = opened_file.split("'")[0]
#     label_file_explorer.configure(text="File Opened: "+ opened_file)

# def clear_text_widgets(btn1, btn2, master):

#     print("clear text widget")
#     btn1.configure(state=NORMAL)
#     btn1.delete("1.0", END)
#     btn1.configure(state=DISABLED)

#     master.update()

#     btn2.configure(state=NORMAL)
#     btn2.delete("1.0", END)
#     btn2.configure(state=DISABLED)

#     master.update()

# # creates a Tk() object
# master = Tk()
 
# # sets the geometry of main
# # root window
# master.geometry("900x700")

 
# label_main = Label(master, text ="Welcome to P.A.N.T.S", font=("Times New Roman", 25))
# label_main.pack(pady = 10)

# transcribed_text = Text(master, height=25, width=50, wrap=WORD)
# transcribed_text.place(x=25, y=200)
# #transcribed_text.config(state=DISABLED)

# notes_text = Text(master, height=25, width=50, wrap=WORD)
# notes_text.place(x=450, y=200)
 
# # a button widget which will open a new window on button click
# btn_run_speech_to_text = Button(master, text ="Run Speech To Text", command=lambda: speech_to_text.transcribe_file(transcribed_text, master, opened_file))
# btn_run_speech_to_text.place(x=25, y=100)

# btn = Button(master, text ="Run Text to Notes", command=lambda: summarization_poc.generate_summary(notes_text, master))
# btn.place(x=200, y=100)


# btn_run_all = Button(master, text ="Run All", command=lambda: run_all.run_all(transcribed_text, notes_text, master, opened_file))
# btn_run_all.place(x=350, y=100)

# btn_save = Button(master, text ="Clear", command = lambda: clear_text_widgets(transcribed_text, notes_text, master))
# btn_save.place(x=500, y=100)

# btn_load = Button(master, text ="Load", command=lambda: summarization_poc.load_text_to_notes(notes_text, master))
# btn_load.place(x=650, y=100)

# btn_browse = Button(master, text = "Browse Files", command = browse_files)
# btn_browse.place(x=750, y=100)

# # Create a File Explorer label
# label_file_explorer = Label(master, text = None)
# label_file_explorer.pack(pady = 10)

# transcription_label = Label(master, text = "TRANSCRIBED FILE")
# transcription_label.place(x=150, y = 170)

# notes_label = Label(master, text = "NOTES")
# notes_label.place(x=600, y = 170)
  
      
# # mainloop, runs infinitely
# mainloop()