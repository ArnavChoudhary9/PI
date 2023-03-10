from .Camera import Camera

import pyrr

class OrthographicCamera(Camera):
    __slots__ = "_Scale", "_Near", "_Far"

    def __init__(self, aspectRatio: float, scale: float=1) -> None:
        self._Scale = scale
        self._Near = 0.01
        self._Far = 1000
        self._AspectRatio = aspectRatio

        viewMatrix = pyrr.matrix44.create_identity()
        projectionMatrix = pyrr.matrix44.create_orthogonal_projection_matrix(
            -aspectRatio * scale, aspectRatio * scale, -scale, scale, self._Near, self._Far
        )

        super().__init__(viewMatrix, projectionMatrix)

    def SetAspectRatio(self, newRatio: float) -> None:
        self._AspectRatio = newRatio
        self._ProjectionMatrix = pyrr.matrix44.create_orthogonal_projection_matrix(
            -newRatio * self._Scale, newRatio * self._Scale, -self._Scale, self._Scale, self._Near, self._Far
        )

        self._RecalculateViewMatrix()

    @property
    def Scale(self) -> float:
        return self._Scale

    def SetScale(self, newScale: float) -> None:
        self._Scale = newScale
        self._ProjectionMatrix = pyrr.matrix44.create_orthogonal_projection_matrix(
            -self._AspectRatio * newScale, self._AspectRatio * newScale, -newScale, newScale, self._Near, self._Far
        )

        self._RecalculateViewMatrix()

    def GetSpeed(self) -> float:
        return self._Scale * 1.25
