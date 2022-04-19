from .Light import *

class DirectionalLight(Light):
    __Direction: pyrr.Vector3

    def __init__(self,
        direction: pyrr.Vector3,
        diffuse  : pyrr.Vector3=pyrr.Vector3([ 1.0, 1.0, 1.0 ]),
        specular : pyrr.Vector3=pyrr.Vector3([ 1.0, 1.0, 1.0 ]),
        intensity: float=1.0
        ) -> None:
        super().__init__(pyrr.Vector3([ 0.0, 0.0, 0.0 ]), diffuse, specular, intensity)
        self.__Direction = direction

    @property
    def Direction(self) -> pyrr.Vector3:
        return self.__Direction

    def SetDirection(self, new: pyrr.Vector3):
        self.__Direction = new
        return self

    def UploadPropertiesToShader(self, shader: Shader) -> None:
        super().UploadPropertiesToShader("u_DirectionalLight", shader)
        shader.SetFloat3("u_DirectionalLight.Direction", self.__Direction)
