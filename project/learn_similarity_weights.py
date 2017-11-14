# stochastic gradient descent
import collections
import gensim, logging
import pickle
import wordsegUtil
import math
import os
import json
from pathlib import Path
from util import *
CORPUS = 'poet_parsing/corpus.txt'

def read_lines():
    examples = []
    with open(CORPUS) as corpus:
        for line in corpus.readlines():
            examples.append(line.split())
    return examples

def parse_examples(lines,model):
    examples = []
    for line in lines:
        if len(line) < 2:
            continue
        #todo: add score of ans here as word2vec? 
        similarity = model.similarity(line[-1],line[-2])
        examples.append((line[:-1],similarity))
    return examples

def dotProduct(d1, d2):
    """
    @param dict d1: a feature vector represented by a mapping from a feature (string) to a weight (float).
    @param dict d2: same as d1
    @return float: the dot product between d1 and d2
    """
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(d1.get(f, 0) * v for f, v in d2.items())

def increment(d1, scale, d2):
    """
    Implements d1 += scale * d2 for sparse vectors.
    @param dict d1: the feature vector which is mutated.
    @param float scale
    @param dict d2: a feature vector.
    """
    for f, v in d2.items():
        d1[f] = d1.get(f, 0) + v * scale

# should compare word2vec similarity between predicted answer word
# and model difference between the two 
def least_squares_loss(y,weights, features,model):
    margin = dotProduct(weights,features)-y
    #print('dot product is {}'.format(margin))
    #print('similarity is {}'.format(y))
    if math.isnan(margin):
        raise ValueError
    # increment function so we have a decrease here
    return {feature:2*margin*features[feature] for feature in features}


# Given a poem, returns a features vector about the poem 
def featureExtractor(poem,unigramCost,bigramCost):
    features = collections.defaultdict(float)
    features['line_length'] += len(poem)
    if len(poem) >= 1:
        features['unigram_cost'] += unigramCost(poem[-1])
        features[poem[-1]] += 1
    for word in poem:
        features[word] += 1
    if len(poem) >= 2:
        features['bigram'] += bigramCost(poem[-1],poem[-2])
    #standardization
    for feature in features:
        features[feature] = features[feature] / len(features)
    return features

def learn_weights(trainExamples, testExamples, featureExtractor, numIters, eta,model,unigramCost,bigramCost):
    #initalize as 0's
    weights = collections.defaultdict(int)  # feature => weight
    for i in range(numIters):
        for poem, answer in trainExamples:
            features = featureExtractor(poem,unigramCost,bigramCost)
            lossvec = least_squares_loss(answer, weights, features,model)
            #print(lossvec)
            increment(weights,-1*eta,lossvec)
        #print training, test error
        # trainerror = evaluatePredictor(trainExamples,lambda x: 1 if dotProduct(weights,featureExtractor(x)) > 0 else -1)
        testerror = evaluatePredictor(testExamples,lambda x: dotProduct(weights,featureExtractor(x)))
        print('iteration {} completed'.format(i))
        print('Sum of differences in test data = {}'.format(testerror))

    return weights

# learns weights for a predicted similarity function. Used to get similar words 
def main():
    print('training language model...')
    unigramCost , bigramCost = wordsegUtil.makeLanguageModels(CORPUS)
    print('language model trained!')
    print('reading in lines...')
    lines = read_lines()
    print('read in lines!')
    traininglines = lines[:4*len(lines)/5]
    # 80-20 training split
    model_file = Path("poetmodel")
    if model_file.is_file():
        print('reading in existing model for word2vec')
        model = gensim.models.Word2Vec.load('poetmodel')
    else:
        print('training word2vec model...')
        model = gensim.models.Word2Vec(lines, min_count=1)
        print('word2vec model trained!')
        model.save('poetmodel')
    print('generating training examples...')
    train_ex = parse_examples(traininglines,model)
    print('training examples generated!')
    print('generating test examples...')
    testlines = lines[4*len(lines)/5:]
    test_ex = parse_examples(testlines,model)
    print('test examples generated!')
    weights = learn_weights(train_ex,test_ex,featureExtractor,1,.007,model,unigramCost,bigramCost)
    #write weights to file. 
    filename = 'weights.txt'
    with open(filename,'w') as f:
        f.write(json.dumps(weights))
        




if __name__ == '__main__':
    main()