from stack_optimizer import *
from CrashStructure import Frame


class CrashParser:

    def removeRecursiveCalls(self, stackFrames):
        return removeRepeats(stackFrames)


    def stripUnsymbolicatedFrame(self, frameEntry):
        hexPrefix = '0x'
        if not frameEntry or frameEntry.startswith(hexPrefix):
            return None
        return frameEntry


    def isValidString(self, str):
        if str == None or len(str) <= 0:
            return False
        return True