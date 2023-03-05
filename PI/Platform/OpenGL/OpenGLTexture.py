from ...Logging import PI_CORE_ASSERT
from ...Renderer import Texture2D, RenderCommand
from ...Core.Constants import *

from OpenGL.GL import glGenTextures, glBindTextureUnit, glTextureSubImage2D, glTextureParameteri, glTextureStorage2D,\
                      glBindTexture, glTexImage2D, glTexStorage2D, glDeleteTextures

from OpenGL.GL import GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_REPEAT, GL_LINEAR, GL_CLAMP_TO_EDGE, \
                      GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, \
                      GL_RGB8, GL_RGB, GL_RGBA, GL_SRGB, GL_RGBA8, \
                      GL_UNSIGNED_BYTE, GL_NEAREST

from multipledispatch import dispatch
from random import randrange
from PIL import Image

class OpenGLTexture2D(Texture2D):
    __slots__ = "__RendererID", "__Width", "__Height", \
        "__Format", "__DataType", \
        "__Path", "__Name"

    @dispatch(str, int)
    def __init__(self, path: str, format: int) -> None:
        self.__RendererID = None

        self.__Path = path
        image = Image.open(path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        imageByte = image.convert("RGBA").tobytes()

        self.__Width = image.width
        self.__Height = image.height
        
        slashIndex = path.rfind("\\")
        if slashIndex == -1: slashIndex = path.rfind("/")

        dotIndex = path.rfind(".")

        if dotIndex != -1:
            self.__Name = path[slashIndex+1:dotIndex]
        else:
            self.__Name = path[slashIndex+1:]
        
        self.__RendererID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.__RendererID)

        format = PIConstants.ToOpenGLConstant(format)
        _type = GL_RGB8
        dataType = GL_UNSIGNED_BYTE

        if   format == GL_RGBA : _type = GL_RGBA8
        elif format == GL_RGB  : _type = GL_RGB8
        elif format == GL_RED_INTEGER   : _type = GL_RED_INTEGER
        elif format == GL_DEPTH_STENCIL : _type = GL_DEPTH24_STENCIL8
        else: PI_CORE_ASSERT(False, "Invalid texture format.")

        if   format == GL_RGBA : dataType = GL_UNSIGNED_BYTE
        elif format == GL_RGB  : dataType = GL_UNSIGNED_BYTE
        elif format == GL_RED_INTEGER   : dataType = GL_R32I
        elif format == GL_DEPTH_STENCIL : _type = GL_UNSIGNED_INT_24_8
        else: PI_CORE_ASSERT(False, "Invalid texture format.")

        self.__DataType : int = dataType
        self.__Format   : int = format

        glTextureStorage2D(self.__RendererID, 1, _type, image.width, image.height)

        glTextureParameteri(self.__RendererID, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTextureParameteri(self.__RendererID, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTextureParameteri(self.__RendererID, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTextureParameteri(self.__RendererID, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTextureSubImage2D(
            self.__RendererID,
            0, 0, 0, image.width, image.height, format, 
            dataType, imageByte
        )

        RenderCommand.EnableBlending()

        glBindTexture(GL_TEXTURE_2D, 0)

    @dispatch(int, int, int)
    def __init__(self, width: int, height: int, format: int) -> None:
        self.__RendererID = None

        self.__Width = width
        self.__Height = height

        self.__Name = "{}x{}_{}".format(width, height, randrange(0, 1000))
        self.__Path = ""

        self.__RendererID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.__RendererID)

        format = PIConstants.ToOpenGLConstant(format)
        _type = GL_RGB8
        dataType = GL_UNSIGNED_BYTE

        if   format == GL_RGBA : _type = GL_RGBA8
        elif format == GL_RGB  : _type = GL_RGB8
        elif format == GL_RED_INTEGER   : _type = GL_R32I
        elif format == GL_DEPTH_STENCIL : _type = GL_DEPTH24_STENCIL8
        else: PI_CORE_ASSERT(False, "Invalid texture format.")

        if   format == GL_RGBA : dataType = GL_UNSIGNED_BYTE
        elif format == GL_RGB  : dataType = GL_UNSIGNED_BYTE
        elif format == GL_RED_INTEGER   : dataType = GL_R32I
        elif format == GL_DEPTH_STENCIL : dataType = GL_UNSIGNED_INT_24_8
        else: PI_CORE_ASSERT(False, "Invalid texture format.")

        self.__DataType : int = dataType
        self.__Format   : int = format

        glTextureStorage2D(self.__RendererID, 1, _type, width, height)

        glTextureParameteri(self.__RendererID, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTextureParameteri(self.__RendererID, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTextureParameteri(self.__RendererID, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTextureParameteri(self.__RendererID, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def __repr__(self) -> str:
        return self.__Name

    def __del__(self) -> None:
        if self.__RendererID is None: return
        glDeleteTextures(1, [self.__RendererID])

    @property
    def RendererID(self) -> int:
        return self.__RendererID

    @property
    def Name(self) -> int:
        return self.__Name

    @property
    def Path(self) -> int:
        return self.__Path

    @property
    def Width(self) -> int:
        return self.__Width

    @property
    def Height(self) -> int:
        return self.__Height

    def SetData(self, data, size) -> None:
        glTextureSubImage2D(
            self.__RendererID,
            0, 0, 0, self.__Width, self.__Height, self.__Format, 
            self.__DataType, data
        )

    def Bind(self, slot: int=0) -> None:
        glBindTextureUnit(slot, self.__RendererID)

    def Unbind(self) -> None:
        glBindTextureUnit(0, 0)
