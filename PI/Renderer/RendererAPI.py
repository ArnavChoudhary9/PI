class RendererAPI:
    class API:
        Null = 0
        OpenGL = 1

    __API: int

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
