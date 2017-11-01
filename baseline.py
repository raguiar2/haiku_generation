import os
import random
import collections
import string
POEMS_DIR = 'dickinson_parsing/poems'
NUM_POEMS = 5
# TODO: pass these in as arguments to sys, or look at syllable count?
LINE_COUNT = 7
SHORT_LINE_WORDS = 4
LONG_LINE_INCREASE = 2
# zero indexed short lines. 
SHORT_LINES = set([0,2])

# writes a poem to the baseline.txt file
def write_poem(poem):
	# the 'a' flag says to append, rather than to overwrite the file
	with open('baseline.txt','a') as txtfile:
		txtfile.write(poem)
		txtfile.write('\n\n')

# clears the entire baseline file so new poems can be written
def clear_baseline_file():
	with open('baseline.txt','w') as txtfile:
		txtfile.write('Poems are seven lines each, delimited by the line breaks')
		txtfile.write('\n\n')


# Generates a (tanka) poem by going through the lines and 
# putting words in randomly from the words list
def generate_poem(words):
	poem = []
	for linenum in range(LINE_COUNT):
		line = []
		linewords = SHORT_LINE_WORDS
		if linenum not in SHORT_LINES:
			linewords += LONG_LINE_INCREASE
		for wordidx in range(linewords):
			word = random.choice(words)
			line.append(word)
		poem.append(' '.join(line))
	return '\n'.join(poem)

# driver code to generate, print and write poem. 
def generate_poems(words):
	clear_baseline_file()
	for poemidx in range(NUM_POEMS):
		print('\n')
		print('Poem {}:'.format(poemidx+1))
		poem = generate_poem(words)
		write_poem(poem)
		print(poem)
		print('\n')

# reads in one poem and updates the freq defaultdict
def read_poem(file,words,printable):
	lines = file.readlines()
	for line in lines:
		for word in line.split():
			# TODO: This could handle quotes/hyphens better
			# word.translate strips punctuation
			word = word.strip()
			word = word.translate(None, string.punctuation)
			# strips unicode characters out. This was causing some weird
			# spacing in the generated poems. 
			word = ''.join(list(filter(lambda x: x in printable, word)))
			words.append(word)


# Reads in all the poems and stores all of the words in the 
# words list. Then returns the words list for use in 
# poem generation. 
def read_poems(printable):
	words = []
	for file in os.listdir(POEMS_DIR):
		# skip hidden files
		if file[0] == '.':
			continue
		filepath = POEMS_DIR+'/'+file
		with open(filepath) as file:
			read_poem(file,words,printable)
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
	print('Generating poems...')
	generate_poems(words)
	print('Poems generated! look in baseline.txt for the poems')


if __name__ == '__main__':
	main()