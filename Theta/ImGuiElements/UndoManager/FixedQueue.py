from collections import deque as Queue
from typing import Generic, TypeVar

_T = TypeVar("_T")

class FixedQueue(Queue, Generic[_T]):
    __Filler: _T
    def __init__(self, length: int, filler: _T=None) -> None:
        super().__init__([filler]*length, maxlen=length)
        self.__Filler = filler
    def Push     ( self, __x: _T, / ) -> None : super().append     (__x)
    def PushLeft ( self, __x: _T, / ) -> None : super().appendleft (__x)
    def Pop      ( self,          / ) -> _T   : return super().pop ()

    def Clear (self) -> None:
        self.clear()
        self.extend([self.__Filler]*self.maxlen)
