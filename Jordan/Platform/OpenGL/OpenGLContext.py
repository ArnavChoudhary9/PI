from ...logger   import JD_CORE_ASSERT, JD_CORE_INFO
from ...Renderer import GraphicsContext

from OpenGL.GL   import GL_RENDERER, GL_VENDOR, GL_VERSION, glGetString
import glfw

class OpenGLContext(GraphicsContext):
    __WindowHandle = None

    def __init__(self, windowHandle) -> None:
        self.__WindowHandle = windowHandle
        JD_CORE_ASSERT(windowHandle != None, "Window handle is null!")

    def Init(self) -> None:
        glfw.make_context_current(self.__WindowHandle)

        JD_CORE_INFO("OpenGL Renderer")
        JD_CORE_INFO("\tVendor     : {}", glGetString(GL_VENDOR)   .decode('utf-8'))
        JD_CORE_INFO("\tRenderer   : {}", glGetString(GL_RENDERER) .decode('utf-8'))
        JD_CORE_INFO("\tVersion    : {}", glGetString(GL_VERSION)  .decode('utf-8'))

    def SwapBuffers(self) -> None:
        glfw.swap_buffers(self.__WindowHandle)
