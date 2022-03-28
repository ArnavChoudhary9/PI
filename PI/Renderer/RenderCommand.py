from ..Window     import Window, OS
from .RendererAPI import RendererAPI
from ..logger     import PI_CORE_ASSERT

class RenderCommand:
    __RendererAPI: RendererAPI

    @staticmethod
    def Init() -> None:
        if (Window.GetOS() == OS.Null):
            PI_CORE_ASSERT(False, "OS.Null is currently not supported!")
            return

        elif (Window.GetOS() == OS.Windows):
            from ..Platform.OpenGL.OpenGLRendererAPI import OpenGLRendererAPI
            RenderCommand.__RendererAPI = OpenGLRendererAPI
            return

        PI_CORE_ASSERT(False, "Unknown RendererAPI!!")
        return None

    @staticmethod
    def SetClearColor(*args) -> None:
        RenderCommand.__RendererAPI.SetClearColor(*args)

    @staticmethod
    def Clear() -> None:
        RenderCommand.__RendererAPI.Clear()

    @staticmethod
    def DrawIndexed(vertexArray) -> None:
        RenderCommand.__RendererAPI.DrawIndexed(vertexArray)

    @staticmethod
    def EnableDepth() -> None:
        RenderCommand.__RendererAPI.EnableDepth()

    @staticmethod
    def EnableBlending() -> None:
        RenderCommand.__RendererAPI.EnableBlending()
