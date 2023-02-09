## Summarization ##
### What To Expect ###

plaintext transcription
bulleted notes of topic

### Creating A Summary From a Text File ###

P.A.N.T.S will automatically generate a plaintext transcription of the video and write it to 
input.txt. The summarization service will read input.txt and using the OpenAI API will recursively summarize
and bullet point the text and write it to output.txt

### Summarizing Recently Transcribed Text ###

Once the transcription service is complete, P.A.N.T.S will read in the input.txt file and recursively generate
a bulleted list and write it to output.txt