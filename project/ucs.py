import shell
import util
import wordsegUtil

class GeneratePoemProblem(util.SearchProblem):
    def __init__(self,firstline):
    	self.firstline = firstline
    def startState(self):
    	pass
    def isEnd(self, state):
    	pass
    def succAndCost(self, state):
    	pass


def generatePoem(firstline):
    if len(firstline) == 0:
        return ''
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(GeneratePoemProblem(firstline))
    return ' '.join(ucs.actions)
