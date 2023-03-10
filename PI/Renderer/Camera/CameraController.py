from ...Core.Input    import Input
from ...ButtonCodes.KeyCodes import *
from ...Events   import Event, WindowResizeEvent, EventDispatcher, EventType

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

    def OnEvent(self, e: WindowResizeEvent) -> None:
        EventDispatcher(e).Dispach(
            lambda e: self._Camera.SetAspectRatio( e.Width / e.Height ),
            EventType.WindowResize
        )
