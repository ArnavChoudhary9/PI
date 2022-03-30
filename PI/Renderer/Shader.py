from ..logger  import PI_CORE_ASSERT
from .Renderer import Renderer, RendererAPI

class Shader:
    __slots__ = ("__NativeAPI",)

    @staticmethod
    def Init() -> None:
        if (Renderer.GetAPI() == RendererAPI.API.Null):
            PI_CORE_ASSERT(False, "RendererAPI.None is currently not supported!")
            return

        elif (Renderer.GetAPI() == RendererAPI.API.OpenGL):
            from ..Platform.OpenGL.OpenGLShader import OpenGLShader
            Shader.__NativeAPI = OpenGLShader
            return

        PI_CORE_ASSERT(False, "Unknown RendererAPI!!")
        return None

    @property
    def Name(self) -> int:
        return self.__Name

    def __del__(self) -> None:
        pass

    def Bind(self) -> None:
        pass

    def Unbind(self) -> None:
        pass

    @staticmethod
    def Create(shaderFile: str):
        return Shader.__NativeAPI(shaderFile)
