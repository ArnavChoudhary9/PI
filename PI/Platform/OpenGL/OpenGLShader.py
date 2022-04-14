from ...Renderer import Shader

from OpenGL.GL import glDeleteProgram, glUseProgram,\
    glGetUniformLocation, \
    glUniformMatrix4fv, glUniform4f, glUniform3f, glUniform2f, glUniform1f, glUniform1i
from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, GL_FALSE

from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr

class OpenGLShader(Shader):
    __slots__ = "__RendererID", "__Name", "__UniformLocations"

    def __init__(self, shaderFile: str) -> None:
        src = ""

        slashIndex = shaderFile.rfind("\\")
        if slashIndex == -1: slashIndex = shaderFile.rfind("/")

        dotIndex = shaderFile.rfind(".")

        if dotIndex != -1:
            self.__Name = shaderFile[slashIndex+1:dotIndex]
        else:
            self.__Name = shaderFile[slashIndex+1:]

        with open(shaderFile, 'r') as file:
            src = file.read()

        src = src.split('\n')

        vertexSrc   : list = []
        fragmentSrc : list = []

        index = 0
        while (len(src) > index):
            shaderType = src[index].split(" ")[1].lower()

            if shaderType == "vertex" or shaderType == "vert":
                index += 1
                while (len(src) > index and src[index].find("#type") < 0):
                    vertexSrc.append(f"{src[index]}\n")
                    index += 1
                    
            if shaderType == "pixel" or shaderType == "frag" or shaderType == "fragment":
                index += 1
                while (len(src) > index and src[index].find("#type") < 0):
                    fragmentSrc.append(f"{src[index]}\n")
                    index += 1

        vertexSrc   = "".join(vertexSrc)
        fragmentSrc = "".join(fragmentSrc)

        self.__RendererID = compileProgram(
            compileShader(vertexSrc, GL_VERTEX_SHADER),
            compileShader(fragmentSrc, GL_FRAGMENT_SHADER)
        )

        self.__UniformLocations: dict = {}

    def __repr__(self) -> str:
        return self.__Name

    @property
    def RendererID(self) -> int:
        return self.__RendererID

    @property
    def Name(self) -> int:
        return self.__Name

    def __del__(self) -> None:
        glDeleteProgram(self.__RendererID)

    def Bind(self) -> None:
        glUseProgram(self.__RendererID)

    def Unbind(self) -> None:
        glUseProgram(0)

    def _GetUniformLocation(self, name: str) -> int:
        location = self.__UniformLocations.get(name, False)
        if not location:
            location = glGetUniformLocation(self.__RendererID, name)
            self.__UniformLocations[name] = location
        return location

    def SetMat4(self, name: str, matrix: pyrr.Matrix44) -> None:
        location = self._GetUniformLocation(name)
        glUniformMatrix4fv(location, 1, GL_FALSE, matrix)

    def SetFloat3(self, name: str, vector: pyrr.Vector3) -> None:
        location = self._GetUniformLocation(name)
        glUniform3f(location, vector.x, vector.y, vector.z)

    def SetFloat4(self, name: str, vector: pyrr.Vector4) -> None:
        location = self._GetUniformLocation(name)
        glUniform4f(location, vector.x, vector.y, vector.z, vector.w)

    def SetFloat2(self, name: str, x: float, y: float) -> None:
        location = self._GetUniformLocation(name)
        glUniform2f(location, x, y)

    def SetFloat(self, name: str, value: float) -> None:
        location = self._GetUniformLocation(name)
        glUniform1f(location, value)

    def SetInt(self, name: str, value: int) -> None:
        location = self._GetUniformLocation(name)
        glUniform1i(location, value)

    def SetBool(self, name: str, value: bool) -> None:
        self.SetInt(name, int(value))
