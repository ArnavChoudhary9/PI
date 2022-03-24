from ...Renderer import Texture2D, RenderCommand

from OpenGL.GL import glGenTextures, glBindTextureUnit, glTextureSubImage2D, glTextureParameteri, glTextureStorage2D,\
                      glBindTexture
from OpenGL.GL import GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_REPEAT, GL_LINEAR, \
                      GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, \
                      GL_RGB8, GL_RGB, GL_RGBA, GL_SRGB, GL_RGBA8, \
                      GL_UNSIGNED_BYTE, GL_NEAREST

from PIL import Image

class OpenGLTexture2D(Texture2D):
    __RendererID : int
    __Width  : int
    __Height : int

    __Path: str

    def __init__(self, path: str) -> None:
        self.__Path = path
        image = Image.open(path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        imageByte = image.convert("RGBA").tobytes()

        self.__Width = image.width
        self.__Height = image.height
        
        self.__RendererID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.__RendererID)

        glTextureStorage2D(self.__RendererID, 1, GL_RGBA8, image.width, image.height)

        glTextureParameteri(self.__RendererID, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTextureParameteri(self.__RendererID, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTextureParameteri(self.__RendererID, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTextureParameteri(self.__RendererID, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTextureSubImage2D(
            self.__RendererID,
            0, 0, 0, image.width, image.height, GL_RGBA, 
            GL_UNSIGNED_BYTE, imageByte
        )

        RenderCommand.EnableBlending()

        glBindTexture(GL_TEXTURE_2D, 0)

    @property
    def Width(self) -> int:
        return self.__Width

    @property
    def Height(self) -> int:
        return self.__Height

    def Bind(self, slot: int=0) -> None:
        glBindTextureUnit(0, self.__RendererID)

    def Unbind(self) -> None:
        glBindTextureUnit(0, 0)
