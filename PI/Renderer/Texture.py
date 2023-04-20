from ..Logging.logger import PI_CORE_ASSERT
from ..Core.Constants import *
from .RendererAPI import RendererAPI

from multipledispatch import dispatch

class TextureFormat:
    NULL: int = 0

    RGBA8: int = PIConstants.RGBA
    RED_INTEGER: int = PIConstants.RED_INTEGER
    
    DEPTH24STENCIL8: int = PIConstants.DEPTH24_STENCIL8

    DEPTH: int = DEPTH24STENCIL8

class TextureSpecification:
    def __init__(self, format: int=PIConstants.RGBA,
        textureSize: int=PIConstants.RGBA8, dataType: int=PIConstants.UNSIGNED_BYTE,
        wrapS: int=PIConstants.REPEAT, wrapT: int=PIConstants.REPEAT, wrapR: int=PIConstants.REPEAT,
        magFilter: int=PIConstants.LINEAR, minFilter: int=PIConstants.LINEAR
    ) -> None:
        self.TextureFormat, self.TextureSize, self.DataType = format, textureSize, dataType
        self.WrapS, self.WrapT, self.WrapR = wrapS, wrapT, wrapR
        self.MagFilter, self.MinFilter     = magFilter, minFilter

class Texture:
    @staticmethod
    def Init() -> None: Texture2D.Init()
    @property
    def RendererID(self) -> int: return self.__RendererID
    @property
    def Name(self) -> int: return self.__Name
    def __del__(self) -> None: pass
    @property
    def Width(self) -> int: pass
    @property
    def Height(self) -> int: pass
    def SetData(self, data, size) -> None: pass
    def Bind(self, slot: int=0) -> None: pass
    def Unbind(self) -> None: pass

class Texture2D(Texture):
    __slots__ = ("__NativeAPI",)

    @staticmethod
    def Init() -> None:
        if (RendererAPI.GetAPI() == RendererAPI.API.Null):
            PI_CORE_ASSERT(False, "RendererAPI.None is currently not supported!")
            return

        elif (RendererAPI.GetAPI() == RendererAPI.API.OpenGL):
            from ..Platform.OpenGL.OpenGLTexture import OpenGLTexture2D
            Texture2D.__NativeAPI = OpenGLTexture2D
            return

        PI_CORE_ASSERT(False, "Unknown RendererAPI!!")
        return None

    @staticmethod
    @dispatch(str)
    def Create(texturePath: str): return Texture2D.__NativeAPI(texturePath, TextureSpecification())
    @staticmethod
    @dispatch(str, int)
    def Create(texturePath: str, spec: TextureSpecification): return Texture2D.__NativeAPI(texturePath, spec)
    @staticmethod
    @dispatch(int, int)
    def Create(width: int, height: int): return Texture2D.__NativeAPI(width, height, TextureSpecification())
    @staticmethod
    @dispatch(int, int, int)
    def Create(width: int, height: int, spec: TextureSpecification): return Texture2D.__NativeAPI(width, height, spec)
