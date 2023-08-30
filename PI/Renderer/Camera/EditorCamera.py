from ...Events      import Event, MouseScrolledEvent, EventDispatcher
from ...ButtonCodes import PI_KEY_LEFT_ALT, PI_MOUSE_BUTTON_LEFT, PI_MOUSE_BUTTON_MIDDLE, PI_MOUSE_BUTTON_RIGHT
from ...Core.Input  import Input

from .PerspectiveCamera import PerspectiveCamera

from typing import Tuple
import pyrr

class EditorCamera(PerspectiveCamera):
    __Position   : pyrr.Vector3
    __FocalPoint : pyrr.Vector3

    __InitialMousePosition: Tuple[float, float] = (0.0, 0.0)

    __Distance: float
    __Pitch: float
    __Yaw: float

    __ViewportWidth: float = 1280
    __ViewportHeight: float = 720

    def __init__(self, fov: float, aspectRatio: float, near: float, far: float) -> None:
        self._Reset()
        super().__init__(fov, aspectRatio, near, far)

    def _Reset(self) -> None:
        self.__Position   : pyrr.Vector3 = pyrr.Vector3([ 0.0, 0.0, 0.0 ])
        self.__FocalPoint : pyrr.Vector3 = pyrr.Vector3([ 0.0, 0.0, 0.0 ])

        self.__Distance: float = -5.0
        self.__Pitch: float = 0.0
        self.__Yaw: float = 0.0

    def _RecalculateViewMatrix(self) -> None:        
        self.__Position = self.__CalculatePosition()
        orientation = self.Orientation
        self._ViewMatrix = pyrr.Matrix44.from_quaternion(orientation) @ pyrr.Matrix44.from_translation(self.__Position)
        self._ViewMatrix = pyrr.matrix44.inverse(self._ViewMatrix)

        self._ViewProjectionMatrix = self._ViewMatrix @ self._ProjectionMatrix

    def OnUpdate(self, dt: float):
        if Input.IsKeyPressed(PI_KEY_LEFT_ALT):
            mouse = Input.GetMousePos()
            delta = (
                (self.__InitialMousePosition[0] - mouse[0]) * dt,
                (self.__InitialMousePosition[1] - mouse[1]) * dt
            )
            
            self.__InitialMousePosition = mouse

            if   Input.IsMouseButtonPressed( PI_MOUSE_BUTTON_MIDDLE ): self.__MousePan    ( delta    )
            elif Input.IsMouseButtonPressed( PI_MOUSE_BUTTON_LEFT   ): self.__MouseRotate ( delta    )
            elif Input.IsMouseButtonPressed( PI_MOUSE_BUTTON_RIGHT  ): self.__MouseZoom   ( delta[1] )

        self._RecalculateViewMatrix()

    def OnEvent(self, e: Event): EventDispatcher(e).Dispach(self.__OnMouseScroll, MouseScrolledEvent)

    @property
    def Distance(self) -> float: return self.__Distance
    def SetDistance(self, distance: float) -> None: self.__Distance = distance

    def SetViewportSize(self, width: float, height: float) -> None:
        self.__ViewportWidth = width
        self.__ViewportHeight = height

        # PerspectiveCamera.SetAspectRatio() automatically recalculates view & projection
        self.SetAspectRatio(width / height)

    @property
    def UpDirection(self) -> pyrr.Vector3:
        orientation = pyrr.matrix44.create_from_quaternion(self.Orientation)
        return pyrr.vector3.create_from_vector4(orientation[1])[0]
    
    @property
    def RightDirection(self) -> pyrr.Vector3:
        orientation = pyrr.matrix44.create_from_quaternion(self.Orientation)
        return pyrr.vector3.create_from_vector4(orientation[0])[0]

    @property
    def ForwardDirection(self) -> pyrr.Vector3:
        orientation = pyrr.matrix44.create_from_quaternion(self.Orientation)
        return pyrr.vector3.create_from_vector4(orientation[2])[0]

    @property
    def Position(self) -> pyrr.Vector3: return self.__Position

    @property
    def Orientation(self) -> pyrr.Quaternion: return pyrr.quaternion.create_from_eulers([ -self.__Pitch, -self.__Yaw, 0.0 ])

    @property
    def Pitch(self) -> float: return self.__Pitch
    @property
    def Yaw(self) -> float: return self.__Yaw

    def __OnMouseScroll(self, e: MouseScrolledEvent) -> None:
        delta = e.OffsetY * 0.1
        self.__MouseZoom(delta)
        self._RecalculateViewMatrix()
        return False

    def __MousePan(self, delta: Tuple[float, float]) -> None:
        xSpeed, ySpeed = self.__PanSpeed
        self.__FocalPoint += -self.RightDirection * delta[0] * xSpeed * self.__Distance
        self.__FocalPoint +=  self.UpDirection    * delta[1] * ySpeed * self.__Distance

    def __MouseRotate(self, delta: Tuple[float, float]) -> None:
        yawSign = -1.0 if self.UpDirection[1] < 0 else 1.0
        self.__Yaw += yawSign * delta[0] * self.__RotationSpeed
        self.__Pitch += delta[1] * self.__RotationSpeed

    def __MouseZoom(self, delta: float) -> None: self.__Distance -= delta * self.__ZoomSpeed
    def __CalculatePosition(self) -> pyrr.Vector3: return self.__FocalPoint - self.ForwardDirection * self.__Distance

    @property
    def __PanSpeed(self) -> Tuple[float, float]:
        x = min(self.__ViewportWidth / 1000.0, 0.2)
        xFactor = 0.0145 * (x*x) - 0.1778 * x + 0.2

        y = min(self.__ViewportHeight / 1000.0, 0.2)
        yFactor = 0.0145 * (y*y) - 0.1778 * y + 0.2

        return xFactor, yFactor

    @property
    def __RotationSpeed(self) -> float: return 0.1

    @property
    def __ZoomSpeed(self) -> float:
        distance = self.__Distance * 0.1
        distance = max(distance, 0.001)
        speed = 1 / distance * 0.9
        speed = min(speed, 7.5)
        return speed
