from PI import *

class UndoEvent: ...

class ComponentDeletionEvent(UndoEvent):
    ComponentDeleted: CTV
    _Entity: Entity
    def __init__(self, component: CTV, entity: Entity) -> None:
        self.ComponentDeleted = component
        self._Entity = entity

    @property
    def Entity(self) -> Entity: return self._Entity

class ComponentChangedEvent(UndoEvent):
    ComponentChanged: CTV
    _Entity: Entity

    PrevValues : Iterable[Any]
    NewValues  : Iterable[Any]

    def __init__(self, compChanged: CTV, entity: Entity, prevVals: Iterable[Any], newVals: Iterable[Any]) -> None:
        self.ComponentChanged = compChanged
        self._Entity = entity

        self.PrevValues = prevVals
        self.NewValues  = newVals
        
    @property
    def Entity(self) -> Entity: return self._Entity

    @property
    def Type(self) -> Type: return type(self.ComponentChanged)
