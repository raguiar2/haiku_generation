
# This file contains the driver (shell) code to generate our poems and 
# write them to poems.txt
import sys
import random
import string
import util
from util import PoemGenerator
from ucs import GeneratePoemProblem
import os 
import wordsegUtil

NUM_POEMS = 1
POEMS_DIR = 'poet_parsing/poems'
CORPUS = 'poet_parsing/corpus.txt'

# reads in one poem and updates the freq defaultdict
def read_poem(file,words,printable):
	lines = file.readlines()
	for line in lines:
		for word in line.split():
			if word in words:
				continue
			# TODO: This could handle quotes/hyphens better
			# word.translate strips punctuation
			word = word.strip()
			word = word.translate(None, string.punctuation)
			# strips unicode characters out. This was causing some weird
			# spacing in the generated poems. 
			word = ''.join(list(filter(lambda x: x in printable, word)))
			words.add(word)


def read_corpus():
	words = set()
	for file in os.listdir(POEMS_DIR):
		# skip hidden files
		if file[0] == '.':
			continue
		filepath = POEMS_DIR+'/'+file
		with open(filepath) as file:
			#print('reading in file {}...'.format(filepath))
			read_poem(file,words,string.printable)
	return words




def generate_poem(firstline):
    if len(firstline) == 0:
        return ''
    firstline = firstline.split()
    ucs = util.UniformCostSearch(verbose=0)
    words = read_corpus()
    print('training cost functions....')
    unigramCost , bigramCost = wordsegUtil.makeLanguageModels(CORPUS)
    print('cost functions trained!')
    lines = []
    for linenum in range(random.randint(8,12)):
    	ucs.solve(GeneratePoemProblem(firstline,words, unigramCost,bigramCost)) #todo: learn cost function and add it as second param.
    	line = ' '.join(ucs.actions)
    	lines.append(line)
    	print(line)
    return '\n'.join(lines)


# only one argument for now. If the user specifies the -l flag
# then use that as the first line. Otherwise, use a random
# dickinson first line as the first line of the poem
def get_args():
	# no argument, just choose a random first line
	# from first_lines.txt
	if len(sys.argv) == 1:
		with open('first_lines.txt') as lines:
			firstlines = lines.readlines()
			return random.choice(firstlines)
	elif len(sys.argv) == 2:
		firstline = sys.argv[1]
		return firstline
	# invalid otherwise
	else:
		raise Exception("Please only specify one argument")



def main():
	firstline = get_args()
	poemgenerator = PoemGenerator("poems.txt")
	poemgenerator.clear_baseline_file()
	for i in range(NUM_POEMS):
		poem = generate_poem(firstline)
		print("Poem number {}:".format(i+1))
		print(firstline + '\n' + poem)
		poemgenerator.write_poem(poem)

if __name__=='__main__':
	main()