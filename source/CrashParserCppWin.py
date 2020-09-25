from CrashParser import *
from CrashStructure import Frame, Stack


class CrashParserCppWin(CrashParser):

    def parse(self, id, stackTrace):
        stackFrames = []
        for line in stackTrace.splitlines():
            frameInfo = self.__getFrameInfo(line)
            if frameInfo != None:
                module = self.__extractModule(frameInfo)
                method = self.__extractMethod(frameInfo)

                if self.isValidString(module) and self.isValidString(method):
                    frame = Frame(module, method)
                    stackFrames.append(frame)

        stackFrames = self.removeRecursiveCalls(stackFrames)
        stackFrames = stackFrames[:40]
        return Stack(id, stackTrace, stackFrames)


    def __getFrameInfo(self, stackLine):
        try:
            frameInfo = stackLine.rsplit(' ', 1)[-1]
        except IndexError:
            return None
        return frameInfo


    def __extractModule(self, frameInfo):
        try:
            module = frameInfo.split('!', 1)[0].strip()
        except IndexError:
            return None
        module = self.__stripSystemModules(module)
        module = self.stripUnsymbolicatedFrame(module)
        return module


    def __extractMethod(self, frameInfo):
        try:
            method = frameInfo.split('!', 1)[1].strip()
        except IndexError:
            return None
        method = self.__stripOffset(method)
        method = self.stripUnsymbolicatedFrame(method)
        return method


    def __stripSystemModules(self, module):
        SYSTEM_MODULES = ('ntdll', 'kernel32', 'ucrtbase', 'VCRUNTIME140', 'KERNELBASE', 'msvcp140')
        if not module or module.startswith(SYSTEM_MODULES):
            return None
        return module


    def __stripOffset(self, method):
        if not method:
            return None
        offsetIndex = method.find('+')
        if offsetIndex == -1:
            return method
        return method[:offsetIndex]



# Not really the main function but used for debugging CrashParser
def main():
    parser = CrashParserCppWin()

    # Sample mac stack trace of crashed thread
    # If the frame structure is changed, update the regex
    stackTrace = """STACK_TEXT:  
        000000e7`33cff358 00007ff7`8c07cb9f : 00000000`00000365 000000e7`33cff3c0 000000e7`33cff450 00007ff9`ac4fb900 : 0x0
        000000e7`33cff360 00007ff7`8c07c46b : 00000216`7dcc89e0 000000e7`33cff4a0 00000000`00000365 000000e7`33cff5b0 : Kindle_Previewer_3!yj::getRenderDocSection+0x7f
        000000e7`33cff440 00007ff7`8c07cfe4 : 00000216`00000365 00000216`7e2915c0 000000e7`33cff5b0 000000e7`33cff4a0 : Kindle_Previewer_3!yj::IndexSectionTask::getFirstPageOfSection+0xab
        000000e7`33cff620 00007ff7`8c07d43f : 00000216`7e2915c0 00000216`7e2915c0 00000216`7e2915c0 000000e7`33cff620 : Kindle_Previewer_3!yj::IndexSectionTask::identifyForwardIndexingStartPage+0x84
        000000e7`33cff6c0 00007ff7`8c07e25f : 00000000`00000365 00000000`00000000 00000216`7e2915c0 00000000`00000000 : Kindle_Previewer_3!yj::IndexSectionTask::initialize+0xef
        000000e7`33cff740 00007ff7`8bf4335d : 00000000`00000000 00000000`00000000 0000a246`4151272b 00000000`00000000 : Kindle_Previewer_3!yj::IndexWorkItem::step+0xf
        000000e7`33cff770 00007ff7`8bdc8dfc : 00000216`7dd74c30 00000216`7de609f0 00000000`00000000 00000216`7de609d0 : Kindle_Previewer_3!yj::SingleThreadSupervisor::step+0xcd
        000000e7`33cff7b0 00007ff7`8b355fb6 : 00000216`7de609f0 00000216`01aa76c0 000028c7`0211c230 00000216`7de8f198 : Kindle_Previewer_3!yj::DocumentIndexer::step+0x2c
        000000e7`33cff7e0 00007ff7`8b363f1a : 00000000`00001388 00000216`7dd74c30 00000216`7dd74c30 00000000`00000000 : Kindle_Previewer_3!kccore::EditorPageModelProvider::indexBookDaemon+0xb6
        000000e7`33cff850 00007ff9`a9490e82 : 00000000`00000000 00000216`01be4100 00000000`00000000 00000000`00000000 : Kindle_Previewer_3!boost::`anonymous namespace'::thread_start_function+0x3a
        000000e7`33cff880 00007ff9`ac3d7bd4 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ucrtbase!thread_start<unsigned int (__cdecl*)(void *),1>+0x42
        000000e7`33cff8b0 00007ff9`ac52ce51 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : kernel32!BaseThreadInitThunk+0x14
        000000e7`33cff8e0 00000000`00000000 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x21"""

    crashStack = parser.parse(1, stackTrace)
    for frame in crashStack.frames:
        print(frame.module + '\t' + frame.method)


if __name__ == "__main__":
    main()

