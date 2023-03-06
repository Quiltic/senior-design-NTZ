## Importing Text Files
To import a text file for summarization, format your command like so:

'pants -notranscribe someTextToSummarize.txt'

the -notranscribe flag will enable and send text input directly to the summarization module.

## Exporting Text Files
You may use a custom name for the output file by specifiying an additional file name after the input file like so:

'pants someVideoToSummarize.mp4 customNameForSummarizedText.txt'
