from ...Events import EventDispatcher, EventType, \
    MouseButtonPressedEvent, MouseButtonReleasedEvent, MouseMovedEvent
from ...Core.Input import Input
from ...ButtonCodes.MouseButtonCodes import PI_MOUSE_BUTTON_MIDDLE, PI_MOUSE_BUTTON_RIGHT

from .PerspectiveCamera import PerspectiveCamera
from .CameraController  import *

from numpy import radians

MOUSE_BUTTON = PI_MOUSE_BUTTON_RIGHT
class PerspectiveCameraController(CameraController):
    __slots__ = "__CameraMoveSpeed", "__CameraRotationSpeed", "__LastMousePos", "__MouseClicked"

    def __init__(self, camera: PerspectiveCamera) -> None:
        super().__init__(camera)

        self.__CameraMoveSpeed     : float = camera.GetSpeed()
        self.__CameraRotationSpeed : float = 0.075
        self.__LastMousePos        : tuple = ( 0, 0 )
        self.__MouseClicked        : bool  = False

    def __OnMouseClicked(self, e: MouseButtonPressedEvent) -> bool:
        if not self.__MouseClicked: self.__MouseClicked = e.ButtonCode == MOUSE_BUTTON
        if self.__MouseClicked: self.__LastMousePos = Input.GetMousePos()

    def __OnMouseDragged(self, e: MouseMovedEvent) -> bool:
        if not self.__MouseClicked: return False

        delta = ( Input.GetMouseX() - self.__LastMousePos[0], Input.GetMouseY() - self.__LastMousePos[1] )
        self.__LastMousePos = Input.GetMousePos()

        self._Camera.SetRotation(
            self._Camera.Rotation + (pyrr.Vector3([ delta[1], delta[0], 0.0 ]) * self.__CameraRotationSpeed)
        )

        return True

    def __OnMouseReleased(self, e: MouseButtonReleasedEvent) -> bool:
        if self.__MouseClicked: self.__MouseClicked = e.ButtonCode != MOUSE_BUTTON
        return False

    def OnEvent(self, e: Event) -> None:
        super().OnEvent(e)

        dispatcher = EventDispatcher(e)

        dispatcher.Dispach(
            lambda e: self._Camera.SetFOV(self._Camera.FOV - e.OffsetY * 3),
            EventType.MouseScrolled
        )

        dispatcher.Dispach( self.__OnMouseClicked  , EventType.MouseButtonPressed  )
        dispatcher.Dispach( self.__OnMouseDragged  , EventType.MouseMoved          )
        dispatcher.Dispach( self.__OnMouseReleased , EventType.MouseButtonReleased )

        self.__CameraMoveSpeed = self._Camera.GetSpeed()

    def OnUpdate(self, dt: float) -> None:
        # Local Axis
        rotation = pyrr.quaternion.create_from_eulers( radians([ *self._Camera.Rotation ]) )
        rotation = pyrr.matrix44.create_from_quaternion(rotation)

        forward, w = pyrr.vector3.create_from_vector4(rotation[2])
        forward   *= dt * self.__CameraMoveSpeed

        right, w   = pyrr.vector3.create_from_vector4(rotation[0])
        right     *= dt * self.__CameraMoveSpeed

        up, w      = pyrr.vector3.create_from_vector4(rotation[1])
        up        *= dt * self.__CameraMoveSpeed

        if (Input.IsKeyPressed(PI_KEY_W)):
            self._Camera.Translate(-forward)
        if (Input.IsKeyPressed(PI_KEY_S)):
            self._Camera.Translate( forward)

        if (Input.IsKeyPressed(PI_KEY_D)):
            self._Camera.Translate( right)
        if (Input.IsKeyPressed(PI_KEY_A)):
            self._Camera.Translate(-right)

        if (Input.IsKeyPressed(PI_KEY_LEFT_SHIFT)):
            self._Camera.Translate( up)
        if (Input.IsKeyPressed(PI_KEY_LEFT_CONTROL)):
            self._Camera.Translate(-up)
