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
    # BEGIN_YOUR_CODE (our solution is 3 lines of code, but don't worry if you deviate from this)
    if len(firstline) == 0:
        return ''
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(GeneratePoemProblem(firstline))
    return ' '.join(ucs.actions)
    #raise Exception("Not implemented yet")
    # END_YOUR_CODE