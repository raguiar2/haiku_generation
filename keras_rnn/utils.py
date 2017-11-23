import numpy as np
import string
import math
import operator
import csv
from pyphen import Pyphen
from keras.callbacks import Callback

class ValidateData(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))
        print('batch ended')

def sample(preds, temperature=1.0):

    if temperature == 0:
        temperature = 1

    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def get_train_data(csvname):
    data = ''
    firstlines = []
    with open(csvname,'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data += row[0]
            lines = row[0].split('\n')
            firstlines.append(lines[0])
    return data,firstlines

def create_sequences(corpus,sequence_length,sequence_step):
    sequences, next_chars = [], []
    idx = 0
    while idx + sequence_length + 1 < len(corpus):
        sequence = corpus[idx:idx+sequence_length]
        nextchar = corpus[idx+sequence_length]
        sequences.append(sequence)
        next_chars.append(nextchar)
        idx += sequence_step
    return sequences, next_chars

def syllable_count(text, lang='en_US'):
    """
    Function to calculate syllable words in a text.
    I/P - a text
    O/P - number of syllable words
    """
    text = text.lower()
    text = "".join(x for x in text if x not in exclude)

    if text is None:
        return 0
    elif len(text) == 0:
        return 0
    else:
        dic = Pyphen(lang=lang)
        count = 0
        for word in text.split(' '):
            word_hyphenated = dic.inserted(word)
            count += max(1, word_hyphenated.count("-") + 1)
        return count