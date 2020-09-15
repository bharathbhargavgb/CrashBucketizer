import math


class PositionDependentModel:

    def __init__(self, hyperParams):
        self.distToTopCoeff = 0.0
        self.alignOffsetCoeff = 0.0
        if 'distToTop' in hyperParams:
            self.distToTopCoeff = hyperParams['distToTop']
        if 'alignOffset' in hyperParams:
            self.alignOffsetCoeff = hyperParams['alignOffset']


    def getSimilarity(self, stack1, stack2):
        stack1Len = len(stack1)
        stack2Len = len(stack2)

        scoreTable = [[0. for i in range(stack2Len + 1)] for j in range(stack1Len + 1)]
        for i in range(1, stack1Len + 1):
            for j in range(1, stack2Len + 1):
                score = 0.
                if stack1.frames[i-1].method == stack2.frames[j-1].method:
                    score = math.e ** (-self.distToTopCoeff * min(i-1, j-1)) * math.e ** (-self.alignOffsetCoeff * abs(i-j))
                scoreTable[i][j] = max(scoreTable[i-1][j-1] + score, scoreTable[i-1][j], scoreTable[i][j-1])

        sig = 0.
        for i in range(min(stack1Len, stack2Len)):
            sig += math.e ** (-self.distToTopCoeff * i)

        similarity = scoreTable[stack1Len][stack2Len] / sig
        return similarity