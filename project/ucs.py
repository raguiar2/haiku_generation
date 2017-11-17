import util
import wordsegUtil
import random
import gensim, logging
from pathlib import Path
from learn_similarity_weights import dotProduct
from heapq import nsmallest
from util import get_syllables_in_word

class GeneratePoemProblem(util.SearchProblem):
    def __init__(self,firstline,words,weights,featureExtractor,similarities,unigramCost,bigramCost, max_syllables):
        print(firstline)
        self.prevword = firstline[-1]
        self.max_syllables = max_syllables
        # fix this to something more complicated? 
        self.words = words
        self.featureExtractor = featureExtractor
        self.weights = weights
        self.similarities = similarities
        self.unigramCost = unigramCost
        self.bigramCost = bigramCost
        model_file = Path("poetmodel")
        if model_file.is_file():
            model = gensim.models.Word2Vec.load('poetmodel')
        else:
            model = gensim.models.Word2Vec(lines, min_count=1)
            model.save('poetmodel')
        self.model = model
    def startState(self):
    	return (self.prevword, "",0)
    def isEnd(self, state):
        prevword, currline, syllables = state
    	return syllables == self.max_syllables
    def _get_k_most_similar(self,words,best_guess,k,allowed_syllables):
        most_similar = []
        # check that we get all k words, or we run out of words. 
        while len(most_similar) < k and len(words) > 0:
            closest = (min(words, key=lambda x:abs(x[1]-best_guess)))
            if get_syllables_in_word(closest[0]) <= allowed_syllables:
                most_similar.append(closest)
            words.remove(closest)
        return most_similar
    def succAndCost(self, state):
    	prevword, currline, syllables = state
        currline = list(currline)
        features = self.featureExtractor(currline,self.unigramCost,self.bigramCost)
        best_guess = dotProduct(features,self.weights)
        successors = []
        if syllables>=self.max_syllables:
            endlineaction = ("\n",(prevword,"",syllables),0) #todo: change cost 
            successors.append(endlineaction)
            return successors
        if prevword not in self.similarities:
            for word in self.words:
                self.similarities[prevword].append((word,self.model.similarity(prevword,word)))
            #self.similarities[prevword].sort()
        most_similar = self._get_k_most_similar(self.similarities[prevword],best_guess,len(self.similarities[prevword]),self.max_syllables-syllables)
        #most_similar = self._get_k_most_similar(self.similarities[prevword],best_guess,10,self.max_syllables-syllables)
        wordcosts = {}
        for pair in most_similar:
            word, similarity = pair
            #cost is the difference between similarities of that word and your best guess. 
            wordcosts[word] = abs(similarity-best_guess)
        for pair in most_similar:
            word = pair[0]
            action = word
            wordsyllabes = get_syllables_in_word(word)
            newstate = (word,tuple(currline+[word]),syllables+wordsyllabes)
            cost = wordcosts[word]
            successors.append((action,newstate,cost))
        return successors

