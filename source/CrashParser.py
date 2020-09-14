import sys
import re
from CrashStructure import Frame, Stack


class CrashParser:

    def __init__(self, appName):
        self.appName = appName
        self.crashFramePattern = "^[0-9]+[ ]+(.*)0x[0-9A-Fa-f]{16} (.*)"


    def parse(self, id, stackTrace):
        stackFrames = []
        for line in stackTrace.splitlines():
            matcher = re.search(self.crashFramePattern, line.strip())
            if matcher != None:
                module = self.getModule(matcher)
                method = self.getMethod(matcher)

                if module != None and method != None:
                    frame = Frame(module, method)
                    stackFrames.append(frame)

        return Stack(id, stackTrace, stackFrames)


    def getModule(self, matcher):
        module = matcher.group(1).strip()
        if module.startswith('libsystem') or module.startswith('libc++abi') or module.startswith('libobjc.A') or module.startswith('libdyld'):
            return None
        return module


    def getMethod(self, matcher):
        method = matcher.group(2).strip()
        if method.startswith('0x'):
            return None
        plusIndex = method.find(' +')
        appNameIndex = method.find(' (in ' + self.appName)
        if plusIndex == -1 and appNameIndex == -1:
            return method
        elif plusIndex == -1 or appNameIndex == -1:
            endIndex = max(plusIndex, appNameIndex)
            return method[:endIndex]
        endIndex = min(plusIndex, appNameIndex)
        return method[:endIndex]


# Not really the main function but used for debugging CrashParser
def main(argv):
    appName = argv[0]
    parser = CrashParser(appName)

    # Sample mac stack trace of crashed thread
    # If the frame structure is changed, update the regex
    stackTrace = """Thread 0 Crashed:: Main Thread  Dispatch queue: com.apple.main-thread
                    0   com.company.sampleApp                	0x000000010d047fac ns4::ns5::CrashingClass::crashingMethod() (in Sample App) + 204
                    0   com.company.sampleApp                	0x000000010d047fac 0x7fff4baa4000
                    1   com.company.sampleApp                	0x000000010daed410 ns2::AnotherClass::loremIpsum() (in Sample App) (FileName.cpp:158)
                    2   com.company.sampleApp                	0x000000010daec5df ns2::AnotherClass::anotherMethod() (in Sample App) (FileName.cpp:116)
                    3   com.company.sampleApp                	0x000000010daebbc1 ns2::AnotherClass::randomFunction(std::__1::shared_ptr<foo::SampleClass>) (in Sample App) (FileName.cpp:95)
                    4   com.company.sampleApp                	0x000000010d4ac914 ns1::func2(std::__1::shared_ptr<foo::SampleClass>, bool) (in Sample App) (AppController.cpp:366)
                    5   com.company.sampleApp                	0x000000010bad3add fun1() (in Sample App) (CoreApplication.cpp:21)
                    6   com.company.sampleApp                	0x000000010baa89e1 main (in Sample App) (main.cpp:98)
                    7   libdyld.dylib                 	0x00007fff72a442e5 start + 1"""

    crashStack = parser.parse(1, stackTrace)
    print(crashStack.id)
    for frame in crashStack.frames:
        print(frame.module + '\t' + frame.method)


if __name__ == "__main__":
    main(sys.argv[1:])

