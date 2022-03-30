from time import time_ns
import io

from multiprocessing import current_process
from threading import current_thread

def Time_MicroSec() -> float:
    return time_ns() / 1000

class ProfileResult:
    __slots__ = "Name", "Start", "End"

    def __init__(self, name: str, start: float, end: float) -> None:
        self.Name = name
        self.Start = start
        self.End = end

class InstrumentationSession:
    __slots__ = ("Name",)

    def __init__(self, name: str) -> None:
        self.Name = name

class Instrumentor:
    __slots__ = "__CurrentSession", "__OutputStream", "__ProfileCount", \
        "__Instance"

    def __init__(self) -> None:
        self.__CurrentSession : InstrumentationSession = None
        self.__ProfileCount   : int = 0

        Instrumentor.__Instance = self

    def BeginSession(self, name: str) -> None:
        self.__OutputStream = open("{}.json".format(name), 'w')
        self.WriteHeader()
        self.__CurrentSession = InstrumentationSession(name)

    def EndSession(self) -> None:
        self.WriteFooter()
        self.__OutputStream.close()

        del self.__CurrentSession
        self.__CurrentSession = None

        self.__ProfileCount = 0

    def WriteProfile(self, result: ProfileResult) -> None:
        if (self.__ProfileCount > 0): self.__OutputStream.write(", ")
        self.__ProfileCount += 1

        self.__OutputStream.write("{ ")
        self.__OutputStream.write("\"cat\": \"function\", ")
        self.__OutputStream.write("\"dur\": {}, ".format(result.End - result.Start))
        self.__OutputStream.write("\"name\": \"{}\", ".format(result.Name))
        self.__OutputStream.write("\"ph\": \"X\", ")
        self.__OutputStream.write("\"pid\": {}, ".format(current_process().pid))
        self.__OutputStream.write("\"tid\": {}, ".format(current_thread().native_id))
        self.__OutputStream.write("\"ts\": {} ".format(result.Start))
        self.__OutputStream.write("} ")

        self.__OutputStream.flush()

    def WriteHeader(self) -> None:
        self.__OutputStream.write("{\"otherData\": {}, \"traceEvents\": [ ")
        self.__OutputStream.flush()

    def WriteFooter(self) -> None:
        self.__OutputStream.write("]}")
        self.__OutputStream.flush()

    @staticmethod
    def Set(instance) -> None:
        Instrumentor.__Instance = instance

    @staticmethod
    def Get():
        return Instrumentor.__Instance

class InstrumentationTimer:
    __slots__ = "__Name", "__StartTimepoint", "__Stopped"

    def __init__(self, name: str) -> None:
        self.__Name = name
        self.__Stopped = False

        self.__StartTimepoint = Time_MicroSec()
        
    def __del__(self) -> None:
        if (self.__Stopped): return
        self.Stop()

    def Stop(self) -> None:
        endTimepoint: float = Time_MicroSec()
        Instrumentor.Get().WriteProfile(ProfileResult(self.__Name, self.__StartTimepoint, endTimepoint))

        self.__Stopped = True
