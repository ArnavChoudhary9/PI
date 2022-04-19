from ..Shader import Shader

import pyrr

class Light:
    # __slots__ = 

    _Position: pyrr.Vector3

    _Ambient  : pyrr.Vector3
    _Diffuse  : pyrr.Vector3
    _Specular : pyrr.Vector3

    _Intensity : float

    def __init__(self,
        position : pyrr.Vector3=pyrr.Vector3([ 0.0, 5.0, 10.0 ]),
        diffuse  : pyrr.Vector3=pyrr.Vector3([ 1.0, 1.0, 1.0 ]),
        specular : pyrr.Vector3=pyrr.Vector3([ 1.0, 1.0, 1.0 ]),
        intensity: float=1.0
        ) -> None:

        self._Position = position

        self._Ambient  = diffuse * 0.2
        self._Diffuse  = diffuse
        self._Specular = specular

        self._Intensity = intensity

    @property
    def Position(self) -> pyrr.Vector3:
        return self._Position

    @property
    def Ambient(self) -> pyrr.Vector3:
        return self._Ambient

    @property
    def Diffuse(self) -> pyrr.Vector3:
        return self._Diffuse

    @property
    def Specular(self) -> pyrr.Vector3:
        return self._Specular

    @property
    def Intensity(self) -> float:
        return self._Intensity

    def SetPosition(self, new: pyrr.Vector3):
        self._Position = new
        return self

    def SetAmbient(self, new: pyrr.Vector3):
        self._Ambient = new
        return self

    def SetDiffuse(self, new: pyrr.Vector3):
        self._Diffuse = new
        return self

    def SetSpecular(self, new: pyrr.Vector3):
        self._Specular = new
        return self

    def SetIntensity(self, new: float):
        self._Intensity = new
        return self

    def UploadPropertiesToShader(self, typeName: str, shader: Shader) -> None:
        '''
        NOTE: We expect the Shader to be bound.
        '''
        
        shader.SetFloat3(f"{typeName}.Position", self._Position)

        shader.SetFloat3(f"{typeName}.Ambient", self._Ambient)
        shader.SetFloat3(f"{typeName}.Diffuse", self._Diffuse)
        shader.SetFloat3(f"{typeName}.Specular", self._Specular)

        shader.SetFloat(f"{typeName}.Intensity", self._Intensity)
