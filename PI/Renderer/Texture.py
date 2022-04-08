from ..logger  import PI_CORE_ASSERT
from .Renderer import Renderer, RendererAPI

from multipledispatch import dispatch

class Texture:
    @staticmethod
    def Init() -> None:
        Texture2D.Init()

    @property
    def RendererID(self) -> int:
        return self.__RendererID

    @property
    def Name(self) -> int:
        return self.__Name

    def __del__(self) -> None:
        pass

    @property
    def Width(self) -> int:
        pass

    @property
    def Height(self) -> int:
        pass

    def SetData(self, data, size) -> None:
        pass

    def Bind(self, slot: int=0) -> None:
        pass

    def Unbind(self) -> None:
        pass

class Texture2D(Texture):
    __slots__ = ("__NativeAPI",)

    @staticmethod
    def Init() -> None:
        if (Renderer.GetAPI() == RendererAPI.API.Null):
            PI_CORE_ASSERT(False, "RendererAPI.None is currently not supported!")
            return

        elif (Renderer.GetAPI() == RendererAPI.API.OpenGL):
            from ..Platform.OpenGL.OpenGLTexture import OpenGLTexture2D
            Texture2D.__NativeAPI = OpenGLTexture2D
            return

        PI_CORE_ASSERT(False, "Unknown RendererAPI!!")
        return None

    @staticmethod
    @dispatch(str)
    def Create(texturePath: str):
        return Texture2D.__NativeAPI(texturePath)

    @staticmethod
    @dispatch(int, int)
    def Create(width: int, height: int):
        return Texture2D.__NativeAPI(width, height)
