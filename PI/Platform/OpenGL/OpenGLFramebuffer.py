from ...Logging import PI_CORE_ASSERT
from ...Renderer import Framebuffer, FramebufferAttachments, Texture2D, RenderCommand
from ...Core.Constants import *

from OpenGL.GL import *

from typing import Tuple as _Tuple
from typing import List  as _List

class OpenGLFramebuffer(Framebuffer):
    __Specs: Framebuffer.Specs

    __Attachments     : _List[Texture2D]
    __AttachmentTuple : _Tuple[int]

    __RendererID: int

    def __init__(self, specs: Framebuffer.Specs) -> None:
        self.__Specs = specs

        attachments = sorted(specs.Attachments)
        PI_CORE_ASSERT(len(attachments), "Cannot generate Framebuffer with no attachments")
        self.__AttachmentTuple = attachments
        self.__Attachments = []
        
        self.__RendererID = 0
        self.__Invalidate()

    def __Invalidate(self) -> None:
        if self.__RendererID != 0:
            glDeleteFramebuffers(1, [self.__RendererID])
            for attachment in self.__Attachments:
                del attachment

        if self.__Specs.SwapChainTarget:
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            return

        self.__RendererID = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.__RendererID)

        self.__Attachments.clear()
        for attachmentType, index in zip(self.__AttachmentTuple, range(len(self.__AttachmentTuple))):
            Attachment : Texture2D
            dataType   : int

            # index = (index - self.__AttachmentTuple.index(FramebufferAttachments.Color))
            # self.__AttachmentTuple.

            if attachmentType == FramebufferAttachments.Color:
                Attachment: Texture2D = Texture2D.Create(
                    int(self.__Specs.Width), int(self.__Specs.Height), PIConstants.RGB
                )
                dataType = GL_COLOR_ATTACHMENT0 + index
            elif attachmentType == FramebufferAttachments.ColorAlpha:
                Attachment: Texture2D = Texture2D.Create(
                    int(self.__Specs.Width), int(self.__Specs.Height), PIConstants.RGBA
                )
                dataType = GL_COLOR_ATTACHMENT0 + index
            elif attachmentType == FramebufferAttachments.RedInteger:
                Attachment: Texture2D = Texture2D.Create(
                    int(self.__Specs.Width), int(self.__Specs.Height), PIConstants.PI_RED_INTEGER
                )
                dataType = GL_COLOR_ATTACHMENT0 + index
            elif attachmentType == FramebufferAttachments.DepthStencil:
                Attachment: Texture2D = Texture2D.Create(
                    int(self.__Specs.Width), int(self.__Specs.Height), PIConstants.DEPTH_STENCIL
                )
                dataType = GL_DEPTH_STENCIL_ATTACHMENT
            
            else: PI_CORE_ASSERT(False, "Wrong Framebuffer Attachment type!")

            Attachment.Bind()
            glFramebufferTexture2D(
                GL_FRAMEBUFFER, dataType, GL_TEXTURE_2D,
                Attachment.RendererID, 0
            )

            self.__Attachments.append(Attachment)

        PI_CORE_ASSERT(
            glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE,
            "Framebuffer not complete!!"
        )

    def Resize(self, width: int, height: int) -> None:
        self.__Specs.Width  = width
        self.__Specs.Height = height

        self.__Invalidate()

    @property
    def Attachments(self) -> _List[Texture2D]: return self.__Attachments

    @property
    def Spec(self) -> Framebuffer.Specs:
        return self.__Specs

    def GetColorAttachment(self, index) -> Texture2D:
        return self.__Attachments[index]

    def Bind(self) -> None:
        if not self.__Specs.SwapChainTarget: glBindFramebuffer(GL_FRAMEBUFFER, self.__RendererID)
        else: glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def Unbind(self) -> None: glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def __del__(self) -> None:
        glDeleteFramebuffers(1, [self.__RendererID])
        for attachment in self.__Attachments:
            del attachment
