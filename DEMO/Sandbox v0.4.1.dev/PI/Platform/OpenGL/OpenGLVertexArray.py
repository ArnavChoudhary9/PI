from ...Renderer import VertexArray, VertexBuffer, IndexBuffer
from ...logger   import PI_CORE_ASSERT

from OpenGL.GL import \
    glGenVertexArrays, glDeleteVertexArrays, \
    glBindVertexArray, glEnableVertexAttribArray, glVertexAttribPointer

class OpenGLVertexArray(VertexArray):
    __RendererID: int = 0

    __VertexBuffers : list = []
    __IndexBuffer   : IndexBuffer

    def __init__(self) -> None:
        self.__RendererID = glGenVertexArrays(1)

    def __del__(self) -> None:
        glDeleteVertexArrays(self.__RendererID)

    def Bind(self) -> None:
        glBindVertexArray(self.__RendererID)
    
    def Unbind(self) -> None:
        glBindVertexArray(0)

    def AddVertexBuffer(self, buffer: VertexBuffer) -> None:
        glBindVertexArray(self.__RendererID)
        buffer.Bind()

        elements = buffer.Layout.Elements
        PI_CORE_ASSERT(bool(len(elements)), "Layout of VertexBuffer if not set!")
          
        for i, element in enumerate(elements):      
            glEnableVertexAttribArray(i)
            glVertexAttribPointer(i,
                element.ComponentCount,
                element.OpenGLBaseType,
                element.Normalized,
                buffer.Layout.Stride,
                element.Offset
            )

        self.__VertexBuffers.append(buffer)

    def SetIndexBuffer(self, buffer: IndexBuffer) -> None:
        glBindVertexArray(self.__RendererID)
        buffer.Bind()

        self.__IndexBuffer = buffer

    @property
    def VertexBuffers(self) -> list:
        return self.__VertexBuffers

    @property
    def IndexBuffer(self) -> IndexBuffer:
        return self.__IndexBuffer
