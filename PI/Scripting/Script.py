import numpy as np
from ..Scene.Entity import Entity
import pyrr

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

class Behaviour:
    _Entity: Entity

    def __init__(self, entity: Entity) -> None:
        self._Entity = entity
        from ..Scene.Components import TransformComponent
        self._Transform: TransformComponent = entity.GetComponent(TransformComponent)

    def OnAttach(self) -> None: ...
    def OnDetach(self) -> None: ...
    def OnUpdate(self, dt: float) -> None: ...
