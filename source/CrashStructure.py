import random


class Frame:
    def __init__(self, module, method):
        self.module = module
        self.method = method

    def __eq__(self, frame):
        if isinstance(frame, Frame):
            return self.module == frame.module and self.method == frame.method
        return False

    def __str__(self):
        return str(self.module) + '\t' + str(self.method)


class Stack:
    def __init__(self, id, stackTrace, frames):
        self.id = id
        self.frames = frames
        self.originalStackTrace = stackTrace

    def __len__(self):
        return len(self.frames)

    def __str__(self):
        stackTrace = ""
        for frame in self.frames:
            stackTrace += str(frame) + '\n'
        return stackTrace

    def getRawStackTrace(self):
        return self.originalStackTrace


class Bucket:
    def __init__(self, id):
        self.id = id
        self.stacks = []

    def __len__(self):
        return len(self.stacks)

    def append(self, crashStack):
        self.stacks.append(crashStack)

    def getCandidateStack(self):
        if not self.stacks:
            return None
        return self.stacks[0]

    def getCandidateStacks(self, count):
        totalStacks = len(self.stacks)
        validCount = min(count, totalStacks)
        if validCount <= 0:
            return None
        sample_indexes = random.sample(range(0, totalStacks), k=validCount)
        candidates = []
        for ind in sample_indexes:
            candidates.append(self.stacks[ind])
        return candidates