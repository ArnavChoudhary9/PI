from ...Logging import PI_CORE_ASSERT, PI_CORE_WARN
from ...Renderer import Framebuffer
from ...Core.Constants import *

from OpenGL.GL import *

from typing import List  as _List

class Utils:
    @staticmethod
    def TextureTarget(multisampled: bool) -> int: return GL_TEXTURE_2D_MULTISAMPLE if multisampled else GL_TEXTURE_2D
    
    @staticmethod
    def CreateTextures(multisampled: bool, count: int) -> int:
        texture = glGenTextures(count)

        if count == 1: texture = [texture]
        else: texture = list(texture)

        return texture

    @staticmethod
    def BindTexture(multisampled: bool, id: int) -> None: glBindTexture(Utils.TextureTarget(multisampled), id)

    @staticmethod
    def AttachColorTexture(id: int, samples: int, internalFormat: int, format: int, width: int, height: int, index: int):
        multisampled: bool = samples > 1
        if multisampled:
            glTexImage2DMultisample(GL_TEXTURE_2D_MULTISAMPLE, samples, internalFormat, width, height, GL_FALSE)
        else:
            glTexImage2D(GL_TEXTURE_2D, 0, internalFormat, width, height, 0, format, GL_UNSIGNED_BYTE, None)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0 + index, Utils.TextureTarget(multisampled), id, 0)

    @staticmethod
    def AttachDepthTexture(id: int, samples: int, format: int, attachmentType: int, width: int, height: int):
        width = int(width)
        height = int(height)

        multisampled: bool = samples > 1
        if multisampled:
            glTexImage2DMultisample(GL_TEXTURE_2D_MULTISAMPLE, samples, format, width, height, GL_FALSE)
        else:
            glTexStorage2D(GL_TEXTURE_2D, 1, format, width, height)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glFramebufferTexture2D(GL_FRAMEBUFFER, attachmentType, Utils.TextureTarget(multisampled), id, 0)

    def IsDepthFormat(format: Framebuffer.TextureFormat):
        if format == Framebuffer.TextureFormat.DEPTH24STENCIL8: return True
        else: return False

    def PIFBTextureFormatToGL(format: Framebuffer.TextureFormat):
        if   format == Framebuffer.TextureFormat.RGBA8       : return GL_RGBA8
        elif format == Framebuffer.TextureFormat.RED_INTEGER : return GL_RED_INTEGER

        PI_CORE_ASSERT(False, "Invalid texture format.")
        return 0

_MaxFramebufferSize : int = 8192

class OpenGLFramebuffer(Framebuffer):
    __Specs: Framebuffer.Specs

    __ColorAttachmentsSpecs : _List[Framebuffer.TextureSpecification]
    __DepthAttachmentSpecs  : Framebuffer.TextureFormat = Framebuffer.TextureFormat.NULL

    __ColorAttachments      : _List[int]
    __DepthAttachment       : int = 0
    
    __RendererID: int

    def __init__(self, specs: Framebuffer.Specs) -> None:
        self.__Specs = specs

        self.__RendererID = 0
        self.__ColorAttachmentsSpecs = []
        self.__ColorAttachments = []

        for spec in specs.Attachments.Attachments:
            if not Utils.IsDepthFormat(spec.TextureFormat.TextureFormat):
                self.__ColorAttachmentsSpecs.append(spec)
            else:
                self.__DepthAttachmentSpecs = spec

        self.Invalidate()

    def Invalidate(self) -> None:
        if self.__RendererID:
            glDeleteFramebuffers(1, [self.__RendererID])
            glDeleteTextures(self.__ColorAttachments)
            glDeleteTextures([self.__DepthAttachment])

            self.__ColorAttachments = []
            self.__DepthAttachment = 0

        self.__RendererID = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.__RendererID)

        multisample = self.__Specs.Samples > 1

        # Attachments
        if len(self.__ColorAttachmentsSpecs):
            self.__ColorAttachments = Utils.CreateTextures(multisample, len(self.__ColorAttachmentsSpecs))

            for attachment, spec in zip(self.__ColorAttachments, self.__ColorAttachmentsSpecs):
                Utils.BindTexture(multisample, attachment)

                if spec.TextureFormat.TextureFormat == Framebuffer.TextureFormat.RGBA8:
                    Utils.AttachColorTexture(attachment, self.__Specs.Samples, GL_RGBA8, GL_RGBA,
                        self.__Specs.Width, self.__Specs.Height, self.__ColorAttachmentsSpecs.index(spec))

                elif spec.TextureFormat.TextureFormat == Framebuffer.TextureFormat.RED_INTEGER:
                    Utils.AttachColorTexture(attachment, self.__Specs.Samples, GL_R32I, GL_RED_INTEGER,
                        self.__Specs.Width, self.__Specs.Height, self.__ColorAttachmentsSpecs.index(spec))

        if self.__DepthAttachmentSpecs.TextureFormat != Framebuffer.TextureFormat.NULL:
            self.__DepthAttachment = Utils.CreateTextures(multisample, 1)[0]
            Utils.BindTexture(multisample, self.__DepthAttachment)

            if self.__DepthAttachmentSpecs.TextureFormat.TextureFormat == Framebuffer.TextureFormat.DEPTH24STENCIL8:
                Utils.AttachDepthTexture(self.__DepthAttachment, self.__Specs.Samples, GL_DEPTH24_STENCIL8,
                    GL_DEPTH_STENCIL_ATTACHMENT, self.__Specs.Width, self.__Specs.Height)

        if len(self.__ColorAttachments) > 1:
            PI_CORE_ASSERT(len(self.__ColorAttachments) <= 4, "There can be atmost 4 color attachment")
            buffers = [ GL_COLOR_ATTACHMENT0, GL_COLOR_ATTACHMENT1, GL_COLOR_ATTACHMENT2, GL_COLOR_ATTACHMENT3 ]
            glDrawBuffers(len(self.__ColorAttachments), buffers)

        elif len(self.__ColorAttachments) == 0:
            # Only depth-pass
            glDrawBuffer(GL_NONE)
        
        PI_CORE_ASSERT(glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE, "Framebuffer is incomplete!")
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def Resize(self, width: int, height: int) -> None:
        if width == 0 or height == 0 or width > _MaxFramebufferSize or height > _MaxFramebufferSize:
            PI_CORE_WARN("Attempting to resize framebuffer to {}, {}", width, height)
            return

        self.__Specs.Width  = width
        self.__Specs.Height = height

        self.Invalidate()

    def ReadPixel(self, attachmentIndex: int, x: int, y: int) -> None:
        PI_CORE_ASSERT(attachmentIndex < len(self.__ColorAttachments), "Index must be less than attachments length")
        glReadBuffer(GL_COLOR_ATTACHMENT0 + attachmentIndex)
        return bytes(glReadPixels(x, y, 1, 1, GL_RED_INTEGER, GL_INT))
        # return glReadPixels(x, y, 1, 1, GL_RGBA, GL_BYTE)

    @property
    def Attachments(self) -> _List[int]: return self.__ColorAttachments

    @property
    def Spec(self) -> Framebuffer.Specs:
        return self.__Specs

    def GetColorAttachment(self, index=0) -> int:
        PI_CORE_ASSERT(index < len(self.__ColorAttachments), "Index must be less than attachments length")
        return self.__ColorAttachments[index]

    def ClearAttachment(self, attachmentIndex: int, value: bytes) -> bytes:
        PI_CORE_ASSERT(attachmentIndex < len(self.__ColorAttachments), "Cannot generate Framebuffer with no attachments")

        spec = self.__ColorAttachmentsSpecs[attachmentIndex]
        glClearTexImage(self.__ColorAttachments[attachmentIndex], 0,
            Utils.PIFBTextureFormatToGL(spec.TextureFormat.TextureFormat), GL_INT, value)

    def Bind(self) -> None:
        if not self.__Specs.SwapChainTarget: glBindFramebuffer(GL_FRAMEBUFFER, self.__RendererID)
        else: glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def Unbind(self) -> None: glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def __del__(self) -> None:
        glDeleteFramebuffers(1, [self.__RendererID])
        glDeleteTextures(self.__ColorAttachments)
        glDeleteTextures([self.__DepthAttachment])
