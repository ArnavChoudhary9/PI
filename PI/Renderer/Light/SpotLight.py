from .PointLight import *

from math import cos, radians

# Technically a spot light is also a point light
class SpotLight(PointLight):
    __Index : int

    __Direction : pyrr.Vector3
    __CutOff    : float
    __OuterCutOff: float

    def __init__(self,
        index    : int,
        position : pyrr.Vector3=pyrr.Vector3([ 0.0, 0.0, 0.0 ]),
        direction: pyrr.Vector3=pyrr.Vector3([ 0.0, -1.0, 0.0 ]),
        cutOff   : float=20,
        outerCutOff: float=25,
        diffuse  : pyrr.Vector3=pyrr.Vector3([ 0.8, 0.8, 0.8 ]),
        specular : pyrr.Vector3=pyrr.Vector3([ 0.5, 0.5, 0.5 ]),
        intensity: float=1.0
        ) -> None:

        # NOTE: Accesses Light class
        super(PointLight, self).__init__(position, diffuse, specular, intensity)
        self.SetIntensity(intensity)
        
        self.__Index = index

        self.__Direction = direction
        self.__CutOff    = cutOff
        self.__OuterCutOff = outerCutOff

    @property
    def Direction(self) -> pyrr.Vector3:
        return self.__Direction

    def SetDirection(self, new: pyrr.Vector3):
        self.__Direction = new
        return self

    @property
    def CutOff(self) -> float:
        return self.__CutOff

    def SetCutOff(self, new: float):
        self.__CutOff = new
        return self

    @property
    def OuterCutOff(self) -> float:
        return self.__OuterCutOff

    def SetOuterCutOff(self, new: float):
        self.__OuterCutOff = new
        return self

    def SetIndex(self, index: int) -> None:
        self.__Index = index

    def UploadPropertiesToShader(self, shader: Shader) -> None:
        # NOTE: Accesses Light class
        super(PointLight, self).UploadPropertiesToShader(f"u_SpotLights[{self.__Index}]", shader)
        
        shader.SetFloat3(f"u_SpotLights[{self.__Index}].Direction", self.__Direction)
        shader.SetFloat(f"u_SpotLights[{self.__Index}].CutOff", cos(radians(self.__CutOff)))
        shader.SetFloat(f"u_SpotLights[{self.__Index}].OuterCutOff", cos(radians(self.__OuterCutOff)))

        # We still have to set them manually
        shader.SetFloat(f"u_SpotLights[{self.__Index}].ConstantFactor", self._ConstantFactor)
        shader.SetFloat(f"u_SpotLights[{self.__Index}].LinearFactor", self._LinearFactor)
        shader.SetFloat(f"u_SpotLights[{self.__Index}].QuadraticFactor", self._QuadraticFactor)
