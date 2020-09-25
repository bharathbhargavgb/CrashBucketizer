import sys
import os
import shutil
from CrashParserFactory import *
from CrashBucketizer import *
from PlatformUtils import *


class CrashProcessor:

    def __init__(self, os, lang):
        self.parser = CrashParserFactory().getCrashParser(os, lang)
        self.bucketizer = CrashBucketizer([], distance_measure='PDM', threshold=0.8, distToTop=0.01, alignOffset=0.0)

    def processCrashes(self, crashFile):
        counter = 0
        crashString = ""
        crashLines = open(crashFile).readlines()
        for line in crashLines:
            if line and line.strip():
                crashString += line
            elif crashString:
                self.processCrash(crashString, counter)
                counter += 1
                crashString = ""

        if crashString:
             self.processCrash(crashString, counter)
    
    
    def processCrash(self, crashString, crashID=0):
        crashStack = self.parser.parse(crashID, crashString)
        self.bucketizer.bucketize(crashStack)
    

    def generateReport(self, outputPath):
        if os.path.exists(outputPath):
            shutil.rmtree(outputPath)
        os.makedirs(outputPath)

        for bucket in self.bucketizer.getBuckets():
            bucketName = 'bucket' + str(bucket.id)
            print(str(bucket.id) + '\t' + str(len(bucket)) + '\t' + str(bucket.stacks[0].frames[0].method))
            with open(os.path.join(outputPath, bucketName + ".txt"), "a") as bucketFile:
                for crash in bucket.stacks:
                    bucketFile.write('Crash ' + str(crash.id) + os.linesep)
                    bucketFile.write(crash.getRawStackTrace() + os.linesep)

        print("Ignored crashes - " + str(len(self.bucketizer.getIgnoredStacks())))


def main(argv):
    if False:
        #crashesFile = "../dataset/sample_crashes_mac.txt"
        crashesFile = "../dataset/kpr_mac_stack_trace.txt"
        processor = CrashProcessor(OperatingSystem.MAC, ProgrammingLanguage.CPP)
    else:
        #crashesFile = "../dataset/sample_crashes_win.txt"
        crashesFile = "../dataset/kpr_win_stack_trace.txt"
        processor = CrashProcessor(OperatingSystem.WINDOWS, ProgrammingLanguage.CPP)
    processor.processCrashes(crashesFile)
    processor.generateReport("../dumps")


if __name__ == "__main__":
    main(sys.argv[1:])