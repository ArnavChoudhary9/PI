from ...Renderer import RendererAPI

from OpenGL.GL import glClear, glClearColor, glDrawElements, glEnable, glBlendFunc, glViewport
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_TRIANGLES, GL_UNSIGNED_INT, \
                      GL_DEPTH_TEST, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA

from ctypes import c_void_p

class OpenGLRendererAPI(RendererAPI):
    @staticmethod
    def SetClearColor(*args) -> None:
        glClearColor(*args)

    @staticmethod
    def Clear() -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    @staticmethod
    def DrawIndexed(vertexArray, indices: int=None) -> None:
        if indices is None:
            glDrawElements(GL_TRIANGLES, vertexArray.IndexBuffer.Count, GL_UNSIGNED_INT, c_void_p(0))
            return
            
        glDrawElements(GL_TRIANGLES, indices, GL_UNSIGNED_INT, c_void_p(0))

    @staticmethod
    def Resize(x: int, y: int, width: int, height: int) -> None:
        glViewport(x, y, width, height)

    @staticmethod
    def EnableDepth() -> None:
        glEnable(GL_DEPTH_TEST)

    @staticmethod
    def EnableBlending() -> None:
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
