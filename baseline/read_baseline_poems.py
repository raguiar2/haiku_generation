
# This file reads in all of Emily Dickinson's poems and puts them into one large corpus. 

import os
import random
import collections
import string
from wordsegUtil import get_train_data
CORPUS = 'haikus.csv'
# zero indexed short lines. 

# reads in one poem and updates the freq defaultdict
def read_poem(line,words,printable):
	for word in line.split():
		words.append(word)


# Reads in all the poems and stores all of the words in the 
# words list. Then returns the words list for use in 
# poem generation. 
def read_poems(printable):
	words = []
	data, firstlines = get_train_data(CORPUS)
	with open('first_lines.txt','w') as f:
		for i, firstline in enumerate(firstlines):
			f.write(firstline)
			if i != len(firstlines) - 1:
				f.write('\n')
	data = data.split()
	for line in data:
		read_poem(line,words,printable)
	return words

# Driver code. Opens directory, and makes 
# helper calls to read in file and generate poems
def main():
	#ASCII characters for unicode filter
	printable = set(string.printable)
	# goes through poems directory. 
	print('Reading in poems...')
	words = read_poems(printable)
	print('Poems read!')


if __name__ == '__main__':
	main()