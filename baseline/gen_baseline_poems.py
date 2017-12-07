
# This file generates the baseline poems using a greedy approach and bigram costs. 

import wordsegUtil
import curses 
import nltk
from read_baseline_poems import * 
from wordsegUtil import get_train_data
from curses.ascii import isdigit 
from nltk.corpus import cmudict 
d = cmudict.dict()
CORPUS = 'poet_parsing/haikus.csv'
NUM_POEMS = 3
SYLLABLES = 5
LONG_LINE_INCREASE = 2
SHORT_LINES = set([1])



# writes a poem to the baseline.txt file
def write_poem(poem, filename="baseline.txt"):
	# the 'a' flag says to append, rather than to overwrite the file
	with open(filename,'a') as txtfile:
		txtfile.write(poem)
		txtfile.write('\n\n')

# clears the entire baseline file so new poems can be written
def clear_baseline_file(baseline_file = "baseline.txt"):
	with open(baseline_file,'w') as txtfile:
		txtfile.write('Poems are three lines each, delimited by the line breaks')
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

# citation: https://www.sitepoint.com/community/t/printing-the-number-of-syllables-in-a-word/206809
def get_syllables_in_word(word):
    #error case, do not include
    if word not in d:
        return [float('inf')]
    return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]

# Generates a (haiku) poem by going through the lines and 
# putting words in greedily from the words list
def generate_poem(bigramCost,words,firstline):
	poem = [firstline]
	prevword = firstline.split()[-1]
	for linenum in range(2):
		line = []
		# long vs short line
		total_syllables = SYLLABLES
		if linenum not in SHORT_LINES:
			total_syllables += LONG_LINE_INCREASE
		while total_syllables > 0: 
			# generate the poem here. 
			newords = [word for word in words if get_syllables_in_word(word)[0] <= total_syllables]
			if prevword == wordsegUtil.SENTENCE_BEGIN:
				word = random.choice(list(words))
			else:
				word = get_min_word(bigramCost,newords,prevword)
			line.append(word)
			total_syllables -= get_syllables_in_word(word)[0]
			prevword = word
			words.remove(prevword)
		poem.append(' '.join(line))
	return poem[0]+ poem[1] + '\n' + poem[2]
 
def read_random_first_line(firstlines):
	with open(firstlines) as f:
		lines = f.readlines()
	return random.choice(lines)
# driver code to generate, print and write poem. 
def generate_poems():
	clear_baseline_file()
	# Also returns an unused unigram cost. 
	data, firstlines = get_train_data(CORPUS)
	data = data.split()
	_ , bigramCost = wordsegUtil.makeLanguageModels(data)
	words = set(read_poems(set(string.printable)))
	for poemidx in range(NUM_POEMS):
		firstline = read_random_first_line('first_lines.txt')
		print('\n')
		print('Poem {}:'.format(poemidx+1))
		poem = generate_poem(bigramCost,words,firstline)
		write_poem(poem)
		print(poem)
		print('\n')

def main():
	print('Generating poems...')
	generate_poems()
	print('Poems generated! look in baseline.txt for the poems')



if __name__ == '__main__':
	main()