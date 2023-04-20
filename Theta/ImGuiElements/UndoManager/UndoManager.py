from .FixedQueue import *
from .UndoEvents import *

class UndoManager:
    _Instance=None

    __UndoEvents: FixedQueue
    __RedoEvents: FixedQueue

    def __init__(self) -> None:
        UndoManager._Instance = self

        self.__UndoEvents = FixedQueue(15, UndoEvent())
        self.__RedoEvents = FixedQueue(15, UndoEvent())

    @staticmethod
    def GetInstance(): return UndoManager._Instance

    def PushUndo(self, event: UndoEvent) -> None:
        self.__UndoEvents.Push(event)
        self.__RedoEvents.Clear()

    def PopUndo(self) -> UndoEvent:
        event = self.__UndoEvents.Pop()
        self.__UndoEvents.PushLeft(UndoEvent())
        self.__RedoEvents.Push(event)
        return event
    
    def PopRedo(self) -> UndoEvent:
        event = self.__RedoEvents.Pop()
        self.__RedoEvents.PushLeft(UndoEvent())
        self.__UndoEvents.Push(event)
        return event
