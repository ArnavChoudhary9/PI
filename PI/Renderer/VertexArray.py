from ..Logging.logger  import PI_CORE_ASSERT
from .Buffer   import IndexBuffer, VertexBuffer
from .Renderer import Renderer, RendererAPI

from abc import ABC, abstractmethod

class VertexArray(ABC):
    __slots__ = ("__NativeAPI",)

    @abstractmethod
    def Bind(self) -> None: ...
    @abstractmethod
    def Unbind(self) -> None: ...
    @abstractmethod
    def AddVertexBuffer(self, buffer: VertexBuffer) -> None: ...
    @abstractmethod
    def SetIndexBuffer(self, buffer: IndexBuffer) -> None: ...

    @property
    def VertexBuffers(self) -> list: ...
    @property
    def IndexBuffer(self) -> IndexBuffer: ...

    @staticmethod
    def Init() -> None:
        if (Renderer.GetAPI() == RendererAPI.API.Null):
            PI_CORE_ASSERT(False, "RendererAPI.None is currently not supported!")
            return

        elif (Renderer.GetAPI() == RendererAPI.API.OpenGL):
            from ..Platform.OpenGL.OpenGLVertexArray import OpenGLVertexArray
            VertexArray.__NativeAPI = OpenGLVertexArray
            return

        PI_CORE_ASSERT(False, "Unknown RendererAPI!!")
        return None

    @staticmethod
    def Create():
        return VertexArray.__NativeAPI()

