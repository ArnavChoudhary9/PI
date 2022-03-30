import pyrr
from math import radians

class Camera:
    __slots__ = "_ProjectionMatrix", "_ViewMatrix", "_ViewProjectionMatrix", \
        "_Position", "_Rotation", \
        "_AspectRatio"

    def __init__(self, view: pyrr.Matrix44, projection: pyrr.Matrix44) -> None:
        self._ViewMatrix = view
        self._ProjectionMatrix = projection
        self._ViewProjectionMatrix = self._ViewMatrix @ self._ProjectionMatrix

        self._Position = pyrr.Vector3( [ 0, 0, 0 ] )
        self._Rotation = pyrr.Vector3( [ 0, 0, 0 ] )

        self._RecalculateViewMatrix()

    def _RecalculateViewMatrix(self) -> None:
        transform : pyrr.Matrix44 = pyrr.matrix44.create_from_translation(self._Position)

        rotX = pyrr.matrix44.create_from_z_rotation( radians(self._Rotation.x) )
        rotY = pyrr.matrix44.create_from_z_rotation( radians(self._Rotation.y) )
        rotZ = pyrr.matrix44.create_from_z_rotation( radians(self._Rotation.z) )

        rotation = rotX @ rotY @ rotZ

        model = rotation @ transform
        self._ViewMatrix = pyrr.matrix44.inverse(model)
        self._ViewProjectionMatrix = self._ViewMatrix @ self._ProjectionMatrix

    @property
    def Position(self) -> pyrr.Vector3:
        return self._Position

    def SetPosition(self, pos: pyrr.Vector3) -> None:
        self._Position = pos
        self._RecalculateViewMatrix()

    @property
    def Rotation(self) -> pyrr.Vector3:
        return self._Rotation

    def SetRotation(self, rotation: pyrr.Vector3) -> None:
        self._Rotation = rotation
        self._RecalculateViewMatrix()

    @property
    def ProjectionMatrix(self) -> pyrr.Matrix44:
        return self._ProjectionMatrix

    @property
    def ViewMatrix(self) -> pyrr.Matrix44:
        return self._ViewMatrix

    @property
    def ViewProjectionMatrix(self) -> pyrr.Matrix44:
        return self._ViewProjectionMatrix

    @property
    def AspectRatio(self) -> float:
        return self._AspectRatio

    def SetAspectRatio(self, newRatio: float) -> None:
        self._AspectRatio = newRatio
        self._RecalculateViewMatrix()
    