from .logger import LogSubcriprtions
from ..Core.Base import PI_DEBUG

import datetime
import inspect
from typing import List, Tuple

class DebugConsole:
    __Logs: List[Tuple[int, str]] = []
    __ErrorOccured: bool = False

    class Severity:
        TRACE : int = 0b00000001
        WARN  : int = 0b00000010
        ERROR : int = 0b00000100

        ALL : int = TRACE | WARN | ERROR

    @staticmethod
    def Init() -> None: LogSubcriprtions.Subscribe(DebugConsole)
        
    @staticmethod
    def GetLogs(filter: int=Severity.ALL) -> List[Tuple[int, str]]:
        if filter == DebugConsole.Severity.ALL: return DebugConsole.__Logs
        if filter == 0: return []
        
        logs = []

        for severity, log in DebugConsole.__Logs:
            if severity & filter: logs.append((severity, log))

        return logs
    
    @staticmethod
    def Clear():
        DebugConsole.__Logs.clear()
        DebugConsole.__ErrorOccured = False
        return DebugConsole

    @staticmethod
    def HasErrorOccurred(): return DebugConsole.__ErrorOccured

    @staticmethod
    def ClearError() -> None: DebugConsole.__ErrorOccured = False    

    @staticmethod
    def FormatString(string: str) -> str:
        timeStr = datetime.datetime.now().strftime("%H:%M:%S")

        extra = ""
        if PI_DEBUG:
            callerFrame = inspect.currentframe().f_back.f_back
            filename = callerFrame.f_code.co_filename.split('\\')[-1]
            extra = f" ({filename}, Line: {callerFrame.f_lineno}): "
        
        return f"[{timeStr}]{extra}{string}"

    @staticmethod
    def Trace(*args):
        if len(args) == 1: DebugConsole.__Logs.append((DebugConsole.Severity.TRACE, DebugConsole.FormatString(args[0])))
        else: DebugConsole.__Logs.append((DebugConsole.Severity.TRACE, DebugConsole.FormatString(" ".join(args))))
        return DebugConsole

    @staticmethod
    def Info(*args):
        if len(args) == 1: DebugConsole.__Logs.append((DebugConsole.Severity.TRACE, DebugConsole.FormatString(args[0])))
        else: DebugConsole.__Logs.append((DebugConsole.Severity.TRACE, DebugConsole.FormatString(" ".join(args))))
        return DebugConsole

    @staticmethod
    def Debug(*args):
        if len(args) == 1: DebugConsole.__Logs.append((DebugConsole.Severity.TRACE, DebugConsole.FormatString(args[0])))
        else: DebugConsole.__Logs.append((DebugConsole.Severity.TRACE, DebugConsole.FormatString(" ".join(args))))
        return DebugConsole

    @staticmethod
    def Log(*args):
        if len(args) == 1: DebugConsole.__Logs.append((DebugConsole.Severity.TRACE, DebugConsole.FormatString(args[0])))
        else: DebugConsole.__Logs.append((DebugConsole.Severity.TRACE, DebugConsole.FormatString(" ".join(args))))
        return DebugConsole

    @staticmethod
    def Warn(*args):
        if len(args) == 1: DebugConsole.__Logs.append((DebugConsole.Severity.WARN, DebugConsole.FormatString(args[0])))
        else: DebugConsole.__Logs.append((DebugConsole.Severity.TRACE, DebugConsole.FormatString(" ".join(args))))
        return DebugConsole

    @staticmethod
    def Error(*args):
        if len(args) == 1: DebugConsole.__Logs.append((DebugConsole.Severity.ERROR, DebugConsole.FormatString(args[0])))
        else: DebugConsole.__Logs.append((DebugConsole.Severity.TRACE, DebugConsole.FormatString(" ".join(args))))

        DebugConsole.__ErrorOccured = True
        return DebugConsole

    @staticmethod
    def Critical(*args):
        if len(args) == 1: DebugConsole.__Logs.append((DebugConsole.Severity.ERROR, DebugConsole.FormatString(args[0])))
        else: DebugConsole.__Logs.append((DebugConsole.Severity.TRACE, DebugConsole.FormatString(" ".join(args))))

        DebugConsole.__ErrorOccured = True
        return DebugConsole
