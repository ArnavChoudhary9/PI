from typing import Set, Any, Generic, TypeVar

T = TypeVar("T")

class SubcriprtionInterface(Generic[T]):
    __Subcribers: Set[T]

    def __init__(self) -> None: self.__Subcribers = set()

    def Subscribe(self, obj: T) -> None:
        self.__Subcribers.add(obj)
    def Unsubscribe(self,obj: T) -> None:
        try: self.__Subcribers.remove(obj)
        except KeyError: pass
