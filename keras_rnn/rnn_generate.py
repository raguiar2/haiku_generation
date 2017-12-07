#Code to generate poems. Enter with an optional argument for number of poems.

# for example, python rnn_generate.py 3 creates 3 poems

import keras.models
import random
import sys
import string
import numpy as np
from rnn_train import MODEL, sequence_length
from utils import *


def create_poem(firstlines,model,data,words):
	prevline = random.sample(firstlines,1)[0]
	print(prevline)
	prevline = prevline.split()
	prevline = prevline[-sequence_length:]
	# one index for clarity
	numlines = 1
	currline = []
	while numlines < 3:
		if numlines == 1:
			line_syllable_count = 7
		else:
			line_syllable_count = 5
		x = np.zeros((1,sequence_length, len(words)))
		for i, word in enumerate(prevline):
			x[0,i,words.index(word)] = 1
		#sample highest prob one. with some diversity
		prediction = model.predict(x,verbose=0)[0]
		# TODO: Edit this to be more diverse?
		next_index = sample(prediction,temperature=.4)
		next_word = words[next_index]
		currline.append(next_word)
		if syllable_count(' '.join(currline)) >= line_syllable_count:
			print(' '.join(currline))
			numlines += 1
			currline = []
		# loop to next word in sentence. 
		prevline.append(next_word)
		if len(prevline) > sequence_length:
			prevline = prevline[1:]




def main():
	num_poems = 1
	if len(sys.argv) >=2:
		num_poems = int(sys.argv[1])
	model = keras.models.load_model(MODEL)
	data, firstlines = get_train_data('haikus.csv')
	# list of words in the data
	words = sorted(list(set(data.split())))
	data = data[3*len(data)//4:]
	# make sure first line is of appropriate length
	#firstlines = [line for line in firstlines if len(line.split())==sequence_length]
	for _ in range(num_poems):
		create_poem(firstlines,model,data,words)
		print('')


if __name__ == '__main__':
	main()