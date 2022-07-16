from ..Core.Window import Window, OS
from ..Logging.logger import PI_CORE_ASSERT

class RendererAPI:
    class API:
        Null = 0
        OpenGL = 1

    __slots__ = ("__API",)

    @staticmethod
    def Init() -> None:
        if (Window.GetOS() == OS.Null):
            PI_CORE_ASSERT(False, "OS.Null is currently not supported!")
            return

        elif (Window.GetOS() == OS.Windows):
            RendererAPI.__API = RendererAPI.API.OpenGL
            return

        PI_CORE_ASSERT(False, "Unknown RendererAPI!!")
        return None

    @staticmethod
    def SetClearColor(*args) -> None: ...
    @staticmethod
    def Clear() -> None: ...
    @staticmethod
    def DrawIndexed(vertexArray, indices: int=None) -> None: ...
    @staticmethod
    def DrawLines(vertexArray, indices: int) -> None: ...
    @staticmethod
    def EnableDepth() -> None: ...
    @staticmethod
    def EnableBlending() -> None: ...
    @staticmethod
    def EnableCulling() -> None: ...

    @staticmethod
    def GetAPI() -> int: return RendererAPI.__API

    @staticmethod
    def SetAPI(api: int) -> None: RendererAPI.__API = api
