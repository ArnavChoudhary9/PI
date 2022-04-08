from .Shader import Shader
from ..logger import PI_CORE_ASSERT

from typing import Dict, List
import pyrr
from random import randrange

class Material:
    class Type:
        StandardUnlit = 0

    # __slots__ = 

    __Shader : Shader
    __Albedo : pyrr.Vector4
    __Name   : str

    def __init__(self, _type: int, albedo: pyrr.Vector4=pyrr.Vector4([ 1.0, 1.0, 1.0, 1.0 ]),
        name: str="Material_{}".format(randrange(0, 10000))) -> None:
        if _type == Material.Type.StandardUnlit:
            self.__Shader : Shader = Shader.Create(".\\Assets\\Shaders\\Standard3DShader.glsl")
        
        else: PI_CORE_ASSERT(False, "Unsupported Shader type.")

        self.__Albedo = albedo
        self.__Name   = name

    @staticmethod
    def Load(path: str):
        UnParsedStr: str
        with open(path) as _file:
            UnParsedStr = _file.read()
        UnParsedStr: List[str] = UnParsedStr.splitlines()

        _type = Material.Type.StandardUnlit

        Materials: Dict[str, List[int, pyrr.Vector4]] = {}
        currentMaterial: str

        for _str in UnParsedStr:
            _str : List[str] = _str.split(" ")

            if _str[0] == "#" or _str == [""]:
                continue

            elif _str[0] == "newmtl":
                currentMaterial = _str[1]
                Materials[currentMaterial] = [_type, None]

            elif _str[0] == "Ns" or _str[0] == "Ka" or _str[0] == "Ks" or \
                 _str[0] == "Ke" or _str[0] == "Ni" or _str[0] == "d"  or \
                 _str[0] == "illum":
                
                continue

            elif _str[0] == "Kd":
                Materials[currentMaterial][1] = pyrr.Vector4([
                    float(_str[1]),
                    float(_str[2]),
                    float(_str[3]),
                    1.0
                ])

        materials: List[Material] = []
        for name, obj in Materials.items():
            materials.append(Material(
                _type  = obj[0],
                albedo = obj[1],
                name   = name
            ))

        return materials

    @property
    def Name(self) -> str:
        return self.__Name

    def Bind(self) -> None:
        self.__Shader.Bind()

    def SetViewProjection(self, matrix: pyrr.Matrix44) -> None:
        self.__Shader.Bind()
        self.__Shader.SetMat4("u_ViewProjection", matrix)

    def SetFields(self, mesh) -> None:
        self.__Shader.Bind()
        self.__Shader.SetMat4("u_Transform", mesh.Transform)
        self.__Shader.SetFloat4("u_Color", self.__Albedo)
