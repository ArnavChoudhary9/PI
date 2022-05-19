from PI.Logging.logger import PI_CORE_ASSERT, PI_CORE_WARN
from ...Renderer import Shader

from OpenGL.GL import glDeleteProgram, glUseProgram,\
    glGetUniformLocation, \
    glUniformMatrix4fv, glUniform4f, glUniform3f, glUniform2f, glUniform1f, glUniform1i
from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, GL_GEOMETRY_SHADER, GL_FALSE

from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr

class OpenGLShader(Shader):
    __slots__ = "__RendererID", "__Name", "__UniformLocations"

    def __init__(self, shaderFile: str) -> None:
        src = ""
        with open(shaderFile, 'r') as file: src = file.read()
        src = src.split('\n')

        slashIndex = shaderFile.rfind("\\")
        if slashIndex == -1: slashIndex = shaderFile.rfind("/")

        dotIndex = shaderFile.rfind(".")

        if   dotIndex != -1: self.__Name = shaderFile [ slashIndex+1:dotIndex ]  # Has file extension
        else               : self.__Name = shaderFile [ slashIndex+1:         ]  # Does not have file extension

        currentShaderType = -1
        currentCode = []
        codes = []
        version = 450
        shaderVersionType: str = "core"
        for nextLine in src:
            nextLineList = nextLine.split(" ")

            if nextLineList[0] == "#type":
                if currentShaderType == -1: currentShaderType = OpenGLShader.StrToGLShaderType(nextLineList[1])
                else:
                    code = "\n".join(currentCode)
                    currentCode = []
                    codes.append(compileShader(code, currentShaderType))

                    currentShaderType = OpenGLShader.StrToGLShaderType(nextLineList[1])

            elif nextLineList[0] == "#version":
                version = min(int(nextLineList[1]), version)   
                shaderVersionType = nextLineList[2]                 
                currentCode.append(nextLine)

            else: currentCode.append(nextLine)
        
        if len(currentCode) != 0:
            code = "\n".join(currentCode)
            currentCode = []
            codes.append(compileShader(code, currentShaderType))
            currentShaderType = -1

        if version < 450:
            PI_CORE_ASSERT(version >= 330, "GLSL version too old.")

            PI_CORE_WARN("Older version of GLSL ({1} {2}) used in Shader: {0}", shaderFile, version, shaderVersionType)
            PI_CORE_WARN("Use GLSL version 450 core or higher")

        self.__RendererID = compileProgram(*codes)
        self.__UniformLocations: dict = {}

    @staticmethod
    def StrToGLShaderType(_str: str) -> int:
        _str = _str.lower()

        vertNames = [ "vertex"   , "vert" ]
        geomNames = [ "geometry" , "tess" ]
        fragNames = [ "fragment" , "frag" , "pixel" ]

        if   _str in vertNames: return GL_VERTEX_SHADER
        elif _str in geomNames: return GL_GEOMETRY_SHADER
        elif _str in fragNames: return GL_FRAGMENT_SHADER
        else: PI_CORE_ASSERT(False, "Invalid shader type.")

    @property
    def RendererID(self) -> int: return self.__RendererID
    @property
    def Name(self) -> str: return self.__Name

    def __repr__(self) -> str: return self.__Name
    def __del__ (self) -> None: glDeleteProgram(self.__RendererID)
    def Bind    (self) -> None: glUseProgram(self.__RendererID)
    def Unbind  (self) -> None: glUseProgram(0)

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
