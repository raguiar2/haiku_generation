
# This file contains the driver (shell) code to generate our poems and 
# write them to poems.txt
import sys
import random
import string
import util
import os 
import json
import wordsegUtil
import collections
import gensim, logging
from learn_similarity_weights import featureExtractor
from pathlib import Path
from util import get_syllables_in_word
from ucs import GeneratePoemProblem



NUM_POEMS = 5
POEMS_DIR = 'poet_parsing/poems'
CORPUS = 'poet_parsing/corpus.txt'
    

# function to write similarities to similarities.txt
# shouldn't be called too often because it takes a while to do. 
def get_word_similarities(words):
    model_file = Path("poetmodel")
    if model_file.is_file():
        print('reading in existing model for word2vec')
        model = gensim.models.Word2Vec.load('poetmodel')
    else:
        print('training word2vec model...')
        model = gensim.models.Word2Vec(lines, min_count=1)
        print('word2vec model trained!')
        model.save('poetmodel')
    similaritydict = collections.defaultdict(list)
    print('getting similarities...')
    index = 0
    for word in words:
        for word2 in words:
            similaritydict[word].append((word2,model.similarity(word,word2)))
        print('iteration {} complete'.format(index))
        index += 1
    print('similarities learned!')
    # sort similarities by value
    for key,value in similaritydict.items():
        similaritydict[key].sort(key = lambda x: x[1])
    with open('similarities.txt','w') as f:
        f.write(json.dumps(similaritydict))
    return similaritydict

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
    with open(CORPUS) as corpus:
        for line in corpus.readlines():
            for word in line.split():
                words.add(word)
    return words


def generate_poem(firstline,unigramCost,bigramCost):
    if len(firstline) == 0:
        return ''
    firstline = firstline.split()
    ucs = util.UniformCostSearch(verbose=0)
    words = read_corpus()
    lines = []
    similaritydict = collections.defaultdict(list)
    #similaritydict = json.load(open('similarities.txt'))
    weights = json.load(open('weights.txt'))
    for linenum in range(2):
        max_syllables = 5 if linenum%2==1 else 7
        ucs.solve(GeneratePoemProblem(firstline,words,weights,
        featureExtractor,similaritydict,unigramCost,bigramCost,max_syllables))
        line = ' '.join(ucs.actions)
        lines.append(line)
        firstline = ucs.actions
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
    # words = read_corpus()
    # similaritydict = get_word_similarities(words)
    poemgenerator = util.PoemGenerator("poems.txt")
    poemgenerator.clear_baseline_file()
    print('training cost functions....')
    unigramCost , bigramCost = wordsegUtil.makeLanguageModels(CORPUS)
    print('cost functions trained!')
    for i in range(NUM_POEMS):
        print('getting first line')
        firstline = get_args()
        poem = generate_poem(firstline,unigramCost,bigramCost)
        print("Poem number {}:".format(i+1))
        print(firstline + poem)
        poemgenerator.write_poem(firstline + poem)

if __name__=='__main__':
    main()