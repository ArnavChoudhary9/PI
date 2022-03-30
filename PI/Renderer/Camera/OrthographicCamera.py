from .Camera import Camera

import pyrr

class OrthographicCamera(Camera):
    __slots__ = ("__Scale",)

    def __init__(self, aspectRatio: float, scale: float=1) -> None:
        self.__Scale = scale
        self._AspectRatio = aspectRatio

        viewMatrix = pyrr.matrix44.create_identity()
        projectionMatrix = pyrr.matrix44.create_orthogonal_projection_matrix(
            -aspectRatio * scale, aspectRatio * scale, -scale, scale, -1, 1
        )

        super().__init__(viewMatrix, projectionMatrix)

    def SetAspectRatio(self, newRatio: float) -> None:
        self._AspectRatio = newRatio
        self._ProjectionMatrix = pyrr.matrix44.create_orthogonal_projection_matrix(
            -newRatio * self.__Scale, newRatio * self.__Scale, -self.__Scale, self.__Scale, -1, 1
        )

        self._RecalculateViewMatrix()

    @property
    def Rotation(self) -> float:
        return self._Rotation.z

    def SetRotation(self, angle: float) -> None:
        self._Rotation = pyrr.Vector3([ 0, 0, angle ])
        self._RecalculateViewMatrix()

    @property
    def Scale(self) -> float:
        return self.__Scale

    def SetScale(self, newScale: float) -> None:
        self.__Scale = newScale
        self._ProjectionMatrix = pyrr.matrix44.create_orthogonal_projection_matrix(
            -self._AspectRatio * newScale, self._AspectRatio * newScale, -newScale, newScale, -1, 1
        )

        self._RecalculateViewMatrix()
