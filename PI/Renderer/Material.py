from .Shader import Shader
from ..logger import PI_CORE_ASSERT

from typing import Dict, List
import pyrr
from random import randrange

class Material:
    class Type:
        StandardUnlit    : int = 0
        StandardLitPhong : int = 1

    # __slots__ = 

    __Shader : Shader
    __Albedo : pyrr.Vector4
    __Name   : str

    def __init__(self, _type: int, albedo: pyrr.Vector4=pyrr.Vector4([ 1.0, 1.0, 1.0, 1.0 ]),
        name: str="Material_{}".format(randrange(0, 10000))) -> None:
        if _type == Material.Type.StandardUnlit:
            self.__Shader : Shader = Shader.Create(".\\Assets\\Shaders\\StandardLitPhong_3D.glsl")
            # self.__Shader : Shader = Shader.Create(".\\Assets\\Shaders\\StandardUnlit_3D.glsl")
        
        else: PI_CORE_ASSERT(False, "Unsupported Shader type.")

        self.__Albedo = albedo
        self.__Name   = name

    @property
    def Name(self) -> str:
        return self.__Name

    def Bind(self) -> None:
        self.__Shader.Bind()

    def SetViewProjection(self, matrix: pyrr.Matrix44) -> None:
        self.__Shader.Bind()
        self.__Shader.SetMat4("u_ViewProjection", matrix)

    def SetFields(self, mesh, lightColor: pyrr.Vector3, lightPos: pyrr.Vector3, cameraPos: pyrr.Vector3) -> None:
        self.__Shader.Bind()
        self.__Shader.SetMat4("u_Transform", mesh.Transform)
        self.__Shader.SetFloat4("u_Color", self.__Albedo)
        self.__Shader.SetFloat3("u_LightColor", lightColor)
        self.__Shader.SetFloat3("u_LightPos", lightPos)
        self.__Shader.SetFloat3("u_CameraPos", cameraPos)
