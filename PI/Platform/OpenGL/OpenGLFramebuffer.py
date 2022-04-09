from ...Renderer import Framebuffer

class OpenGLFramebuffer(Framebuffer):
    __Specs: Framebuffer.Specs

    def __init__(self, specs: Framebuffer.Specs) -> None:
        self.__Specs = specs
