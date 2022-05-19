from ..Logging.logger  import PI_CORE_ASSERT
from .Renderer import Renderer, RendererAPI

from abc import ABC, abstractmethod

class GraphicsContext(ABC):
    @abstractmethod
    def Init(self) -> None: ...
    @abstractmethod
    def SwapBuffers(self) -> None: ...

    @staticmethod
    def Create(window):
        if Renderer.GetAPI() == RendererAPI.API.Null:
            PI_CORE_ASSERT(False, "RendererAPI.Null is not yet supported!")
            return None

        elif Renderer.GetAPI() == RendererAPI.API.OpenGL:
            from ..Platform.OpenGL import OpenGLContext
            return OpenGLContext(window)
