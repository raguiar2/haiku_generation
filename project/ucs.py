import util
import wordsegUtil
import random

class GeneratePoemProblem(util.SearchProblem):
    def __init__(self,firstline,words,unigramCost,bigramCost):
    	self.prevline = firstline
        self.line = ""
        self.linenum = 2
        # fix this to something more complicated? 
        self.maxlines = 3 #random.randint(8,12)
        self.words = words
        self.unigramCost = unigramCost
        self.bigramCost = bigramCost
        self.wordsperline = 5
    def startState(self):
    	return (tuple(self.prevline),"",2)
    def isEnd(self, state):
        prevline, currline, linenum = state
    	return linenum == self.maxlines
    # Todo: Fix cost function
    def succAndCost(self, state):
    	prevline, currline, linenum = state
        prevline = list(prevline)
        currline = list(currline)
        successors = []
        if len(currline)>=self.wordsperline:
            endlineaction = ("",(tuple(currline),"",linenum+1),0) #todo: change cost 
            successors.append(endlineaction)
            return successors
        wordcosts = {}
        for word in self.words:
            if len(currline) == 0:
                wordcosts[word] = self.unigramCost(word)
            else:
                wordcosts[word] = self.bigramCost(currline[-1],word)
        worditems = wordcosts.items()
        worditems.sort(key = lambda x: x[1])
        lowestcostwords = []
        for i in range(5):
            lowestcostwords.append(worditems[i][0])
        for word in lowestcostwords:
            action = word
            newstate = (tuple(prevline),tuple(currline+[word]),linenum)
            cost = wordcosts[word]
            successors.append((action,newstate,cost))
        return successors

