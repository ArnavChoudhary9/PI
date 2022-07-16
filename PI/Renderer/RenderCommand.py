from ..Core.Base         import PI_DEBUG
from ..Core.Window       import Window, OS
from ..Core.StateManager import StateManager
from ..Logging.logger    import PI_CORE_ASSERT

class RenderCommand:
    __slots__ = ("__RendererAPI",)

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
    def DrawIndexed(vertexArray, indices: int=None) -> None:
        if PI_DEBUG: StateManager.Stats.DrawCalls += 1
        RenderCommand.__RendererAPI.DrawIndexed(vertexArray, indices)

    @staticmethod
    def DrawLines(vertexArray, indices: int) -> None:
        if PI_DEBUG: StateManager.Stats.DrawCalls += 1
        RenderCommand.__RendererAPI.DrawLines(vertexArray, indices)

    @staticmethod
    def Resize(x: int, y: int, width: int, height: int) -> None:
        RenderCommand.__RendererAPI.Resize(x, y, width, height)

    @staticmethod
    def EnableDepth() -> None:
        RenderCommand.__RendererAPI.EnableDepth()

    @staticmethod
    def EnableBlending() -> None:
        RenderCommand.__RendererAPI.EnableBlending()

    @staticmethod
    def EnableCulling() -> None:
        RenderCommand.__RendererAPI.EnableCulling()
