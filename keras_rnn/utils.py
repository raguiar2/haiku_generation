import numpy as np
import string
import math
import operator
import csv
from pyphen import Pyphen
from keras.callbacks import Callback
# import matplotlib.pyplot as plt

def sample(preds, temperature=1.0):

    if temperature >= 0.0:
        temperature = 1
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    # plt.plot(preds)
    # plt.show()
    return np.argmax(probas)

def invalid_char(ch,i,rowlist):
    return ch == '.' or ch == '?' or (ch == "\'" and i+1 < len(rowlist) and rowlist[i+1] not in ['t','l','s'] )

def get_train_data(csvname):
    data = ''
    firstlines = []
    with open(csvname,'rt') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # cleans out an odd '?' and ' issue
            rowlist = list(row[0])
            for i, ch in enumerate(rowlist):
                if invalid_char(ch,i,rowlist):
                    rowlist[i] = ' '
            row[0] = ''.join(rowlist)
            data += row[0]
            lines = row[0].split('\n')
            firstlines.append(lines[0])
    return data,firstlines

def create_sequences(corpus,sequence_length,sequence_step):
    corpus = corpus.split()
    sequences, next_words = [], []
    idx = 0
    while idx + sequence_length + 1 < len(corpus):
        sequence = corpus[idx:idx+sequence_length]
        nextword = corpus[idx+sequence_length]
        sequences.append(sequence)
        next_words.append(nextword)
        idx += sequence_step
    return sequences, next_words

def syllable_count(text, lang='en_US'):
    """
    Function to calculate syllable words in a text.
    I/P - a text
    O/P - number of syllable words
    """
    exclude = list(string.punctuation)
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