from .Renderer        import RendererAPI
from ..Logging.logger import PI_CORE_ASSERT

from abc import ABC, abstractmethod

class UniformBuffer(ABC):
    __slots__ = ("__NativeAPI",)

    @staticmethod
    def Init() -> None:
        if RendererAPI.GetAPI() == RendererAPI.API.Null:
            PI_CORE_ASSERT(False, "RendererAPI.NULL is currently not supported!")
            return

        elif RendererAPI.GetAPI() == RendererAPI.API.OpenGL:
            from ..Platform.OpenGL.OpenGLUniformBuffer import OpenGLUniformBuffer
            UniformBuffer.__NativeAPI = OpenGLUniformBuffer
            return

    @abstractmethod
    def SetData(data, size: int, offset: int=0) -> None: ...

    @staticmethod
    def Create(size: int, binding: int): UniformBuffer.__NativeAPI(size, binding)

