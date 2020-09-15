from CrashStructure import Bucket, Frame, Stack
from PDM import PositionDependentModel


class CrashBucketizer:

    def __init__(self, buckets, distance_measure, threshold, **hyperParams):
        self.buckets = buckets
        self.distance_measure = distance_measure
        self.threshold = threshold
        self.hyperParams = hyperParams


    def getBuckets(self):
        return self.buckets


    def bucketize(self, newStack):
        if len(newStack) == 0:
            print("No frames available for this crash")
            print(newStack.getRawStackTrace())
            return

        bestBucket = None
        maxSimilarity = -1
        for bucket in self.buckets:
            bucketized_stack = bucket.getCandidateStack()
            if bucketized_stack == None:
                continue
            similarity = self.__getSimilarity(bucketized_stack, newStack)
            if similarity > maxSimilarity:
                maxSimilarity = similarity
                bestBucket = bucket

        if not self.buckets or maxSimilarity < self.threshold:
            newBucket = Bucket(len(self.buckets) + 1)
            newBucket.append(newStack)
            self.buckets.append(newBucket)
        else:
            bestBucket.append(newStack)


    def __getSimilarity(self, stack1, stack2):
        if self.distance_measure == 'PDM':
            pdm = PositionDependentModel(self.hyperParams)
            return pdm.getSimilarity(stack1, stack2)
        elif self.distance_measure == 'WED':
            # TODO: Implement Weighted Edit Distance 
            return -1
        return -1


def main():
    stack1 = Stack(1, "", [Frame("com.company.sampleApp", "ns4::ns5::CrashingClass::crashingMethod()"), Frame("com.company.sampleApp", "ns2::AnotherClass::loremIpsum()"), Frame("com.company.sampleApp", "ns2::AnotherClass::anotherMethod()"), Frame("com.company.sampleApp", "ns2::AnotherClass::randomFunction(std::__1::shared_ptr<foo::SampleClass>)"), Frame("com.company.sampleApp", "ns1::func2(std::__1::shared_ptr<foo::SampleClass>, bool)"), Frame("com.company.sampleApp", "fun1()"), Frame("com.company.sampleApp", "main")])
    stack2 = Stack(2, "", [Frame("com.company.sampleApp", "ns4::ns5::CrashingClass::crashingMethod()"), Frame("com.company.sampleApp", "ns2::AnotherClass::loremIpsum()"), Frame("com.company.sampleApp", "ns2::AnotherClass::anotherMethod()"), Frame("com.company.sampleApp", "ns2::AnotherClass::randomFunction(std::__1::shared_ptr<foo::SampleClass>)"), Frame("com.company.sampleApp", "ns1::func2(std::__1::shared_ptr<foo::SampleClass>, bool)"), Frame("com.company.sampleApp", "fun1()"), Frame("com.company.sampleApp", "main")])
    stack3 = Stack(3, "", [Frame("com.company.sampleApp", "ns4::ns5::CrashingClass::crashingMethod()"), Frame("com.company.sampleApp", "ns2::AnotherClass::loremIpsum()"), Frame("com.company.sampleApp", "ns2::AnotherClass::anotherMethod()"), Frame("com.company.sampleApp", "ns2::AnotherClass::randomFunction0(std::__1::shared_ptr<foo::SampleClass>)"), Frame("com.company.sampleApp", "ns1::func20(std::__1::shared_ptr<foo::SampleClass>, bool)"), Frame("com.company.sampleApp", "fun10()"), Frame("com.company.sampleApp", "main0")])

    bucketizer = CrashBucketizer([], distance_measure='PDM', threshold=0.8, distToTop=0.1, alignOffset=0.1)
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
