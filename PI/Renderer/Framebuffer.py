from ..Renderer import Renderer, RendererAPI, Texture2D, RenderCommand
from ..Logging.logger   import PI_CORE_ASSERT

from abc import ABC, abstractmethod
from dataclasses import dataclass
from contextlib  import contextmanager

from typing import Tuple as _Tuple
from typing import List  as _List

@dataclass(frozen=True)
class FramebufferAttachments:
    Color: int = 0
    ColorAlpha: int = 1
    RedInteger: int = 2
    
    DepthStencil: int = 3
    Depth: int = DepthStencil

class Framebuffer(ABC):
    class Specs:
        Width  : int
        Height : int

        Attachments : _Tuple[int]

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
    def Attachments(self) -> _List[Texture2D]: ...
    @property
    def Spec(self) -> Specs: ...

    @abstractmethod
    def Bind(self) -> None: ...
    @abstractmethod
    def GetColorAttachment(self, index) -> Texture2D: ...
    @abstractmethod
    def Unbind(self) -> None: ...
    @abstractmethod
    def Resize(self, width: int, height: int) -> None: ...

    @staticmethod
    def Create(specs: Specs):
        return Framebuffer.__NativeAPI(specs)

@contextmanager
def BindFramebuffer(framebuffer: Framebuffer, clearColor: _Tuple[int]=(0.1, 0.1, 0.1, 1.0)) -> Framebuffer:
    try:
        framebuffer.Bind()

        if len(clearColor) == 3: clearColor = (*clearColor, 1.0)
        
        RenderCommand.SetClearColor(*clearColor)
        RenderCommand.Clear()

        yield framebuffer
        
    finally: framebuffer.Unbind()
