# This file reads in all of the poems from the file "other_poets" 
# and puts them into one large corpus called "all_other_poems.txt". 

import os
import random
import collections
import string
POEMS_DIR = 'other_poets'

def read_poem(file):
    lines = file.readlines()
    contentsFound = False
    with open('all_other_poems.txt','a') as txtfile:
        for line in lines:
            fixedtext = ""
            # delete line numbers
            for char in line:
                if char.isdigit():
                    continue
                else:
                    fixedtext += char
            # strip EOL. 
            fixedtext = fixedtext.strip()
            # write to txt file
            # only obtain text after contents tag
            if fixedtext == "CONTENTS.":
                print('CONTENTS. Found')
                contentsFound = True
            if contentsFound == True:
                txtfile.write(fixedtext.lower() + '\n')

def read_poems():
    with open('all_other_poems.txt', 'w') as txtfile:
        txtfile.write('All other poems filtered. Used as a corpus')
        txtfile.write('\n\n')
	for file in os.listdir(POEMS_DIR):
		# skip hidden files
		if file[0] == '.':
			continue
		filepath = POEMS_DIR+'/'+file
		with open(filepath) as file:
			read_poem(file)

def main():
    print('Reading in poems...')
    read_poems()
    print('Poems read!')


if __name__ == "__main__":
	main()
