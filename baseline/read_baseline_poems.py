
# This file reads in all of Emily Dickinson's poems and puts them into one large corpus. 

import os
import random
import collections
import string
CORPUS = 'poet_parsing/corpus.txt'
# zero indexed short lines. 

# reads in one poem and updates the freq defaultdict
def read_poem(file,words,printable, write_to_all):
	lines = file.readlines()
	# if write_to_all:
	# 	with open('all_poems.txt','a') as txtfile:
	# 		for line in lines:
	# 			txtfile.write(line)
	for poem in lines:
		for line in poem.split('\t'):
			for word in line.split():
				words.append(word)


# Reads in all the poems and stores all of the words in the 
# words list. Then returns the words list for use in 
# poem generation. 
def read_poems(printable, write_to_all = False):
	if write_to_all:
		with open('all_poems.txt','w') as txtfile:
			txtfile.write('All of Emily Dickinsons poems. Used as a corpus')
			txtfile.write('\n\n')
	words = []
	with open(CORPUS) as file:
		read_poem(file,words,printable, write_to_all)
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