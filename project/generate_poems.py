
# This file contains the driver (shell) code to generate our poems and 
# write them to poems.txt
import sys
import random
import nltk
NUM_POEMS = 1
import sys
from util import PoemGenerator


def generate_poem(firstline):
	return firstline


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
	for _ in range(NUM_POEMS):
		poem = generate_poem(firstline)
		poemgenerator.write_poem(poem)

if __name__=='__main__':
	main()