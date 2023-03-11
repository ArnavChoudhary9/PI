from ..Scene.Entity import Entity

from typing import Type, TypeVar, List
import pyrr

_C = TypeVar("_C")

class Color4(pyrr.Vector4):
    @property
    def r(self) -> float: return self.x
    @property
    def g(self) -> float: return self.y
    @property
    def b(self) -> float: return self.z
    @property
    def a(self) -> float: return self.w

class Color3(pyrr.Vector3):
    @property
    def r(self) -> float: return self.x
    @property
    def g(self) -> float: return self.y
    @property
    def b(self) -> float: return self.z

# Remember Annotations will pass down the class hierarchy
class Behaviour:
    def __init__(self, entity: Entity) -> None:
        self._Entity: Entity = entity
        from ..Scene.Components import TransformComponent
        self._Transform: TransformComponent = entity.GetComponent(TransformComponent)

    def GetComponent    (self, _type: Type[_C]) -> _C   : return self._Entity.GetComponent    (_type)
    def HasComponent    (self, _type: Type[_C]) -> bool : return self._Entity.HasComponent    (_type)
    def RemoveComponent (self, _type: Type[_C]) -> None :        self._Entity.RemoveComponent (_type)

    def GetEntityOfType(self, _type: Type[_C]) -> Entity: return self.GetEntitiesOfType(_type)[0]
    def GetEntitiesOfType(self, _type: Type[_C]) -> List[Entity]:
        scene = self._Entity._Scene
        entities = []

        for entityID in range(scene._Registry._next_entity_id+1):
            if scene._Registry.has_component(entityID, _type): entities.append(Entity(entityID, scene))

        return entities

    def InstanciateEntity(self, name: str="Entity") -> Entity:
        entity = self._Entity._Scene.CreateEntity(name)
        return entity

    def OnAttach(self) -> None: ...
    def OnDetach(self) -> None: ...
    def OnUpdate(self, dt: float) -> None: ...
