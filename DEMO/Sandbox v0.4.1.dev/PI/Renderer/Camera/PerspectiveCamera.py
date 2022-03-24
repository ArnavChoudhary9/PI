from .Camera         import Camera
from ..RenderCommand import RenderCommand

import pyrr

class PerspectiveCamera(Camera):
    __Fov  : float
    __Near : float
    __Far  : float

    def __init__(self, fov: float, aspectRatio: float, near: float=0.01, far: float=1000) -> None:
        self.__Fov = fov
        self._AspectRatio = aspectRatio
        self.__Near = near
        self.__Far = far

        viewMatrix = pyrr.matrix44.create_identity()
        projectionMatrix = pyrr.matrix44.create_perspective_projection_matrix(
            fov, aspectRatio, near, far
        )

        super().__init__(viewMatrix, projectionMatrix)

        RenderCommand.EnableDepth()

    def SetAspectRatio(self, newRatio: float) -> None:
        self._AspectRatio = newRatio

        self._ProjectionMatrix = pyrr.matrix44.create_perspective_projection_matrix(
            self.__Fov, self._AspectRatio, self.__Near, self.__Far
        )

        self._RecalculateViewMatrix()

    @property
    def FOV(self) -> float:
        return self.__Fov

    def SetFOV(self, fov: float) -> None:
        self.__Fov = fov
