
# This file generates the baseline poems using a greedy approach and bigram costs. 

import os
import random
import collections
import string
import wordsegUtil
from read_baseline_poems import * 
CORPUS = 'all_poems.txt'
NUM_POEMS = 3




# writes a poem to the baseline.txt file
def write_poem(poem, filename="baseline.txt"):
	# the 'a' flag says to append, rather than to overwrite the file
	with open(filename,'a') as txtfile:
		txtfile.write(poem)
		txtfile.write('\n\n')

# clears the entire baseline file so new poems can be written
def clear_baseline_file(baseline_file = "baseline.txt"):
	with open(baseline_file,'w') as txtfile:
		txtfile.write('Poems are seven lines each, delimited by the line breaks')
		txtfile.write('\n\n')


def get_min_word(bigramCost,words,prev):
	minword , mincost = '', float('inf')
	for word in words:
		cost = bigramCost(prev,word)
		if cost < mincost:
			minword = word
			mincost = cost
			#minword = word
		# with some probability choose a different word. 
		elif cost == mincost:
			prob = random.randint(1,2)
			if prob == 1:
				minword = word
	words.remove(minword)
	return minword

# Generates a (tanka) poem by going through the lines and 
# putting words in greedily from the words list
def generate_poem(bigramCost,words):
	poem = []
	prevword = wordsegUtil.SENTENCE_BEGIN
	for linenum in range(LINE_COUNT):
		line = []
		# long vs short line
		linewords = SHORT_LINE_WORDS
		if linenum not in SHORT_LINES:
			linewords += LONG_LINE_INCREASE
		for wordidx in range(linewords):
			# generate the poem here. 
			if prevword == wordsegUtil.SENTENCE_BEGIN:
				word = random.choice(list(words))
			else:
				word = get_min_word(bigramCost,words,prevword)
			line.append(word)
			prevword = word
		poem.append(' '.join(line))
	return '\n'.join(poem)

# driver code to generate, print and write poem. 
def generate_poems():
	clear_baseline_file()
	# Also returns an unused unigram cost. 
	_ , bigramCost = wordsegUtil.makeLanguageModels(CORPUS)
	words = set(read_poems(set(string.printable)))
	for poemidx in range(NUM_POEMS):
		print('\n')
		print('Poem {}:'.format(poemidx+1))
		poem = generate_poem(bigramCost,words)
		write_poem(poem)
		print(poem)
		print('\n')

def main():
	print('Generating poems...')
	generate_poems()
	print('Poems generated! look in baseline.txt for the poems')



if __name__ == '__main__':
	main()