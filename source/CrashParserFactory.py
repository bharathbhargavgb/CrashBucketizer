from PlatformUtils import *
from CrashParser import *
from CrashParserCppMac import *
from CrashParserCppWin import *


class CrashParserFactory:
    def getCrashParser(self, os, lang):
        if lang == ProgrammingLanguage.CPP:
            if os == OperatingSystem.MAC:
                return CrashParserCppMac()
            elif os == OperatingSystem.WINDOWS:
                return CrashParserCppWin()

        return CrashParser()