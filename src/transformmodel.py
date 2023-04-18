import torch
import torch.nn as nn
import torch.optim as optim
import os
import numpy as np
from torch.utils.data.sampler import SubsetRandomSampler

PATH = "C:/Users/jtrex/Documents/SrDesignProj"

########################
### Training Helpers ###
########################


def avg_wer(wer_scores, combined_ref_len):
    return float(sum(wer_scores)) / float(combined_ref_len)


def _levenshtein_distance(ref, hyp):
    """Levenshtein distance is a string metric for measuring the difference
    between two sequences. Informally, the levenshtein disctance is defined as
    the minimum number of single-character edits (substitutions, insertions or
    deletions) required to change one word into the other. We can naturally
    extend the edits to word level when calculate levenshtein disctance for
    two sentences.
    """
    m = len(ref)
    n = len(hyp)

    # special case
    if ref == hyp:
        return 0
    if m == 0:
        return n
    if n == 0:
        return m

    if m < n:
        ref, hyp = hyp, ref
        m, n = n, m

    # use O(min(m, n)) space
    distance = np.zeros((2, n + 1), dtype=np.int32)

    # initialize distance matrix
    for j in range(0,n + 1):
        distance[0][j] = j

    # calculate levenshtein distance
    for i in range(1, m + 1):
        prev_row_idx = (i - 1) % 2
        cur_row_idx = i % 2
        distance[cur_row_idx][0] = i
        for j in range(1, n + 1):
            if ref[i - 1] == hyp[j - 1]:
                distance[cur_row_idx][j] = distance[prev_row_idx][j - 1]
            else:
                s_num = distance[prev_row_idx][j - 1] + 1
                i_num = distance[cur_row_idx][j - 1] + 1
                d_num = distance[prev_row_idx][j] + 1
                distance[cur_row_idx][j] = min(s_num, i_num, d_num)

    return distance[m % 2][n]


def word_errors(reference, hypothesis, ignore_case=False, delimiter=' '):
    """Compute the levenshtein distance between reference sequence and
    hypothesis sequence in word-level.
    :param reference: The reference sentence.
    :type reference: basestring
    :param hypothesis: The hypothesis sentence.
    :type hypothesis: basestring
    :param ignore_case: Whether case-sensitive or not.
    :type ignore_case: bool
    :param delimiter: Delimiter of input sentences.
    :type delimiter: char
    :return: Levenshtein distance and word number of reference sentence.
    :rtype: list
    """
    if ignore_case == True:
        reference = reference.lower()
        hypothesis = hypothesis.lower()

    ref_words = reference.split(delimiter)
    hyp_words = hypothesis.split(delimiter)

    edit_distance = _levenshtein_distance(ref_words, hyp_words)
    return float(edit_distance), len(ref_words)


def char_errors(reference, hypothesis, ignore_case=False, remove_space=False):
    """Compute the levenshtein distance between reference sequence and
    hypothesis sequence in char-level.
    :param reference: The reference sentence.
    :type reference: basestring
    :param hypothesis: The hypothesis sentence.
    :type hypothesis: basestring
    :param ignore_case: Whether case-sensitive or not.
    :type ignore_case: bool
    :param remove_space: Whether remove internal space characters
    :type remove_space: bool
    :return: Levenshtein distance and length of reference sentence.
    :rtype: list
    """
    if ignore_case == True:
        reference = reference.lower()
        hypothesis = hypothesis.lower()

    join_char = ' '
    if remove_space == True:
        join_char = ''

    reference = join_char.join(filter(None, reference.split(' ')))
    hypothesis = join_char.join(filter(None, hypothesis.split(' ')))

    edit_distance = _levenshtein_distance(reference, hypothesis)
    return float(edit_distance), len(reference)


def wer(reference, hypothesis, ignore_case=False, delimiter=' '):
    """Calculate word error rate (WER). WER compares reference text and
    hypothesis text in word-level. WER is defined as:
    .. math::
        WER = (Sw + Dw + Iw) / Nw
    where
    .. code-block:: text
        Sw is the number of words subsituted,
        Dw is the number of words deleted,
        Iw is the number of words inserted,
        Nw is the number of words in the reference
    We can use levenshtein distance to calculate WER. Please draw an attention
    that empty items will be removed when splitting sentences by delimiter.
    :param reference: The reference sentence.
    :type reference: basestring
    :param hypothesis: The hypothesis sentence.
    :type hypothesis: basestring
    :param ignore_case: Whether case-sensitive or not.
    :type ignore_case: bool
    :param delimiter: Delimiter of input sentences.
    :type delimiter: char
    :return: Word error rate.
    :rtype: float
    :raises ValueError: If word number of reference is zero.
    """
    edit_distance, ref_len = word_errors(reference, hypothesis, ignore_case,
                                         delimiter)

    if ref_len == 0:
        raise ValueError("Reference's word number should be greater than 0.")

    wer = float(edit_distance) / ref_len
    return wer


def cer(reference, hypothesis, ignore_case=False, remove_space=False):
    """Calculate charactor error rate (CER). CER compares reference text and
    hypothesis text in char-level. CER is defined as:
    .. math::
        CER = (Sc + Dc + Ic) / Nc
    where
    .. code-block:: text
        Sc is the number of characters substituted,
        Dc is the number of characters deleted,
        Ic is the number of characters inserted
        Nc is the number of characters in the reference
    We can use levenshtein distance to calculate CER. Chinese input should be
    encoded to unicode. Please draw an attention that the leading and tailing
    space characters will be truncated and multiple consecutive space
    characters in a sentence will be replaced by one space character.
    :param reference: The reference sentence.
    :type reference: basestring
    :param hypothesis: The hypothesis sentence.
    :type hypothesis: basestring
    :param ignore_case: Whether case-sensitive or not.
    :type ignore_case: bool
    :param remove_space: Whether remove internal space characters
    :type remove_space: bool
    :return: Character error rate.
    :rtype: float
    :raises ValueError: If the reference length is zero.
    """
    edit_distance, ref_len = char_errors(reference, hypothesis, ignore_case,
                                         remove_space)

    if ref_len == 0:
        raise ValueError("Length of reference should be greater than 0.")

    cer = float(edit_distance) / ref_len
    return cer


####################
### Data Loaders ###
####################

def tokenizer(inpStr):
    arr = [ord(c) for c in inpStr if ord(c)<128] # changes to ascii and removes non basic ascii
    return [c for c in arr if c != ' '] # removes ' ' which are the holes left from turning it to ascii and removing nonbasic

def detokenizer(inpArr):
    return ''.join([chr(a) for a in inpArr]) # from ascii array to string

class NotesDataset(torch.utils.data.Dataset):

  def __init__(self, source_folder):
    """
    data_loader = data.DataLoader(dataset=___,
                                batch_size=hparams['batch_size'],
                                shuffle=False,
                                **kwargs)
                                
    """

    self.x_data = []
    self.y_data = []

    transcribe = os.path.join(source_folder,"transcribe")
    notes = os.path.join(source_folder,"notes")
    
    transcribeFiles = [os.path.join(transcribe, f) for f in os.listdir(transcribe) if os.path.isfile(os.path.join(transcribe, f))]
    notesFiles = [os.path.join(notes, f) for f in os.listdir(transcribe) if os.path.isfile(os.path.join(notes, f))]

    for fil in transcribeFiles:
        with open(fil, 'r') as f:
            #print("newb:")
            #print(f.name)
            self.x_data.append(tokenizer(f.read()))
    
    for fil in notesFiles:
        with open(fil, 'r') as f:
            self.y_data.append(tokenizer(f.read()))
    
    self.x_data = torch.from_numpy(np.asarray(self.x_data))
    self.y_data = torch.from_numpy(np.asarray(self.y_data))
    

  def __len__(self):
    return len(self.x_data)  # required

  def __getitem__(self, idx):
    if torch.is_tensor(idx):
      idx = idx.tolist()
    preds = self.x_data[idx]
    pol = self.y_data[idx]
    
    return preds, pol



########################
###    LSTM MODEL    ###
########################

#pytorch LSTM: https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html
#background: https://machinelearningmastery.com/text-generation-with-lstm-in-pytorch/
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, dropout=0.2):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        #LSTM layer with dropout
        self.lstm = nn.LSTM(input_size, hidden_size, dropout=dropout)
        #dropout layer to assist with generalization / prevent overfitting. This is important as we are working with limited datasets
        self.dropout = nn.Dropout(dropout)
        #linear layer
        self.linear = nn.Linear(hidden_size, output_size)
        #Softmax activation
        self.softmax = nn.LogSoftmax(dim=1)   
    def forward(self, input):
        #Forward pass through LSTM, dropout layer, linear layer...
        output = self.lstm(input)
        output = self.dropout(output)
        output = self.linear(output.view(-1, self.hidden_size))
        output = self.softmax(output)
        return output
    def init_hidden(self, batch_size):
        #Initialize hidden layer to 0s
        return (torch.zeros(1, batch_size, self.hidden_size),
                torch.zeros(1, batch_size, self.hidden_size))



########################
##TESTING AND TRAINING##
########################

#train1
"""
    
    #we have source and target files, input, hidden, and output size, 
def train(model, device, source_file, target_file, input_size, hidden_size, output_size, learning_rate, num_epochs, dropout):
    #load text from file
    with open(source_file, 'r') as f:
        source_text = f.read()
    with open(target_file, 'r') as f:
        target_text = f.read()

    #Convert to ASCII
    source_tensor = torch.tensor([ord(c) for c in source_text]).unsqueeze(1).float()
    target_tensor = torch.tensor([ord(c) for c in target_text]).unsqueeze(1).float()
    
    optimizer = optim.Adam(model.parameters(), learning_rate=learning_rate)
    #We should consider replacing with torch.optim.SGD to assist with generalization? May converge slower
    #place torch lstm in training mode
    model.train()
    for epoch in range(num_epochs):
        source = source_tensor[epoch].unsqueeze(1)
        target = target_tensor[epoch].unsqueeze(1)
"""
    
#Training function, takes model (LSTM), device, train_loader (Probably libre 500 dataset), 
def train(model, device, train_loader, criterion, optimizer, scheduler, epoch):
    model.train()
    data_len = len(train_loader.dataset)
    for batch_idx, _data in enumerate(train_loader):
        transcription, labels = _data 
        transcription, labels = transcription.to(device), labels.to(device)

        optimizer.zero_grad()
        
        print(transcription)
        output = model(transcription)  # (batch, time, n_class)
        #output = F.log_softmax(output, dim=2)
        #output = output.transpose(0, 1) # (time, batch, n_class)

        loss = criterion(output, labels, data_len, data_len)
        loss.backward()

        optimizer.step()
        scheduler.step()
        if batch_idx % 100 == 0 or batch_idx == data_len:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(transcription), data_len,
                100. * batch_idx / len(train_loader), loss.item()))
    torch.save(model.state_dict(), f'{PATH}/Senior_Model_{1}.pt')

def main():
    #(self, input_size, hidden_size, output_size, dropout=0.2)
    hparams = {
        "n_input_size": 3010,
        "n_hidden_size": 1900,
        "n_output_size": 1024,
        "stride": 2,
        "dropout": 0.2,
        "learning_rate": 5e-4,
        "batch_size": 20,
        "epochs": 1
    }
    train_url="train-clean-100"
    test_url="test-clean"

    use_cuda = torch.cuda.is_available()
    torch.manual_seed(42)
    #device = torch.device("cuda" if use_cuda else "cpu")


    CUDA_DEVICE_NUM = 0
    # DEVICE = torch.device('cpu')

    #check cuda, we could get away with running this on CPU, but we shouldn't.
    device = torch.device(f'cuda:{CUDA_DEVICE_NUM}' if torch.cuda.is_available() else 'cpu')
    print('Device:', device)
    
    
    if not os.path.isdir(f"{PATH}/data"):
        os.makedirs(f"{PATH}/data")



    kwargs = {'num_workers': 1, 'pin_memory': True} if use_cuda else {}
    
    
    #Notes should be organized so that titles correlate to plaintext.
    #AmericanHistory wikipedia plaintext should correlate to AmericanHistory summary in corresonding target folder.
    dataset = NotesDataset(f"{PATH}/data")
    dataset.__len__()
    # Creating PT data samplers and loaders:
    train_sampler = SubsetRandomSampler([0 , int(dataset.__len__() * .8)])
    valid_sampler = SubsetRandomSampler([int(dataset.__len__() * .8) , int(dataset.__len__())])
    
    train_loader = torch.utils.data.DataLoader(dataset, batch_size=hparams['batch_size'], 
                                               sampler=train_sampler)
    test_loader = torch.utils.data.DataLoader(dataset, batch_size=hparams['batch_size'],
                                                    sampler=valid_sampler)
    #(input_size, hidden_size, output_size, dropout=0.2)
    model = LSTMModel(
        hparams['n_input_size'],hparams['n_hidden_size'],hparams["n_output_size"],
        hparams['dropout']
        ).to(device)

    #https://discuss.pytorch.org/t/how-to-count-model-parameters/128505 thanks to user mariosasko
    
    # print(model)
    print('Number of parameters', sum([param.nelement() for param in model.parameters()]))

    #Change to SGD?
    #use adamW optimization, good base choice
    optimizer = optim.AdamW(model.parameters(), hparams['learning_rate'])
    
    #Connectionist Temporal Classification loss
    #CTC Loss is specifically beneficial for neural networks training to recognize speech
    #In this case we use MSELoss, to find error between predicted and actual values, works well with summarization / text transformations
    criterion = nn.MSELoss(blank=42).to(device)
    
    #Adjusts learning rate according to epochs
    #Trusting boilerplate on this
    scheduler = optim.lr_scheduler.OneCycleLR(optimizer, max_lr=hparams['learning_rate'], 
                                            steps_per_epoch=int(len(train_loader)),
                                            epochs=hparams['epochs'],
                                            anneal_strategy='linear')
    #Used for Comet statistics
    #iter_meter = IterMeter()
    #Iterate through epochs.
    for epoch in range(1, hparams['epochs'] + 1):
        train(model, device, train_loader, criterion, optimizer, scheduler, epoch)
        #test(model, device, test_loader, criterion, epoch, "")
        
main()
