from .Shader import Shader

import pyrr

class Light:
    # __slots__ = 

    __Position: pyrr.Vector3

    __Ambient  : pyrr.Vector3
    __Diffuse  : pyrr.Vector3
    __Specular : pyrr.Vector3

    def __init__(self,
        position : pyrr.Vector3=pyrr.Vector3([ 0.0, 5.0, 10.0 ]),
        ambient  : pyrr.Vector3=pyrr.Vector3([ 0.15, 0.15, 0.15 ]),
        diffuse  : pyrr.Vector3=pyrr.Vector3([ 1.0, 1.0, 1.0 ]),
        specular : pyrr.Vector3=pyrr.Vector3([ 1.0, 1.0, 1.0 ]),
        ) -> None:

        self.__Position = position

        self.__Ambient  = ambient
        self.__Diffuse  = diffuse
        self.__Specular = specular

    @property
    def Position(self) -> pyrr.Vector3:
        return self.__Position

    @property
    def Ambient(self) -> pyrr.Vector3:
        return self.__Ambient

    @property
    def Diffuse(self) -> pyrr.Vector3:
        return self.__Diffuse

    @property
    def Specular(self) -> pyrr.Vector3:
        return self.__Specular

    def SetPosition(self, new: pyrr.Vector3) -> None:
        self.__Position = new

    def SetAmbient(self, new: pyrr.Vector3) -> None:
        self.__Ambient = new

    def SetDiffuse(self, new: pyrr.Vector3) -> None:
        self.__Diffuse = new

    def SetSpecular(self, new: pyrr.Vector3) -> None:
        self.__Specular = new

    def SetProperties(self, shader: Shader) -> None:
        shader.SetFloat3("u_Light.Position", self.__Position)

        shader.SetFloat3("u_Light.Ambient", self.__Ambient)
        shader.SetFloat3("u_Light.Diffuse", self.__Diffuse)
        shader.SetFloat3("u_Light.Specular", self.__Specular)
