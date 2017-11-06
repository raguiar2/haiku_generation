
# This file scrapes the first line of each poem and writes it to first_lines.txt
import os
import random
import collections
import string
POEMS_DIR = 'dickinson_parsing/poems'

def write_first_line(file,printable):
	lines = file.readlines()
	firstline = lines[0]
	with open("first_lines.txt",'a') as first_lines:
		first_lines.write(firstline)

def write_to_firstlines(printable):
	for file in os.listdir(POEMS_DIR):
	# skip hidden files
		if file[0] == '.':
			continue
		filepath = POEMS_DIR+'/'+file
		with open(filepath) as file:
			write_first_line(file,printable)

def main(clear_file = False):
	if clear_file:
		open('first_lines.txt', 'w').close()
	printable = set(string.printable)
	write_to_firstlines(printable)

if __name__ == "__main__":
	main()