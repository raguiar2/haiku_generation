
# This file scrapes the first line of each poem and writes it to first_lines.txt
import os
import random
import collections
import string
from generate_poems import get_syllables_in_word
CORPUS = 'poet_parsing/corpus.txt'



def write_first_line(file,printable):
	lines = file.readlines()
	for i, line in enumerate(lines):
		#split by spaces after edit
		poem = line.split('\t')
		#makes sure poorly formatted ones are filtered out
		if len(poem) == 3:
			firstline = poem[0]
			syllable_count = sum([get_syllables_in_word(word)[0] for word in firstline.split()])
			if syllable_count == 5:
				with open("first_lines.txt",'a') as first_lines:
					first_lines.write(firstline+'\n')

def write_to_firstlines(printable):
	# for file in os.listdir(POEMS_DIR):
	# # skip hidden files
	# 	if file[0] == '.':
	# 		continue
	# 	filepath = POEMS_DIR+'/'+file
	# 	with open(filepath) as file:
	with open(CORPUS) as f:
		write_first_line(f,printable)

def main(clear_file = True):
	with  open('first_lines.txt', 'w') as f:
		f.write('')
	printable = set(string.printable)
	write_to_firstlines(printable)

if __name__ == "__main__":
	main()