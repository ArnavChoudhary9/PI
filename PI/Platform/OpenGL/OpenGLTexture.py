from ...Logging import PI_CORE_ASSERT, PI_CLIENT_ERROR
from ...Renderer import Texture2D, RenderCommand, TextureSpecification
from ...Core.Constants import *

from OpenGL.GL import glGenTextures, glBindTextureUnit, glTextureSubImage2D, glTextureParameteri, glTextureStorage2D,\
                      glBindTexture, glTexImage2D, glTexStorage2D, glDeleteTextures

from OpenGL.GL import GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, \
                      GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER

from multipledispatch import dispatch
from random import randrange
from PIL import Image

class OpenGLTexture2D(Texture2D):
    __slots__ = "__RendererID", "__Width", "__Height", \
        "__Format", "__DataType", \
        "__Path", "__Name"

    @dispatch(str, TextureSpecification)
    def __init__(self, path: str, spec: TextureSpecification) -> None:
        self.__RendererID = None

        self.__Path = path
        try:
            image = Image.open(path)
        except FileNotFoundError as e:
            PI_CLIENT_ERROR("File: {} Not Found!!", path)
            raise e
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
        self.__Specification: TextureSpecification = spec

        glTextureStorage2D(self.__RendererID, 1, spec.TextureSize, image.width, image.height)

        glTextureParameteri(self.__RendererID, GL_TEXTURE_WRAP_S, spec.WrapS)
        glTextureParameteri(self.__RendererID, GL_TEXTURE_WRAP_T, spec.WrapT)

        glTextureParameteri(self.__RendererID, GL_TEXTURE_MIN_FILTER, spec.MinFilter)
        glTextureParameteri(self.__RendererID, GL_TEXTURE_MAG_FILTER, spec.MagFilter)

        glTextureSubImage2D(
            self.__RendererID,
            0, 0, 0, image.width, image.height, spec.TextureFormat, 
            spec.DataType, imageByte
        )

        RenderCommand.EnableBlending()
        glBindTexture(GL_TEXTURE_2D, 0)

    @dispatch(int, int, TextureSpecification)
    def __init__(self, width: int, height: int, spec: TextureSpecification) -> None:
        self.__RendererID = None

        self.__Width = width
        self.__Height = height

        self.__Name = "{}x{}_{}".format(width, height, randrange(0, 1000))
        self.__Path = ""

        self.__RendererID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.__RendererID)
        self.__Specification: TextureSpecification = spec

        glTextureStorage2D(self.__RendererID, 1, spec.TextureSize, width, height)

        glTextureParameteri(self.__RendererID, GL_TEXTURE_WRAP_S, spec.WrapS)
        glTextureParameteri(self.__RendererID, GL_TEXTURE_WRAP_T, spec.WrapT)

        glTextureParameteri(self.__RendererID, GL_TEXTURE_MIN_FILTER, spec.MinFilter)
        glTextureParameteri(self.__RendererID, GL_TEXTURE_MAG_FILTER, spec.MagFilter)

    def __repr__(self) -> str: return self.__Name
    def __del__(self) -> None:
        if self.__RendererID is None: return
        glDeleteTextures(1, [self.__RendererID])

    @property
    def RendererID(self) -> int: return self.__RendererID
    @property
    def Name(self) -> int: return self.__Name
    @property
    def Path(self) -> int: return self.__Path
    @property
    def Width(self) -> int: return self.__Width
    @property
    def Height(self) -> int: return self.__Height
    @property
    def Specifications(self) -> int: return self.__Specification

    def SetData(self, data, size) -> None:
        glTextureSubImage2D(
            self.__RendererID,
            0, 0, 0, self.__Width, self.__Height, self.__Specification.TextureFormat, 
            self.__Specification.DataType, data
        )

    def Bind(self, slot: int=0) -> None: glBindTextureUnit(slot, self.__RendererID)
    def Unbind(self) -> None: glBindTextureUnit(0, 0)
