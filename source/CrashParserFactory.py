from PlatformUtils import *
from CrashParser import *
from CrashParserCppMac import *


class CrashParserFactory:
    def getCrashParser(self, os, lang):
        if lang == ProgrammingLanguage.CPP:
            if os == OperatingSystem.MAC:
                return CrashParserCppMac()
            elif os == OperatingSystem.WIN:
                return CrashParserCppWin()

        return CrashParser()