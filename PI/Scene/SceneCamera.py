from ..Logging.logger  import PI_CORE_ASSERT
from ..Renderer.Camera import Camera, PerspectiveCamera, OrthographicCamera

from dataclasses import dataclass

class SceneCamera():
    @dataclass(frozen=True)
    class ProjectionTypeEnum:
        Orthographic : int = 0
        Perspective  : int = 1

    __ProjectionType : int    = ProjectionTypeEnum.Orthographic
    __Camera         : Camera = None

    def __init__(self, projectionType: int=ProjectionTypeEnum.Orthographic) -> None:
        self.__ProjectionType = projectionType
        self._RecalculateCamera()

    @property
    def ProjectionType (self) -> int    : return self.__ProjectionType
    @property 
    def CameraObject   (self) -> Camera : return self.__Camera
    
    def SetProjection(self, projection: int) -> None:
        self.__ProjectionType = projection
        aspectRatio = self.__Camera.AspectRatio
        self.__Camera = None
        self._RecalculateCamera()
        self.__Camera.SetAspectRatio(aspectRatio)

    def _RecalculateCamera(self) -> None:
        if self.__Camera is None:
            if   self.__ProjectionType == SceneCamera.ProjectionTypeEnum.Orthographic : self.__Camera = OrthographicCamera (  1 , 1 )
            elif self.__ProjectionType == SceneCamera.ProjectionTypeEnum.Perspective  : self.__Camera = PerspectiveCamera  ( 45 , 1 )
            else : PI_CORE_ASSERT(False, "Unknown Projection Type")

        self.__Camera._RecalculateViewMatrix()
