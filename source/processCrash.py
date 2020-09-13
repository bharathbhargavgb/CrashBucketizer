import sys
import os
import shutil
from CrashParser import *
from CrashBucketizer import *

class CrashProcessor:
    def __init__(self, appName):
        self.parser = CrashParser(appName)
        self.bucketizer = CrashBucketizer([])

    def processCrashes(self, crashFile):
        counter = 0
        crashString = ""
        crashLines = open(crashFile).readlines()
        for line in crashLines:
            if line and line.strip():
                crashString += line
            elif crashString:
                self.processCrash(counter, crashString)
                counter += 1
                crashString = ""

        if crashString:
             self.processCrash(counter, crashString)
    
    
    def processCrash(self, counter, crashString):
        crashStack = self.parser.parse(counter, crashString)
        self.bucketizer.bucketize(crashStack)
    

    def generateReport(self, outputPath):
        if os.path.exists(outputPath):
            shutil.rmtree(outputPath)
        os.makedirs(outputPath)

        for bucket in self.bucketizer.getBuckets():
            bucketName = 'bucket' + str(bucket.id)
            with open(os.path.join(outputPath, bucketName + ".txt"), "a") as bucketFile:
                for crash in bucket.stacks:
                    bucketFile.write('Crash ' + str(crash.id) + os.linesep)
                    bucketFile.write(crash.getRawStackTrace() + os.linesep)


def main(argv):
    #crashesFile = "../dataset/sample_crashes.txt"
    crashesFile = "../dataset/kpr_mac_stack_trace.txt"
    processor = CrashProcessor(argv[0])
    processor.processCrashes(crashesFile)
    processor.generateReport("../dumps")


if __name__ == "__main__":
    main(sys.argv[1:])