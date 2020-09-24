import sys
import re
from CrashStructure import Frame, Stack
from stack_optimizer import *


class CrashParser:

    def __init__(self, appName):
        self.appName = appName
        self.crashFramePattern = "^[0-9]+[ ]+(.*)0x[0-9A-Fa-f]{16} (.*)"


    def parse(self, id, stackTrace):
        stackFrames = []
        for line in stackTrace.splitlines():
            matcher = re.search(self.crashFramePattern, line.strip())
            if matcher != None:
                module = self.__extractModule(matcher)
                method = self.__extractMethod(matcher)

                if self.__isValid(module) and self.__isValid(method):
                    frame = Frame(module, method)
                    stackFrames.append(frame)

        stackFrames = self.__removeRecursiveCalls(stackFrames)
        stackFrames = stackFrames[:40]
        return Stack(id, stackTrace, stackFrames)


    def __extractModule(self, matcher):
        module = matcher.group(1).strip()
        module = self.__stripSystemModules(module)
        return module


    def __extractMethod(self, matcher):
        method = matcher.group(2).strip()
        method = self.__stripOffset(method)
        method = self.__stripUnsymbolicatedMethod(method)
        method = self.__stripParameters(method)
        return method


    def __stripSystemModules(self, module):
        SYSTEM_MODULES = ('libsystem', 'libc++abi', 'libobjc.A', 'libdyld', 'libdispatch')
        if not module or module.startswith(SYSTEM_MODULES):
            return None
        return module


    def __removeRecursiveCalls(self, stackFrames):
        return removeRepeats(stackFrames)


    def __stripOffset(self, method):
        if not method:
            return None
        offsetIndex = method.find(' + ')
        appNameIndex = method.find(' (in ' + self.appName)
        if offsetIndex == -1 and appNameIndex == -1:
            return method
        elif offsetIndex == -1 or appNameIndex == -1:
            endIndex = max(offsetIndex, appNameIndex)
            return method[:endIndex]
        endIndex = min(offsetIndex, appNameIndex)
        return method[:endIndex]


    def __stripUnsymbolicatedMethod(self, method):
        hexPrefix = '0x'
        if not method or method.startswith(hexPrefix):
            return None
        return method


    def __stripParameters(self, method):
        if not method:
            return None
        openParanIndex = method.find('(')
        if openParanIndex != -1:
            return method[:openParanIndex]
        return method


    def __isValid(self, str):
        if str == None or len(str) <= 0:
            return False
        return True



# Not really the main function but used for debugging CrashParser
def main(argv):
    appName = argv[0]
    parser = CrashParser(appName)

    # Sample mac stack trace of crashed thread
    # If the frame structure is changed, update the regex
    stackTrace = """Thread 0 Crashed:: Main Thread  Dispatch queue: com.apple.main-thread
                    0   com.company.sampleApp                	0x000000010d047fac ns4::ns5::CrashingClass::crashingMethod() (in Sample App) + 204
                    0   com.company.sampleApp                	0x000000010d047fac ns4::ns5::CrashingClass::crashingMethod() (in Sample App) + 204
                    1   com.company.sampleApp                	0x000000010d047fac 0x7fff4baa4000
                    2   com.company.sampleApp                	0x000000010daed410 ns2::AnotherClass::loremIpsum() (in Sample App) (FileName.cpp:158)
                    3   com.company.sampleApp                	0x000000010daec5df ns2::AnotherClass::anotherMethod() (in Sample App) (FileName.cpp:116)
                    4   com.company.sampleApp                	0x000000010daebbc1 ns2::AnotherClass::randomFunction(std::__1::shared_ptr<foo::SampleClass>) (in Sample App) (FileName.cpp:95)
                    5   com.company.sampleApp                	0x000000010daed410 ns2::AnotherClass::loremIpsum() (in Sample App) (FileName.cpp:158)
                    6   com.company.sampleApp                	0x000000010daec5df ns2::AnotherClass::anotherMethod() (in Sample App) (FileName.cpp:116)
                    7   com.company.sampleApp                	0x000000010daebbc1 ns2::AnotherClass::randomFunction(std::__1::shared_ptr<foo::SampleClass>) (in Sample App) (FileName.cpp:95)
                    8   com.company.sampleApp                	0x000000010d4ac914 ns1::func2(std::__1::shared_ptr<foo::SampleClass>, bool) (in Sample App) (AppController.cpp:366)
                    9   com.company.sampleApp                	0x000000010bad3add fun1() (in Sample App) (CoreApplication.cpp:21)
                    9   com.company.sampleApp                	0x000000010bad3add fun1() (in Sample App) (CoreApplication.cpp:21)
                    10  com.company.sampleApp                	0x000000010baa89e1 main (in Sample App) (main.cpp:98)
                    11  libdyld.dylib                 	0x00007fff72a442e5 start + 1"""

    crashStack = parser.parse(1, stackTrace)
    print(crashStack.id)
    for frame in crashStack.frames:
        print(frame.module + '\t' + frame.method)


if __name__ == "__main__":
    main(sys.argv[1:])

