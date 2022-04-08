from ...Input    import Input
from ...KeyCodes import *
from ...Events   import Event

from .Camera     import Camera

import pyrr

class CameraController:
    __slots__ = ("_Camera",)

    def __init__(self, camera: Camera) -> None:
        self._Camera: Camera = camera

    @property
    def Camera(self) -> Camera:
        return self._Camera

    def OnUpdate(self, dt: float) -> None:
        pass

    def OnEvent(self, e: Event) -> None:
        pass
