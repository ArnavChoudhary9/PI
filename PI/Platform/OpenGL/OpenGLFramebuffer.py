from ...Logging import PI_CORE_ASSERT
from ...Renderer import Framebuffer, Texture2D, RenderCommand
from ...Core.Constants import *

from OpenGL.GL import *

class OpenGLFramebuffer(Framebuffer):
    __Specs: Framebuffer.Specs

    __RendererID: int

    __ColorAttachment : Texture2D
    __DepthAttachment : Texture2D

    def __init__(self, specs: Framebuffer.Specs) -> None:
        self.__Specs = specs
        self.__RendererID = 0
        self.__Invalidate()

    def __Invalidate(self) -> None:
        if self.__RendererID != 0:
            glDeleteFramebuffers(1, [self.__RendererID])
            del self.__ColorAttachment
            del self.__DepthAttachment

        if self.__Specs.SwapChainTarget:
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            return

        self.__RendererID = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.__RendererID)

        self.__ColorAttachment: Texture2D = Texture2D.Create(
            int(self.__Specs.Width), int(self.__Specs.Height), PIConstants.RGB
        )
        self.__ColorAttachment.Bind()
        glFramebufferTexture2D(
            GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, 
            self.__ColorAttachment.RendererID, 0
        )

        self.__DepthAttachment: Texture2D = Texture2D.Create(
            int(self.__Specs.Width), int(self.__Specs.Height), PIConstants.DEPTH_STENCIL
        )
        self.__DepthAttachment.Bind()
        glFramebufferTexture2D(
            GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_TEXTURE_2D,
            self.__DepthAttachment.RendererID, 0
        )

        PI_CORE_ASSERT(
            glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE,
            "Framebuffer not complete!!"
        )

    def Resize(self, width: int, height: int) -> None:
        self.__Specs.Width  = width
        self.__Specs.Height = height

        self.__Invalidate()

    @property
    def ColorAttachment0(self) -> Texture2D:
        return self.__ColorAttachment

    @property
    def DepthAttachment(self) -> Texture2D:
        return self.__DepthAttachment

    @property
    def Spec(self) -> Framebuffer.Specs:
        return self.__Specs

    def Bind(self) -> None:
        if not self.__Specs.SwapChainTarget:
            glBindFramebuffer(GL_FRAMEBUFFER, self.__RendererID)
            RenderCommand.Clear()
        
        else: glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def Unbind(self) -> None: glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def __del__(self) -> None:
        glDeleteFramebuffers(1, self.__RendererID)
        del self.__ColorAttachment
        del self.__DepthAttachment
