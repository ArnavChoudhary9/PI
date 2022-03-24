from .RendererAPI import RendererAPI

class RenderCommand:
    __RendererAPI: RendererAPI

    @staticmethod
    def SetRendererAPI(rendererAPI: RendererAPI) -> None:
        RenderCommand.__RendererAPI = rendererAPI

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
