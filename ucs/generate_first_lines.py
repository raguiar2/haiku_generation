
# This file scrapes the first line of each poem and writes it to first_lines.txt
import os
import random
import collections
import string
import csv
from generate_poems import get_syllables_in_word
from util import *
CORPUS = 'poet_parsing/haikus.csv'


def write_first_lines(firstlines):
	for i, firstline in enumerate(firstlines):
		with open("first_lines.txt",'a') as first_lines:
			first_lines.write(firstline)
			if i != len(firstlines) - 1:
				first_lines.write('\n')

def write_to_firstlines(printable):
	data, firstlines = get_train_data(CORPUS)
	write_first_lines(firstlines)

def main(clear_file = True):
	with  open('first_lines.txt', 'w') as f:
		f.write('')
	printable = set(string.printable)
	write_to_firstlines(printable)

if __name__ == "__main__":
	main()