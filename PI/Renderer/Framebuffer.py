from ..Renderer import Renderer, RendererAPI
from ..logger   import PI_CORE_ASSERT

class Framebuffer:
    class Specs:
        Width  : int
        Height : int

        Samples : int = 1
        SwapChainTarget = False

        def __init__(self, width: int, height: int) -> None:
            self.Width  = width
            self.Height = height

    __slots__ = ("__NativeAPI",)

    @staticmethod
    def Init() -> None:
        if (Renderer.GetAPI() == RendererAPI.API.Null):
            PI_CORE_ASSERT(False, "RendererAPI.None is currently not supported!")
            return

        elif (Renderer.GetAPI() == RendererAPI.API.OpenGL):
            from ..Platform.OpenGL.OpenGLFramebuffer import OpenGLFramebuffer
            Framebuffer.__NativeAPI = OpenGLFramebuffer
            return

        PI_CORE_ASSERT(False, "Unknown RendererAPI!!")
        return None

    def Bind(self) -> None:
        pass
    
    def Unbind(self) -> None:
        pass

    @property
    def Spec(self):
        return self.__Specs

    @staticmethod
    def Create(specs):
        return Framebuffer.__NativeAPI(specs)
