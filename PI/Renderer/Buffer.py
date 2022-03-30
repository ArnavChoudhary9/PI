from ..Renderer import Renderer, RendererAPI
from ..logger   import PI_CORE_ASSERT

from OpenGL.GL import GL_FLOAT, GL_INT, GL_BOOL
from ctypes    import c_void_p

class ShaderDataType:
    Null,                          \
    Float, Float2, Float3, Float4, \
    Int, Int2, Int3, Int4,         \
    Mat3x3, Mat4x4,                \
    Bool                           \
        = range(0, 12)

def ShaderDataTypeSize(_type: ShaderDataType) -> int:
    if   ( _type == ShaderDataType.Float  ):    return 4
    elif ( _type == ShaderDataType.Float2 ):    return 4 * 2
    elif ( _type == ShaderDataType.Float3 ):    return 4 * 3
    elif ( _type == ShaderDataType.Float4 ):    return 4 * 4
    elif ( _type == ShaderDataType.Int    ):    return 4
    elif ( _type == ShaderDataType.Int2   ):    return 4 * 2
    elif ( _type == ShaderDataType.Int3   ):    return 4 * 3
    elif ( _type == ShaderDataType.Int4   ):    return 4 * 4
    elif ( _type == ShaderDataType.Mat3x3 ):    return 4 * 3 * 3
    elif ( _type == ShaderDataType.Mat4x4 ):    return 4 * 4 * 4
    elif ( _type == ShaderDataType.Bool   ):    return 1

    PI_CORE_ASSERT(False, "Unknown ShaderDataType!")
    return 0

class BufferElement:
    __slots__ = "Name", "Type", \
        "Offset", "Size", \
        "Normalized"

    def __init__(self, _type: ShaderDataType, name: str, normalized: bool=False) -> None:
        self.Name = name
        self.Type = _type

        self.Size = ShaderDataTypeSize(_type)
        self.Normalized = normalized

    @property
    def ComponentCount(self) -> int:
        if   ( self.Type == ShaderDataType.Float  ):    return 1
        elif ( self.Type == ShaderDataType.Float2 ):    return 2
        elif ( self.Type == ShaderDataType.Float3 ):    return 3
        elif ( self.Type == ShaderDataType.Float4 ):    return 4

        elif ( self.Type == ShaderDataType.Int    ):    return 1
        elif ( self.Type == ShaderDataType.Int2   ):    return 2
        elif ( self.Type == ShaderDataType.Int3   ):    return 3
        elif ( self.Type == ShaderDataType.Int4   ):    return 4

        elif ( self.Type == ShaderDataType.Mat3x3 ):    return 9
        elif ( self.Type == ShaderDataType.Mat4x4 ):    return 16

        elif ( self.Type == ShaderDataType.Bool   ):    return 1

        PI_CORE_ASSERT(False, "Unknown ShaderDataType!")
        return 0

    @property
    def OpenGLBaseType(self):
        if   ( self.Type == ShaderDataType.Float  ):     return GL_FLOAT
        elif ( self.Type == ShaderDataType.Float2 ):     return GL_FLOAT
        elif ( self.Type == ShaderDataType.Float3 ):     return GL_FLOAT
        elif ( self.Type == ShaderDataType.Float4 ):     return GL_FLOAT

        elif ( self.Type == ShaderDataType.Int    ):     return GL_INT
        elif ( self.Type == ShaderDataType.Int2   ):     return GL_INT
        elif ( self.Type == ShaderDataType.Int3   ):     return GL_INT
        elif ( self.Type == ShaderDataType.Int4   ):     return GL_INT
        
        elif ( self.Type == ShaderDataType.Mat3x3 ):     return GL_FLOAT
        elif ( self.Type == ShaderDataType.Mat4x4 ):     return GL_FLOAT
        
        elif ( self.Type == ShaderDataType.Bool   ):     return GL_BOOL

        PI_CORE_ASSERT(False, "Unknown ShaderDataType!")
        return 0

class BufferLayout:
    __slots__ = "__Elements", "__Stride"

    def __init__(self, *elements: tuple) -> None:
        self.__Elements = tuple([
            BufferElement(*element) for element in elements
        ])

        self.__CalculateOffsetsAndStride()

    @property
    def Elements(self) -> tuple:
        return self.__Elements

    @property
    def Stride(self) -> int:
        return self.__Stride

    def __CalculateOffsetsAndStride(self) -> None:
        offset = 0
        self.__Stride = 0

        for element in self.__Elements:
            element.Offset = c_void_p(offset)
            offset += element.Size
            self.__Stride += element.Size

class VertexBuffer:
    __slots__ = ("__NativeAPI",)

    def Bind(self) -> None:
        pass
    
    def Unbind(self) -> None:
        pass

    def SetLayout(self, layout: BufferLayout) -> None:
        pass

    @property
    def Layout(self) -> BufferLayout:
        pass

    @staticmethod
    def Init() -> None:
        if (Renderer.GetAPI() == RendererAPI.API.Null):
            PI_CORE_ASSERT(False, "RendererAPI.None is currently not supported!")
            return

        elif (Renderer.GetAPI() == RendererAPI.API.OpenGL):
            from ..Platform.OpenGL.OpenGLBuffer import OpenGLVertexBuffer
            VertexBuffer.__NativeAPI = OpenGLVertexBuffer
            return

        PI_CORE_ASSERT(False, "Unknown RendererAPI!!")
        return None

    @staticmethod
    def Create(vertices: list):
        return VertexBuffer.__NativeAPI(vertices)

class IndexBuffer:
    __slots__ = ("__NativeAPI",)

    def Bind(self) -> None:
        pass
    
    def Unbind(self) -> None:
        pass

    @staticmethod
    def Init() -> None:
        if (Renderer.GetAPI() == RendererAPI.API.Null):
            PI_CORE_ASSERT(False, "RendererAPI.None is currently not supported!")
            return

        elif (Renderer.GetAPI() == RendererAPI.API.OpenGL):
            from ..Platform.OpenGL.OpenGLBuffer import OpenGLIndexBuffer
            IndexBuffer.__NativeAPI = OpenGLIndexBuffer
            return

        PI_CORE_ASSERT(False, "Unknown RendererAPI!!")
        return None

    @staticmethod
    def Create(indices: list):
        return IndexBuffer.__NativeAPI(indices)
