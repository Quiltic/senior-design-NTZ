import torch
import zipfile
import torchaudio
from glob import glob

from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

device = torch.device('cpu')  # gpu also works, but our models are fast enough for CPU

model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                       model='silero_stt',
                                       language='en', # also available 'de', 'es'
                                       device=device)
(read_batch, split_into_batches,
 read_audio, prepare_model_input) = utils  # see function signature for details

#download a single file, any format compatible with TorchAudio (soundfile backend)
# torch.hub.download_url_to_file('https://opus-codec.org/static/examples/samples/speech_orig.wav',
#                                dst ='speech_orig.wav', progress=True)

def transcribe_file(btn, master):
    btn.configure(state=NORMAL)
    btn.delete("1.0", END)
    btn.insert(END, "TRANSCRIBING FILE........")
    btn.configure(state=DISABLED)
    master.update()
    test_files = glob('chemistry.wav')
    batches = split_into_batches(test_files, batch_size=10)
    input = prepare_model_input(read_batch(batches[0]),
                                device=device)

    output = model(input)
    time_through = 1
    for example in output:
        if time_through > 1:
            teststr = ' ' + decoder(example.cpu())
        else:
            teststr = decoder(example.cpu())

       
        file1 = open("input_backup.txt", 'w')
        file1.write(teststr)
        file1.close() 

        print(type(teststr))
        print(decoder(example.cpu()))

    file1 = open("input_backup.txt", 'r')
    txt = file1.read()
    btn.configure(state=NORMAL)
    btn.configure(state=NORMAL)
    btn.delete("1.0", END)
    btn.insert(END, txt)
    btn.configure(state=DISABLED)

        