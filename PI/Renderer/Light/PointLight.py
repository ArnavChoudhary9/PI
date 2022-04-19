from .Light import *

class PointLight(Light):
    _ConstantFactor  : float
    _LinearFactor    : float
    _QuadraticFactor : float

    __Index : int

    def __init__(self,
        index: int,
        position : pyrr.Vector3=pyrr.Vector3([ 0.8, 0.8, 0.8 ]),
        diffuse  : pyrr.Vector3=pyrr.Vector3([ 0.8, 0.8, 0.8 ]),
        specular : pyrr.Vector3=pyrr.Vector3([ 0.8, 0.8, 0.8 ]),
        intensity: float = 1
        ) -> None:
        super().__init__(position, diffuse, specular, intensity)
        self.SetIntensity(intensity)
        self.__Index = index

    @property
    def Index(self) -> int:
        return self.__Index

    def SetIntensity(self, new: float):
        self._Intensity = new

        # Calculate attenuation factors
        self._ConstantFactor  = 1.0
        self._LinearFactor    = 0.1   / new
        self._QuadraticFactor = 0.02  / new

        return self

    def UploadPropertiesToShader(self, shader: Shader) -> None:
        super().UploadPropertiesToShader(f"u_PointLights[{self.__Index}]", shader)

        shader.SetFloat(f"u_PointLights[{self.__Index}].ConstantFactor", self._ConstantFactor)
        shader.SetFloat(f"u_PointLights[{self.__Index}].LinearFactor", self._LinearFactor)
        shader.SetFloat(f"u_PointLights[{self.__Index}].QuadraticFactor", self._QuadraticFactor)
