from PI import *

class UndoEvent: ...

class ComponentDeletionEvent(UndoEvent):
    ComponentDeleted: CTV
    Entity: Entity
    def __init__(self, component: CTV, entity: Entity) -> None:
        self.ComponentDeleted = component
        self.Entity = entity
