import numpy as np
import h5py
import time
import string
from utils import *
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Activation
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from keras.optimizers import RMSprop

#inspiration taken from https://medium.com/@ivanliljeqvist/using-ai-to-generate-lyrics-5aba7950903
MODEL = 'model'
sequence_length = 10
sequence_step = 1
num_epochs = 30

def train_model(sequence_length,chars,X,y):
	# Parameters and training for the model
	model = Sequential()
	model.add(LSTM(512, input_shape=(sequence_length, len(chars))))
	#model.add(LSTM(128, input_shape=(sequence_length, len(chars))))
	model.add(Dense(len(chars)))
	model.add(Dropout(0.2))
	model.add(Activation('softmax'))
	optimizer = RMSprop(lr=0.01)
	model.compile(loss='categorical_crossentropy', optimizer=optimizer)
	# fitting and saving the model
	validatefn = ValidateData()
	model.fit(X, y, batch_size=256, epochs=num_epochs,validation_split=.2,callbacks=[validatefn])
	model.save(MODEL)

def process_data(sequences,next_chars,chars):
	X = np.zeros((len(sequences), sequence_length, len(chars)), dtype=np.bool)
	y = np.zeros((len(sequences), len(chars)), dtype=np.bool)
	for i, sequence in enumerate(sequences):
	    y[i, chars.index(next_chars[i])] = 1
	    for t, char in enumerate(sequence):
	        X[i, t, chars.index(char)] = 1
	return X,y

def main():
	# getting and processing the data
	data, firstlines = get_train_data('haikus.csv')
	#chars is a set of the characters that appear in the data. 
	chars = string.printable
	sequences, next_chars = create_sequences(data, sequence_length, sequence_step)
	# converting data into arrays
	X,y = process_data(sequences,next_chars,chars)
	model = train_model(sequence_length,chars,X,y)

if __name__ == '__main__':
	main()