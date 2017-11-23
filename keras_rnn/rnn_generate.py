import keras.models
import random
import sys
import string
import numpy as np
from rnn_train import MODEL, sequence_length
from utils import *

def main():
	model = keras.models.load_model(MODEL)
	data, firstlines = get_train_data('haikus.csv')
	chars = string.printable
	# make sure first line is of appropriate length
	firstlines = [line for line in firstlines if len(line)==sequence_length]
	firstline = random.sample(firstlines,1)[0]+'\n'
	sys.stdout.write(firstline)
	sys.stdout.flush()
	firstline = firstline[-sequence_length:]
	# one index for clarity
	numlines = 1
	currline = ''
	while numlines < 3:
		x = np.zeros((1, sequence_length, len(chars)))
		for i, char in enumerate(firstline):
			x[0,i,chars.index(char)] = 1
		#sample highest prob one. 
		prediction = model.predict(x,verbose=0)[0]
		# TODO: Edit this to be more diverse?
		next_index = sample(prediction,temperature=.4)
		#print(prediction,prediction[next_index])
		next_char = chars[next_index]
		currline += next_char
		if next_char == '\n':
			sys.stdout.write(currline)
			sys.stdout.flush()
			currline = ''
			numlines += 1
		firstline = firstline[1:]+next_char
if __name__ == '__main__':
	main()