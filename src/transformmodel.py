import torch
import torch.nn as nn
import torch.optim as optim

#LSTM model:
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, dropout=0.2):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size, dropout=dropout)
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)   
    def forward(self, input, hidden):
        output, hidden = self.lstm(input, hidden)
        output = self.dropout(output)
        output = self.linear(output.view(-1, self.hidden_size))
        output = self.softmax(output)
        return output, hidden
    def init_hidden(self, batch_size):
        return (torch.zeros(1, batch_size, self.hidden_size),
                torch.zeros(1, batch_size, self.hidden_size))



#FOR TRAINING:
    #we have source and target files, input, hidde, and output size, 
def train(source_file, target_file, input_size, hidden_size, output_size, learning_rate, num_epochs, dropout):
    #load text
    with open(source_file, 'r') as f:
        source_text = f.read()
    with open(target_file, 'r') as f:
        target_text = f.read()

    #Convert to ASCII
    source_tensor = torch.tensor([ord(c) for c in source_text]).unsqueeze(1).float()
    target_tensor = torch.tensor([ord(c) for c in target_text]).unsqueeze(1).float()
    
    model = LSTMModel(input_size, hidden_size, output_size, dropout=dropout)
    optimizer = optim.Adam(model.parameters(), learning_rate=learning_rate)
    
def tokenizer(inpStr):
    arr = [ord(c) for c in inpStr if ord(c)<128] # changes to ascii and removes non basic ascii
    return [c for c in arr if c != ' '] # removes ' ' which are the holes left from turning it to ascii and removing nonbasic

def detokenizer(inpArr):
    return ''.join([chr(a) for a in inpArr]) # from ascii array to string
    

