import datetime
from collections import deque
from abc import ABC
from threading import Thread

class Queue(deque):
    def push(self, item) -> None:
        self.append(item)

    def pop(self):
        return self.popleft()

class LogSeverity(ABC):
    Trace : int = 0x59      # White
    Log   : int = 0x5C      # Green
    Warn  : int = 0x5D      # Yellow
    Error : int = 0x5B      # Red

class LogColor(ABC):
    @staticmethod
    def color(string: str, severity: int) -> str:
        return "\033[{1}m{0}\033[00m".format(string, severity)

def GetTime() -> str:
    timeData = datetime.datetime.now()
    s = timeData.strftime("%H:%M:%S")
    return "[{}]".format(s)

class Console:
    __Queue : Queue
    __Name  : str

    __Running : bool
    __Thred   : Thread

    def __init__(self, name: str) -> None:
        self.__Queue = Queue()
        self.__Name  = name

        self.__Thred = Thread(target=self._PrintLoop)
        self.__Thred.start()

    def __del__(self) -> None:    
        try:
            self.__Thred.join()
            del self.__Thred
        except:
            del self.__Thred

    def Log(self, msg: str, sev: int):
        self.__Queue.push((sev, msg, GetTime()))

    def _PrintLoop(self) -> None:
        while (Console.__Running):
            if (len(self.__Queue) == 0): continue

            severity, msg, timestamp = self.__Queue.pop()
            msg = "{} - {} - {}".format(timestamp, self.__Name, msg)
            msg = LogColor.color(msg, severity)

            print(msg)

    @staticmethod
    def Init() -> None:
        Console.__Running = True

    @staticmethod
    def Destroy() -> None:
        Console.__Running = False
