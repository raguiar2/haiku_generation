import util
import wordsegUtil
import random

class GeneratePoemProblem(util.SearchProblem):
    def __init__(self,firstline,words,unigramCost,bigramCost):
        self.prevword = firstline[-1]
        self.linewords = 0
        self.numiter = 0
        # fix this to something more complicated? 
        self.words = words
        self.unigramCost = unigramCost
        self.bigramCost = bigramCost
        self.wordsperline = 5
    def startState(self):
    	return (self.prevword, "",self.linewords)
    def isEnd(self, state):
        prevword, currline, linewords = state
    	return linewords == self.wordsperline
    # Todo: Fix cost function
    def succAndCost(self, state):
    	prevword, currline, linewords = state
        currline = list(currline)
        successors = []
        if len(currline)>=self.wordsperline:
            endlineaction = ("\n",(prevword,"",linewords+1),0) #todo: change cost 
            successors.append(endlineaction)
            return successors
        wordcosts = {}
        for word in random.sample(self.words,50):
            wordcosts[word] = self.bigramCost(prevword,word)
        worditems = wordcosts.items()
        worditems.sort(key = lambda x: x[1])
        lowestcostwords = []
        for i in range(10):
            lowestcostwords.append(worditems[i][0])
        for word in lowestcostwords:
            action = word
            newstate = (prevword,tuple(currline+[word]),linewords+1)
            cost = wordcosts[word]
            successors.append((action,newstate,cost))
        self.numiter += 1

        return successors

