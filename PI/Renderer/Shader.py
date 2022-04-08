from ..logger  import PI_CORE_ASSERT
from .Renderer import Renderer, RendererAPI

import pyrr

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

    def _GetUniformLocation(self, name: str) -> int:
        pass

    def SetMat4(self, name: str, matrix: pyrr.Matrix44) -> None:
        pass

    def SetFloat3(self, name: str, vector: pyrr.Vector3) -> None:
        pass

    def SetFloat4(self, name: str, vector: pyrr.Vector4) -> None:
        pass

    def SetFloat2(self, name: str, x: float, y: float) -> None:
        pass

    def SetFloat(self, name: str, value: float) -> None:
        pass

    def SetInt(self, name: str, value: int) -> None:
        pass

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

    # @staticmethod
    # @dispatch(str, str)
    # def Create(vertexShader: str, fragmentShader: str):
    #     return Shader.__NativeAPI(vertexShader, fragmentShader)
