from ...Renderer.UniformBuffer import UniformBuffer

from OpenGL.GL import glGenBuffers, glNamedBufferData, glBindBufferBase, glDeleteBuffers, glNamedBufferSubData
from OpenGL.GL import GL_DYNAMIC_DRAW, GL_UNIFORM_BUFFER

class OpenGLUniformBuffer(UniformBuffer):
    __slots__ = ("__RendererID",)

    def __init__ (self, size: int, binding: int) -> None:
        self.__RendererID = glGenBuffers(1)
        glNamedBufferData(self.__RendererID, size, None, GL_DYNAMIC_DRAW)
        glBindBufferBase(GL_UNIFORM_BUFFER, binding, self.__RendererID)

    def __del__  (self) -> None: glDeleteBuffers(1, [ self.__RendererID ])

    def SetData(self, data, size: int, offset: int = 0) -> None:
        glNamedBufferSubData(self.__RendererID, offset, size, data)
