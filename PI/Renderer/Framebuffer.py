from ..Renderer import Renderer, RendererAPI, Texture2D
from ..Logging.logger   import PI_CORE_ASSERT

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

    @property
    def ColorAttachment0(self) -> Texture2D: ...
    @property
    def DepthAttachment(self) -> Texture2D: ...
    @property
    def Spec(self) -> Specs: ...

    def Bind(self) -> None: ...
    def Unbind(self) -> None: ...
    def Resize(self, width: int, height: int) -> None: ...

    @staticmethod
    def Create(specs):
        return Framebuffer.__NativeAPI(specs)
