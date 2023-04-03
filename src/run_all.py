from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

import speech_to_text
import summarization_poc

def run_all(transcribed_text, notes_text, master, opened_file):
    speech_to_text.transcribe_file(transcribed_text, master, opened_file)
    summarization_poc.generate_summary(notes_text, master)
