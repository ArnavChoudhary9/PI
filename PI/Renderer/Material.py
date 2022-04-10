from .Shader import Shader
from .Light import Light
from ..logger import PI_CORE_ASSERT

import pyrr
from random import randrange

class Material:
    class Type:
        StandardUnlit    : int = 0
        StandardLitPhong : int = 1

    # __slots__ = 

    __Shader : Shader

    __Ambient  : pyrr.Vector4
    __Diffuse  : pyrr.Vector4
    __Specular : pyrr.Vector4
    __Shininess: float

    __Name   : str

    def __init__(self, _type: int, 
        ambient  : pyrr.Vector4=pyrr.Vector4([ 0.8, 0.8, 0.8, 1.0 ]),
        diffuse  : pyrr.Vector4=pyrr.Vector4([ 0.8, 0.8, 0.8, 1.0 ]),
        specular : pyrr.Vector4=pyrr.Vector4([ 0.5, 0.5, 0.5, 1.0 ]),
        shininess: float=32,
        name: str="Material_{}".format(randrange(0, 10000))) -> None:
        if _type == Material.Type.StandardUnlit:
            self.__Shader : Shader = Shader.Create(".\\Assets\\Shaders\\StandardLitPhong_3D.glsl")
            # self.__Shader : Shader = Shader.Create(".\\Assets\\Shaders\\StandardUnlit_3D.glsl")
        
        else: PI_CORE_ASSERT(False, "Unsupported Shader type.")

        self.__Ambient  = ambient
        self.__Diffuse  = diffuse
        self.__Specular = specular
        self.__Shininess= shininess

        self.__Name     = name

    @property
    def Name(self) -> str:
        return self.__Name

    def Bind(self) -> None:
        self.__Shader.Bind()

    def SetViewProjection(self, matrix: pyrr.Matrix44) -> None:
        self.__Shader.Bind()
        self.__Shader.SetMat4("u_ViewProjection", matrix)

    def SetFields(self, mesh, light: Light, cameraPos: pyrr.Vector3) -> None:
        self.__Shader.Bind()
        self.__Shader.SetMat4("u_Transform", mesh.Transform)

        self.__Shader.SetFloat3("u_Material.Ambient", pyrr.Vector3.from_vector4(self.__Ambient)[0])
        self.__Shader.SetFloat3("u_Material.Diffuse", pyrr.Vector3.from_vector4(self.__Diffuse)[0])
        self.__Shader.SetFloat3("u_Material.Specular", pyrr.Vector3.from_vector4(self.__Specular)[0])
        self.__Shader.SetFloat("u_Material.Shininess", self.__Shininess)

        light.SetProperties(self.__Shader)

        self.__Shader.SetFloat3("u_CameraPos", cameraPos)
