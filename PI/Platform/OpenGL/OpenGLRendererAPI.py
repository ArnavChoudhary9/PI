from ...Renderer import RendererAPI

from OpenGL.GL import glClear, glClearColor, glDrawElements, glDrawArrays, glEnable, glBlendFunc, glViewport, \
                      glCullFace, glFrontFace
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_TRIANGLES, GL_LINES, \
                      GL_UNSIGNED_INT, GL_DEPTH_TEST, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, \
                      GL_CULL_FACE, GL_FRONT, GL_BACK, GL_FRONT_AND_BACK, GL_CW, GL_CCW

from ctypes import c_void_p

class OpenGLRendererAPI(RendererAPI):
    __ClearFlags: int = 0

    @staticmethod
    def SetClearColor(*args) -> None:
        glClearColor(*args)
        OpenGLRendererAPI.__ClearFlags |= GL_COLOR_BUFFER_BIT

    @staticmethod
    def Clear() -> None: glClear(OpenGLRendererAPI.__ClearFlags)

    @staticmethod
    def DrawIndexed(vertexArray, indices: int=None) -> None:
        vertexArray.Bind()

        if indices is None:
            glDrawElements(GL_TRIANGLES, vertexArray.IndexBuffer.Count, GL_UNSIGNED_INT, c_void_p(0))
            return
            
        glDrawElements(GL_TRIANGLES, indices, GL_UNSIGNED_INT, c_void_p(0))

    @staticmethod
    def DrawLines(vertexArray, indices: int) -> None:
        vertexArray.Bind()
        glDrawArrays(GL_LINES, 0, indices)

    @staticmethod
    def Resize(x: int, y: int, width: int, height: int) -> None: glViewport(int(x), int(y), int(width), int(height))

    @staticmethod
    def EnableDepth() -> None:
        glEnable(GL_DEPTH_TEST)
        OpenGLRendererAPI.__ClearFlags |= GL_DEPTH_BUFFER_BIT

    @staticmethod
    def EnableBlending() -> None:
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    @staticmethod
    def EnableCulling() -> None:
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)
