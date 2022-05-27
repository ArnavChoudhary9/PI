from .Camera         import Camera
from ..RenderCommand import RenderCommand

import pyrr

class PerspectiveCamera(Camera):
    __slots__ = "_Fov", "_Near", "_Far"

    def __init__(self, fov: float, aspectRatio: float, near: float=0.01, far: float=1000) -> None:
        self._Fov = fov
        self._AspectRatio = aspectRatio
        self._Near = near
        self._Far = far

        viewMatrix = pyrr.matrix44.create_identity()
        projectionMatrix = pyrr.matrix44.create_perspective_projection_matrix(
            fov, aspectRatio, near, far
        )

        super().__init__(viewMatrix, projectionMatrix)

        RenderCommand.EnableDepth()

    def SetAspectRatio(self, newRatio: float) -> None:
        self._AspectRatio = newRatio

        self._ProjectionMatrix = pyrr.matrix44.create_perspective_projection_matrix(
            self._Fov, self._AspectRatio, self._Near, self._Far
        )

        self._RecalculateViewMatrix()

    @property
    def FOV(self) -> float:
        return self._Fov

    def RecalculateProjection(self) -> None:
        self._ProjectionMatrix = pyrr.matrix44.create_perspective_projection_matrix(
            self._Fov, self._AspectRatio, self._Near, self._Far
        )
        self._RecalculateViewMatrix()

    def GetSpeed(self) -> float:
        return self._Fov / 15

    def SetFOV(self, fov: float) -> None:
        self._Fov = fov + 0.001
        
        self._ProjectionMatrix = pyrr.matrix44.create_perspective_projection_matrix(
            fov, self._AspectRatio, self._Near, self._Far
        )

        self._RecalculateViewMatrix()
