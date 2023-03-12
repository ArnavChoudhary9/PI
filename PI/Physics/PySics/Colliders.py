from .Utility import *
from abc import ABC, abstractmethod

class Collider(ABC):
    Origin: pyrr.Vector3
    Bounds: pyrr.Vector3

    IsTrigger: bool = False

    def __init__(self,
        origin: pyrr.Vector3=pyrr.Vector3([ 0, 0, 0 ]),
        bounds: pyrr.Vector3=pyrr.Vector3([ 1, 1, 1 ])
    ) -> None:
        self.Origin = origin
        self.Bounds = bounds

    # This is to make sure that Collider is not instantiated
    @abstractmethod
    def _MustOverride(self) -> None: ...

    @property
    def Scale(self) -> pyrr.Vector3: return self.Bounds

    def SetScale(self, scale: pyrr.Vector3) -> None: self.Bounds = scale

    def __repr__(self) -> str:
        return "<{}>: Origin: {}, Bounds: {}, IsTrigger: {}" \
            .format(type(self).__name__, self.Origin, self.Bounds, self.IsTrigger)

class BoxCollider(Collider):
    __BoxCollider: bool = True
    def _MustOverride(self) -> None: ...

class SphereCollider(Collider):
    __SphereCollider: bool = True
    def _MustOverride(self) -> None: ...

class PlaneCollider(Collider):
    __PlaneCollider: bool = True

    Up: pyrr.Vector3

    def __init__(self,
        origin: pyrr.Vector3=pyrr.Vector3([ 0, 0, 0 ]),
        bounds: pyrr.Vector3=pyrr.Vector3([ 0, 0, 0 ]),
        up    : pyrr.Vector3=pyrr.Vector3([ 0, 1, 0 ])
    ) -> None:
        super().__init__(origin, bounds)
        self.Up = up

    def __repr__(self) -> str:
        return "{}, Up: {}".format(super().__repr__(), self.Up)
    
    def _MustOverride(self) -> None: ...
