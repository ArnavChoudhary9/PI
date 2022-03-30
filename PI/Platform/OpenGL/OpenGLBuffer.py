from ...Renderer.Buffer import VertexBuffer, IndexBuffer, BufferLayout

from OpenGL.GL import glGenBuffers, glBufferData, glDeleteBuffers, glBindBuffer
from OpenGL.GL import GL_ARRAY_BUFFER, GL_STATIC_DRAW, GL_ELEMENT_ARRAY_BUFFER

import numpy as np

class OpenGLVertexBuffer(VertexBuffer):
    __slots__ = "__RendererID", "__itemsize", \
        "__Layout"

    def __init__(self, vertices: list) -> None:
        vertices: np.ndarray = np.array(vertices, dtype=np.float32)
        self.__itemsize = vertices.itemsize

        self.__RendererID = glGenBuffers(1)
        self.Bind()
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    def __del__(self) -> None:
        glDeleteBuffers(self.__RendererID)

    @property
    def itemsize(self) -> int:
        return self.__itemsize

    def Bind(self) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, self.__RendererID)

    def Unbind(self) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def SetLayout(self, layout: BufferLayout) -> None:
        self.__Layout = layout

    @property
    def Layout(self) -> BufferLayout:
        return self.__Layout

class OpenGLIndexBuffer(IndexBuffer):
    __RendererID : int
    __Count      : int

    def __init__(self, indices: list) -> None:
        indices: np.ndarray = np.array(indices, dtype=np.uint32)
        self.__Count = len(indices)

        self.__RendererID = glGenBuffers(1)
        self.Bind()
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    def __del__(self) -> None:
        glDeleteBuffers(self.__RendererID)

    @property
    def Count(self) -> int:
        return self.__Count

    def Bind(self) -> None:
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.__RendererID)

    def Unbind(self) -> None:
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
