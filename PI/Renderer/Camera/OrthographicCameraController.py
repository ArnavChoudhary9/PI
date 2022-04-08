from ...Events import EventDispatcher, EventType

from .CameraController import *

class OrthogrphicCameraController(CameraController):
    __slots__ = "__CameraMoveSpeed", "__CameraRotationSpeed"

    def __init__(self, camera: Camera) -> None:
        super().__init__(camera)

        self.__CameraMoveSpeed     : float = camera.GetSpeed()
        self.__CameraRotationSpeed : float = 135

    def OnEvent(self, e: Event) -> None:
        e.Handled = EventDispatcher(e).Dispach(
            lambda event: self._Camera.SetScale( self._Camera.Scale - (event.OffsetY * 0.05) + 0.001 ),
            EventType.MouseScrolled
        )
        
        self.__CameraMoveSpeed = self._Camera.GetSpeed()

    def OnUpdate(self, dt: float) -> None:
        if (Input.IsKeyPressed(PI_KEY_W)):
            self._Camera.SetPosition(
                self._Camera.Position + pyrr.Vector3([0, self.__CameraMoveSpeed * dt, 0])
            )
        if (Input.IsKeyPressed(PI_KEY_S)):
            self._Camera.SetPosition(
                self._Camera.Position - pyrr.Vector3([0, self.__CameraMoveSpeed * dt, 0])
            )

        if (Input.IsKeyPressed(PI_KEY_A)):
            self._Camera.SetPosition(
                self._Camera.Position - pyrr.Vector3([self.__CameraMoveSpeed * dt, 0, 0])
            )
        if (Input.IsKeyPressed(PI_KEY_D)):
            self._Camera.SetPosition(
                self._Camera.Position + pyrr.Vector3([self.__CameraMoveSpeed * dt, 0, 0])
            )

        if (Input.IsKeyPressed(PI_KEY_Q)):
            self._Camera.SetRotation(self._Camera.Rotation - self.__CameraRotationSpeed * dt)
        if (Input.IsKeyPressed(PI_KEY_E)):
            self._Camera.SetRotation(self._Camera.Rotation + self.__CameraRotationSpeed * dt)
