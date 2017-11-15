
import heapq, collections, re, sys, time, os, random, string

############################################################
# Abstract interfaces for search problems and search algorithms.

class SearchProblem:
    # Return the start state.
    def startState(self): raise NotImplementedError("Override me")

    # Return whether |state| is an end state or not.
    def isEnd(self, state): raise NotImplementedError("Override me")

    # Return a list of (action, newState, cost) tuples corresponding to edges
    # coming out of |state|.
    def succAndCost(self, state): raise NotImplementedError("Override me")

class SearchAlgorithm:
    # First, call solve on the desired SearchProblem |problem|.
    # Then it should set two things:
    # - self.actions: list of actions that takes one from the start state to an end
    #                 state; if no action sequence exists, set it to None.
    # - self.totalCost: the sum of the costs along the path or None if no valid
    #                   action sequence exists.
    def solve(self, problem): raise NotImplementedError("Override me")

############################################################
# Uniform cost search algorithm (Dijkstra's algorithm).

class UniformCostSearch(SearchAlgorithm):
    def __init__(self, verbose=0):
        self.verbose = verbose

    def solve(self, problem):
        # If a path exists, set |actions| and |totalCost| accordingly.
        # Otherwise, leave them as None.
        self.actions = None
        self.totalCost = None
        self.numStatesExplored = 0

        # Initialize data structures
        frontier = PriorityQueue()  # Explored states are maintained by the frontier.
        backpointers = {}  # map state to (action, previous state)

        # Add the start state
        startState = problem.startState()
        frontier.update(startState, 0)

        while True:
            # Remove the state from the queue with the lowest pastCost
            # (priority).
            state, pastCost = frontier.removeMin()
            if state == None: break
            self.numStatesExplored += 1
            if self.verbose >= 2:
                print "Exploring %s with pastCost %s" % (state, pastCost)

            # Check if we've reached an end state; if so, extract solution.
            if problem.isEnd(state):
                self.actions = []
                while state != startState:
                    action, prevState = backpointers[state]
                    self.actions.append(action)
                    state = prevState
                self.actions.reverse()
                self.totalCost = pastCost
                if self.verbose >= 1:
                    print "numStatesExplored = %d" % self.numStatesExplored
                    print "totalCost = %s" % self.totalCost
                    print "actions = %s" % self.actions
                return

            # Expand from |state| to new successor states,
            # updating the frontier with each newState.
            for action, newState, cost in problem.succAndCost(state):
                if self.verbose >= 3:
                    print "  Action %s => %s with cost %s + %s" % (action, newState, pastCost, cost)
                if frontier.update(newState, pastCost + cost):
                    # Found better way to go to |newState|, update backpointer.
                    backpointers[newState] = (action, state)
        if self.verbose >= 1:
            print "No path found"

# Data structure for supporting uniform cost search.
class PriorityQueue:
    def  __init__(self):
        self.DONE = -100000
        self.heap = []
        self.priorities = {}  # Map from state to priority

    # Insert |state| into the heap with priority |newPriority| if
    # |state| isn't in the heap or |newPriority| is smaller than the existing
    # priority.
    # Return whether the priority queue was updated.
    def update(self, state, newPriority):
        oldPriority = self.priorities.get(state)
        if oldPriority == None or newPriority < oldPriority:
            self.priorities[state] = newPriority
            heapq.heappush(self.heap, (newPriority, state))
            return True
        return False

    # Returns (state with minimum priority, priority)
    # or (None, None) if the priority queue is empty.
    def removeMin(self):
        while len(self.heap) > 0:
            priority, state = heapq.heappop(self.heap)
            if self.priorities[state] == self.DONE: continue  # Outdated priority, skip
            self.priorities[state] = self.DONE
            return (state, priority)
        return (None, None) # Nothing left...

############################################################
# Simple examples of search problems to test your code for Problem 1.

# A simple search problem on the number line:
# Start at 0, want to go to 10, costs 1 to move left, 2 to move right.
class NumberLineSearchProblem:
    def startState(self): return 0
    def isEnd(self, state): return state == 10
    def succAndCost(self, state): return [('West', state-1, 1), ('East', state+1, 2)]

# A simple search problem on a square grid:
# Start at init position, want to go to (0, 0)
# cost 2 to move up/left, 1 to move down/right
class GridSearchProblem(SearchProblem):
    def __init__(self, size, x, y): self.size, self.start = size, (x,y)
    def startState(self): return self.start
    def isEnd(self, state): return state == (0, 0)
    def succAndCost(self, state):
        x, y = state
        results = []
        if x-1 >= 0: results.append(('North', (x-1, y), 2))
        if x+1 < self.size: results.append(('South', (x+1, y), 1))
        if y-1 >= 0: results.append(('West', (x, y-1), 2))
        if y+1 < self.size: results.append(('East', (x, y+1), 1))
        return results


# class to clear and write poems to a file.
class PoemGenerator():
    def __init__(self,filename="baseline.txt"):
        self.filename = filename
    # writes a poem to the baseline.txt file
    def write_poem(self,poem):
        # the 'a' flag says to append, rather than to overwrite the file
        with open(self.filename,'a') as txtfile:
            txtfile.write(poem)
            txtfile.write('\n\n')

    # clears the entire baseline file so new poems can be written
    def clear_baseline_file(self):
        with open(self.filename,'w') as txtfile:
            txtfile.write('Poems are seven lines each, delimited by the line breaks')
            txtfile.write('\n\n')


def evaluatePredictor(examples, predictor):
    '''
    predictor: a function that takes an x and returns a predicted y.
    Given a list of examples (x, y), makes predictions based on |predict| and returns the fraction
    of misclassiied examples.
    '''
    difference = 0
    for x, y in examples:
        guess = predictor(x) 
        difference += abs(guess - y)
        #print(guess,y)
    print('avg distance from similarity is {}'.format(difference/len(examples)))
    return difference

def outputWeights(weights, path):
    print "%d weights" % len(weights)
    out = open(path, 'w')
    for f, v in sorted(weights.items(), key=lambda (f, v) : -v):
        print >>out, '\t'.join([f, str(v)])
    out.close()

def verbosePredict(phi, y, weights, out):
    yy = 1 if dotProduct(phi, weights) > 0 else -1
    if y:
        print >>out, 'Truth: %s, Prediction: %s [%s]' % (y, yy, 'CORRECT' if y == yy else 'WRONG')
    else:
        print >>out, 'Prediction:', yy
    for f, v in sorted(phi.items(), key=lambda (f, v) : -v * weights.get(f, 0)):
        w = weights.get(f, 0)
        print >>out, "%-30s%s * %s = %s" % (f, v, w, v * w)
    return yy

def outputErrorAnalysis(examples, featureExtractor, weights, path):
    out = open('error-analysis', 'w')
    for x, y in examples:
        print >>out, '===', x
        verbosePredict(featureExtractor(x), y, weights, out)
    out.close()

def interactivePrompt(featureExtractor, weights):
    while True:
        print '> ',
        x = sys.stdin.readline()
        if not x: break
        phi = featureExtractor(x) 
        verbosePredict(phi, None, weights, sys.stdout)
# citation: https://www.sitepoint.com/community/t/printing-the-number-of-syllables-in-a-word/206809
def get_syllables_in_word(word):
    syllables = 0
    if all([ch in string.punctuation or ch == ' ' for ch in word ]):
        return 0
    for i in range(len(word)) :
       if word[i] in string.punctuation:
          continue
       # If the first letter in the word is a vowel then it is a syllable.
       if i == 0 and word[i] in "aeiouy" :
          syllables = syllables + 1
       # Else if the previous letter is not a vowel.
       elif word[i - 1] not in "aeiouy" :
          # If it is no the last letter in the word and it is a vowel.
          if i < len(word) - 1 and word[i] in "aeiouy" :
             syllables = syllables + 1
          # Else if it is the last letter and it is a vowel that is not e.
          elif i == len(word) - 1 and word[i] in "aiouy" :
             syllables = syllables + 1
    # Adjust syllables from 0 to 1.
    if len(word) > 0 and syllables == 0:
       syllables == 0
       syllables = 1
    return syllables

