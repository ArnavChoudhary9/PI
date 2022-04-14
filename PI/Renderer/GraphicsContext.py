from ..Logging.logger  import PI_CORE_ASSERT
from .Renderer import Renderer, RendererAPI

class GraphicsContext:
    def Init(self) -> None:
        pass

    def SwapBuffers(self) -> None:
        pass

    @staticmethod
    def Create(window):
        if Renderer.GetAPI() == RendererAPI.API.Null:
            PI_CORE_ASSERT(False, "RendererAPI.Null is not yet supported!")
            return None

        elif Renderer.GetAPI() == RendererAPI.API.OpenGL:
            from ..Platform.OpenGL import OpenGLContext
            return OpenGLContext(window)
