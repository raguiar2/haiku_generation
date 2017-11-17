
# This file generates the baseline poems using a greedy approach and bigram costs. 

import wordsegUtil
import pronouncing
from read_baseline_poems import * 
CORPUS = 'poet_parsing/corpus.txt'
NUM_POEMS = 3
SYLLABLES = 5
LONG_LINE_INCREASE = 2
SHORT_LINES = set([0,2])



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
	syllables = 0
	for i in range(len(word)) :
	   # If the first letter in the word is a vowel then it is a syllable.
	   if i == 0 and word[i] in "aeiouy" :
	      syllables = syllables + 1
	   # Else if the previous letter is not a vowel.
	   elif word[i - 1] not in "aeiouy" :
	      # If it is no the last letter in the word and it is a vowel.
	      if i < len(word) - 1 and word[i] in "aeiouy" :
	         syllables = syllables + 1
	      # Else if it is the last letter and it is a vowel that is not e.
	      elif i == len(word) - 1 and word[i] in "aiouy" :
	         syllables = syllables + 1
	# Adjust syllables from 0 to 1.
	if len(word) > 0 and syllables == 0 :
	   syllables == 0
	   syllables = 1

	return syllables


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
			newords = [word for word in words if get_syllables_in_word(word) <= total_syllables]
			if prevword == wordsegUtil.SENTENCE_BEGIN:
				word = random.choice(list(words))
			else:
				word = get_min_word(bigramCost,newords,prevword)
			line.append(word)
			# keep syllable count
			# phones = pronouncing.phones_for_word(word)
			# print(phones)
			# syllcount = pronouncing.syllable_count(phones)
			# print(syllcount)
			total_syllables -= get_syllables_in_word(word)
			prevword = word
			words.remove(prevword)
		poem.append(' '.join(line))
	return '\n'.join(poem)

def read_random_first_line(firstlines):
	with open(firstlines) as f:
		lines = f.readlines()
	return random.choice(lines)
# driver code to generate, print and write poem. 
def generate_poems():
	clear_baseline_file()
	# Also returns an unused unigram cost. 
	_ , bigramCost = wordsegUtil.makeLanguageModels(CORPUS)
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