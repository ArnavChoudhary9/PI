from ...Renderer import Shader

from OpenGL.GL import glDeleteProgram, glUseProgram,\
    glGetUniformLocation, glUniformMatrix4fv, glUniform4f, glUniform3f, glUniform2f, glUniform1f, glUniform1i
from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, GL_FALSE

from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr

class OpenGLShader(Shader):
    __RendererID: int

    def __init__(self, shaderFile: str) -> None:
        src = ""

        with open(shaderFile, 'r') as file:
            src = file.read()

        src = src.split('\n')

        vertexSrc   : list = []
        fragmentSrc : list = []

        index = 0
        while (len(src) > index):
            shaderType = src[index].split(" ")[1].lower()

            if shaderType == "vertex" or shaderType == "vert" or shaderType == "geometry":
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

    @property
    def RendererID(self) -> int:
        return self.__RendererID

    def __del__(self) -> None:
        glDeleteProgram(self.__RendererID)

    def Bind(self) -> None:
        glUseProgram(self.__RendererID)

    def Unbind(self) -> None:
        glUseProgram(0)

    def UploadUniformMat4(self, name: str, matrix: pyrr.Matrix44) -> None:
        location = glGetUniformLocation(self.__RendererID, name)
        glUniformMatrix4fv(location, 1, GL_FALSE, matrix)

    def UploadUniformFloat3(self, name: str, vector: pyrr.Vector3) -> None:
        location = glGetUniformLocation(self.__RendererID, name)
        glUniform3f(location, vector.x, vector.y, vector.z)

    def UploadUniformFloat4(self, name: str, vector: pyrr.Vector4) -> None:
        location = glGetUniformLocation(self.__RendererID, name)
        glUniform4f(location, vector.x, vector.y, vector.z, vector.w)

    def UploadUniformFloat2(self, name: str, x: float, y: float) -> None:
        location = glGetUniformLocation(self.__RendererID, name)
        glUniform2f(location, x, y)

    def UploadUniformFloat(self, name: str, value: float) -> None:
        location = glGetUniformLocation(self.__RendererID, name)
        glUniform1f(location, value)

    def UploadUniformInt(self, name: str, value: int) -> None:
        location = glGetUniformLocation(self.__RendererID, name)
        glUniform1i(location, value)
