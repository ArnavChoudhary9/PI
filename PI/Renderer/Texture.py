from ..logger  import PI_CORE_ASSERT
from .Renderer import Renderer, RendererAPI

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

    def Bind(self, slot: int=0) -> None:
        pass

    def Unbind(self) -> None:
        pass

class Texture2D(Texture):
    __NativeAPI = None

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
    def Create(texturePath: str):
        return Texture2D.__NativeAPI(texturePath)
