from ..logger  import PI_CORE_ASSERT
from .Buffer   import IndexBuffer, VertexBuffer
from .Renderer import Renderer, RendererAPI

class VertexArray:
    __NativeAPI = None

    def Bind(self) -> None:
        pass
    
    def Unbind(self) -> None:
        pass

    def AddVertexBuffer(self, buffer: VertexBuffer) -> None:
        pass

    def SetIndexBuffer(self, buffer: IndexBuffer) -> None:
        pass

    @property
    def VertexBuffers(self) -> list:
        pass

    @property
    def IndexBuffer(self) -> IndexBuffer:
        pass

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

