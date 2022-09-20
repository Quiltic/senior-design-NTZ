# Design Diagrams

### D0:

- Inputs: a pre-transcribed lecture
- Output: A note sheet summarizing lecture content

<img src="D0.png" alt="D0" style="zoom:120%;" />

### D1:

- The Speech to Text AI generates a transcription of the lecture using pytorch
- Using the lecture transcription, a summarized notes sheet is generated. 

<img src="D1.png" alt="D1" style="zoom:13%;" />

### D2:

- Handle audio input using torchaudio libary.
- Train the pytorch AI using the lecture content and generate a lecture transcription.
- Another AI is trained to generate a notes sheet from the lecture summary to return to the user. 

<img src="D2.png" alt="D2" style="zoom: 12%;" />