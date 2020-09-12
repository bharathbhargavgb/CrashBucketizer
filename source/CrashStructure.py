class Frame:
    def __init__(self, module, method):
        self.module = module
        self.method = method


class Stack:
    def __init__(self, id, frames):
        self.id = id
        self.frames = frames

    def __len__(self):
        return len(self.frames)


class Bucket:
    def __init__(self, id):
        self.id = id
        self.stacks = []

    def append(self, crashStack):
        self.stacks.append(crashStack)

    def getCandidateStack(self):
        if not self.stacks:
            return None
        return self.stacks[0]
