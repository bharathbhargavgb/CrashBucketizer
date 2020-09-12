import math
from CrashStructure import Bucket, Frame, Stack


class CrashBucketizer:
    def __init__(self, buckets):
        self.buckets = buckets


    def getBuckets(self):
        return self.buckets


    def bucketize(self, newStack):
        bestBucket = None
        maxSimilarity = -1
        for bucket in self.buckets:
            bucketized_stack = bucket.getCandidateStack()
            if bucketized_stack == None:
                continue
            similarity = self.getSimilarity(bucketized_stack, newStack)
            if similarity > maxSimilarity:
                maxSimilarity = similarity
                bestBucket = bucket

        if not self.buckets or maxSimilarity < 0.9:
            newBucket = Bucket(len(self.buckets) + 1)
            newBucket.append(newStack)
            self.buckets.append(newBucket)
        else:
            bestBucket.append(newStack)


    def getSimilarity(self, stack1, stack2):
        return self.positionDependentSimilarity(stack1, stack2, 0.3, 0.0)


    def positionDependentSimilarity(self, stack1, stack2, distToTopCoeff, alignOffsetCoeff):
        stack1Len = len(stack1)
        stack2Len = len(stack2)

        scoreTable = [[0. for i in range(stack2Len + 1)] for j in range(stack1Len + 1)]
        for i in range(1, stack1Len + 1):
            for j in range(1, stack2Len + 1):
                score = 0.
                if stack1.frames[i-1].method == stack2.frames[j-1].method:
                    score = math.e ** (-distToTopCoeff * min(i-1, j-1)) * math.e ** (-alignOffsetCoeff * abs(i-j))
                scoreTable[i][j] = max(scoreTable[i-1][j-1] + score, scoreTable[i-1][j], scoreTable[i][j-1])

        sig = 0.
        for i in range(min(stack1Len, stack2Len)):
            sig += math.e ** (-distToTopCoeff * i)

        similarity = scoreTable[stack1Len][stack2Len] / sig
        return similarity



def main():
    stack1 = Stack(1, [Frame("com.company.sampleApp", "ns4::ns5::CrashingClass::crashingMethod()"), Frame("com.company.sampleApp", "ns2::AnotherClass::loremIpsum()"), Frame("com.company.sampleApp", "ns2::AnotherClass::anotherMethod()"), Frame("com.company.sampleApp", "ns2::AnotherClass::randomFunction(std::__1::shared_ptr<foo::SampleClass>)"), Frame("com.company.sampleApp", "ns1::func2(std::__1::shared_ptr<foo::SampleClass>, bool)"), Frame("com.company.sampleApp", "fun1()"), Frame("com.company.sampleApp", "main")])
    stack2 = Stack(2, [Frame("com.company.sampleApp", "ns4::ns5::CrashingClass::crashingMethod()"), Frame("com.company.sampleApp", "ns2::AnotherClass::loremIpsum()"), Frame("com.company.sampleApp", "ns2::AnotherClass::anotherMethod()"), Frame("com.company.sampleApp", "ns2::AnotherClass::randomFunction(std::__1::shared_ptr<foo::SampleClass>)"), Frame("com.company.sampleApp", "ns1::func2(std::__1::shared_ptr<foo::SampleClass>, bool)"), Frame("com.company.sampleApp", "fun1()"), Frame("com.company.sampleApp", "main")])
    stack3 = Stack(3, [Frame("com.company.sampleApp", "ns4::ns5::CrashingClass::crashingMethod()"), Frame("com.company.sampleApp", "ns2::AnotherClass::loremIpsum()"), Frame("com.company.sampleApp", "ns2::AnotherClass::anotherMethod()"), Frame("com.company.sampleApp", "ns2::AnotherClass::randomFunction0(std::__1::shared_ptr<foo::SampleClass>)"), Frame("com.company.sampleApp", "ns1::func20(std::__1::shared_ptr<foo::SampleClass>, bool)"), Frame("com.company.sampleApp", "fun10()"), Frame("com.company.sampleApp", "main0")])

    bucketizer = CrashBucketizer([])
    bucketizer.bucketize(stack1)
    bucketizer.bucketize(stack2)
    bucketizer.bucketize(stack3)

    for bucket in bucketizer.getBuckets():
        print('Bucket ' + str(bucket.id))
        for crash in bucket.stacks:
            print('Crash ' + str(crash.id))
            for frame in crash.frames:
                print(frame.method)
            print('')


if __name__ == "__main__":
    main()
