from ...Renderer.Buffer import VertexBuffer, IndexBuffer, BufferLayout

from OpenGL.GL import glGenBuffers, glBufferData, glDeleteBuffers, glBindBuffer, glBufferSubData
from OpenGL.GL import GL_ARRAY_BUFFER, GL_STATIC_DRAW, GL_ELEMENT_ARRAY_BUFFER, GL_DYNAMIC_DRAW

import ctypes
import numpy as np
from multipledispatch import dispatch

class OpenGLVertexBuffer(VertexBuffer):
    __slots__ = "__RendererID", "__itemsize", \
        "__Layout"

    @dispatch(list)
    def __init__(self, vertices: list) -> None:
        vertices: np.ndarray = np.array(vertices, dtype=np.float32)
        self.__itemsize = vertices.itemsize

        self.__RendererID = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.__RendererID)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    @dispatch(int)
    def __init__(self, size: int) -> None:
        vertices = np.zeros((size,))
        self.__itemsize = size

        self.__RendererID = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.__RendererID)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, ctypes.c_void_p(None), GL_DYNAMIC_DRAW)

    def __del__(self) -> None:
        glDeleteBuffers(1, [self.__RendererID])

    @property
    def itemsize(self) -> int:
        return self.__itemsize

    @property
    def RendererID(self) -> int:
        return self.__RendererID

    def Bind(self) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, self.__RendererID)

    def Unbind(self) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def SetLayout(self, layout: BufferLayout) -> None:
        self.__Layout = layout

    def SetData(self, data: np.ndarray) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, self.__RendererID)
        glBufferSubData(GL_ARRAY_BUFFER, 0, data.nbytes, data.tobytes())

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
        glDeleteBuffers(1, [self.__RendererID])

    @property
    def RendererID(self) -> int:
        return self.__RendererID

    @property
    def Count(self) -> int:
        return self.__Count

    def Bind(self) -> None:
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.__RendererID)

    def Unbind(self) -> None:
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
