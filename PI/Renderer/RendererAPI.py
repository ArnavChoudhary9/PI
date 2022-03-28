from ..Window import Window, OS
from ..logger import PI_CORE_ASSERT

class RendererAPI:
    class API:
        Null = 0
        OpenGL = 1

    __API: int

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
    def SetClearColor(*args) -> None:
        pass

    @staticmethod
    def Clear() -> None:
        pass

    @staticmethod
    def DrawIndexed(vertexArray) -> None:
        pass

    @staticmethod
    def EnableDepth() -> None:
        pass

    @staticmethod
    def EnableBlending() -> None:
        pass

    @staticmethod
    def GetAPI() -> int:
        return RendererAPI.__API

    @staticmethod
    def SetAPI(api: int) -> None:
        RendererAPI.__API = api
