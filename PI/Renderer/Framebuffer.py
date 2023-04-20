from .RendererAPI import RendererAPI
from ..Logging.logger   import PI_CORE_ASSERT
from .Texture import TextureSpecification

from abc import ABC, abstractmethod, abstractproperty

from typing import List  as _List

class Framebuffer:
    class AttachmentSpecification : ...      # Forward decleration
    class TextureSpecification    : ...      # Forward decleration

class Framebuffer(ABC):
    class AttachmentSpecification:
        Attachments : _List[TextureSpecification]
        def __init__(self, *attachments) -> None:
            self.Attachments : _List[TextureSpecification] = list(attachments)

    class Specs:
        Width  : int
        Height : int

        AttachmentSpecification: Framebuffer.AttachmentSpecification = None

        Samples : int = 1
        SwapChainTarget = False

        def __init__(self) -> None: pass

    __slots__ = ("__NativeAPI",)

    @staticmethod
    def Init() -> None:
        if (RendererAPI.GetAPI() == RendererAPI.API.Null):
            PI_CORE_ASSERT(False, "RendererAPI.None is currently not supported!")
            return

        elif (RendererAPI.GetAPI() == RendererAPI.API.OpenGL):
            from ..Platform.OpenGL.OpenGLFramebuffer import OpenGLFramebuffer
            Framebuffer.__NativeAPI = OpenGLFramebuffer
            return

        PI_CORE_ASSERT(False, "Unknown RendererAPI!!")
        return None

    @abstractproperty
    def Attachments(self) -> _List[int]: ...
    @abstractproperty
    def Spec(self) -> Specs: ...

    @abstractmethod
    def Bind(self) -> None: ...
    @abstractmethod
    def ClearAttachment(self, attachmentIndex: int, value: bytes) -> bytes: ...
    @abstractmethod
    def GetColorAttachment(self, index=0) -> int: ...
    @abstractmethod
    def Unbind(self) -> None: ...
    @abstractmethod
    def Resize(self, width: int, height: int) -> None: ...
    @abstractmethod
    def ReadPixel(self, attachmentIndex: int, x: int, y: int) -> bytes: ...

    def __enter__ (self)        -> None: self.Bind()
    def __exit__  (self, *args) -> None: self.Unbind()

    @staticmethod
    def Create(specs: Specs):
        return Framebuffer.__NativeAPI(specs)
