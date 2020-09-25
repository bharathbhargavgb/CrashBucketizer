from CrashStructure import Frame
from maximal_repeat.rstr_max import *


def removeRepeats(stackFrames):
    stackFrames = removeGroupRepeats(stackFrames)
    stackFrames = removeAdjacentRepeats(stackFrames)
    return stackFrames


def removeGroupRepeats(stackFrames):
    stackString = convertStackToString(stackFrames)
    rstr = Rstr_max()
    rstr.add_str(stackString)
    repeats = rstr.go()
    stackString = removeMaximalRepeat(rstr, repeats, stackString)
    stackFrames = convertStringToStack(stackString)
    return stackFrames


def removeAdjacentRepeats(stackFrames):
    left = 0
    for right in range(0, len(stackFrames)):
        if stackFrames[left] != stackFrames[right]:
            left += 1
            stackFrames[left] = stackFrames[right]

    return stackFrames[:left+1]


def removeMaximalRepeat(rstr, repeats, stackString):
    max_count = 0
    max_indexes = None
    for (offset_end, nb), (l, start_plage) in repeats.items():
        ss = rstr.global_suffix[offset_end-l:offset_end]
        lines = ss.count('#')
        if ss.startswith("#") and lines > 2 and (lines-1) * nb > max_count:
            max_count = (lines-1) * nb
            max_indexes = (offset_end, nb, l, start_plage)
    
    if not max_indexes:
        return stackString

    max_ss = rstr.global_suffix[max_indexes[0]-max_indexes[2]:max_indexes[0]]
    endPos = max_ss.rfind('#')
    max_ss = max_ss[:endPos]
    max_len = len(max_ss)

    for o in range(max_indexes[3], max_indexes[3] + max_indexes[1] - 1):
        offset_global = rstr.res[o]
        offset = rstr.idxPos[offset_global]
        stackString = stackString[:offset] + stackString[offset+max_len:]
    
    return stackString


def convertStackToString(stackFrames):
    outputString = ""
    for frame in stackFrames:
        outputString += frame.module
        outputString += '$'
        outputString += frame.method
        outputString += '#'
    return outputString


def convertStringToStack(stackString):
    stackFrames = []
    rawFrames = stackString.split('#')
    for entry in rawFrames:
        if not entry:
            continue
        items = entry.split('$')
        try:
            frame = Frame(items[0], items[1])
        except IndexError:
            continue
        stackFrames.append(frame)
    return stackFrames
