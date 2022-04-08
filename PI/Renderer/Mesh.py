from ..logger import PI_CORE_TRACE
from .VertexArray import *
from .Buffer import *
from .Material import *

import pyrr
from math import radians
from random import randrange
from typing import Dict, List

class Mesh:
    __slots__ = "__VertexArray", "__VertexBuffer", "__IndexBuffer", "__Material", \
        "__Translation", "__Rotation", "__Scale", \
        "__Translation_Matrix", "__Rotation_Matrix", "__Scale_Matrix", "__Transform", \
        "__Name"

    def __init__(self, vertices: list, indicies: list, layout: BufferLayout,
        name: str="Mesh_{}".format(randrange(0, 10000)),
        translation : pyrr.Vector3=pyrr.Vector3([ 0, 0, 0 ]),
        rotation    : pyrr.Vector3=pyrr.Vector3([ 0, 0, 0 ]),
        scale       : pyrr.Vector3=pyrr.Vector3([ 1, 1, 1 ]),
        material    : Material = None
        ) -> None:

        self.__Name = name

        self.__Translation = translation
        self.__Rotation    = rotation
        self.__Scale       = scale

        self._RecalculateTransform()

        self.__VertexArray  : VertexArray  = VertexArray.Create()
        self.__VertexBuffer : VertexBuffer = VertexBuffer.Create(vertices)
        self.__IndexBuffer  : IndexBuffer  = IndexBuffer.Create(indicies)

        self.__VertexBuffer.SetLayout(layout)
        self.__VertexArray.AddVertexBuffer(self.__VertexBuffer)
        self.__VertexArray.SetIndexBuffer(self.__IndexBuffer)

        if material is None:
            self.__Material: Material = Material(
                Material.Type.StandardUnlit,
                albedo=pyrr.Vector4([ 0.8, 0.8, 0.8, 1.0 ])
            )

        else: self.__Material = material
        self.__VertexArray.Unbind()

    @staticmethod
    def Load(path: str) -> list:
        UnParsedStr: str
        with open(path) as _file:
            UnParsedStr = _file.read()
        UnParsedStr: List[str] = UnParsedStr.splitlines()

        lastSlash = path.rfind("\\")
        offset = 1
        if lastSlash == -1:
            lastSlash = path.rfind("/")
            offset = 2

        DefaultMaterial = Material(
            Material.Type.StandardUnlit,
            pyrr.Vector4([ 0.8, 0.8, 0.8, 1.0 ]),
            "DefaultMaterial"
        )

        Objects   : Dict[str, List[list, list, list, list, Material]] = {}
        Materials : Dict[str, Material] = {}

        currentobject : str

        for _str in UnParsedStr:
            _str : List[str] = _str.split(" ")

            if _str[0] == "#" or _str == [""]: continue
            elif _str[0] == "mtllib":
                mats = Material.Load("{}{}".format(path[:lastSlash+offset], _str[1]))
                for mat in mats:
                    Materials[mat.Name] = mat

            elif _str[0] == "o":
                currentobject = _str[1]
                Objects[currentobject] = [[], [], [], [], None]

            elif _str[0] == "v":
                Objects[currentobject][0].extend(( float(_str[1]), float(_str[2]), float(_str[3]) ))

            elif _str[0] == "vt":
                Objects[currentobject][1].extend(( float(_str[1]), float(_str[2]) ))

            elif _str[0] == "vn":
                Objects[currentobject][2].extend(( float(_str[1]), float(_str[2]), float(_str[3]) ))

            elif _str[0] == "usemtl":
                if _str[1] == "None":
                    Objects[currentobject][4] = DefaultMaterial
                    continue

                Objects[currentobject][4] = Materials[_str[1]]

            elif _str[0] == "f":
                faces = (
                    int( _str[1].split("/")[0] ) - 1,
                    int( _str[2].split("/")[0] ) - 1,
                    int( _str[3].split("/")[0] ) - 1
                )
                Objects[currentobject][3].extend(faces)

            elif _str[0] == "s": continue
            else:  continue

        meshes: List[Mesh] = []
        
        for name, obj in Objects.items():
            vertices = []
            for index in range(0, len(obj[0]), 3):
                vertices.extend((
                    obj[0][index+0], obj[0][index+1], obj[0][index+2],
                    0.0, 0.0,
                    0.0, 0.0, 0.0
                ))

            meshes.append(Mesh(
                vertices = vertices,
                indicies = obj[3],
                layout = BufferLayout(
                    ( ShaderDataType.Float3, "a_Position" ),
                    ( ShaderDataType.Float2, "a_TexCoord" ),
                    ( ShaderDataType.Float3, "a_Normal" ),
                ),
                material = obj[4],
                name = name
            ))

        return meshes

    @property
    def Name(self) -> str:
        return self.__Name

    @property
    def Transform(self) -> pyrr.Matrix44:
        return self.__Transform

    @property
    def Translation(self) -> pyrr.Vector3:
        return self.__Translation

    @property
    def Rotation(self) -> pyrr.Vector3:
        return self.__Rotation

    @property
    def Scale(self) -> pyrr.Vector3:
        return self.__Scale

    @property
    def Material(self) -> Material:
        return self.__Material

    @property
    def TranslationMatrix(self) -> pyrr.Vector3:
        return self.__Translation_Matrix

    @property
    def RotationMatrix(self) -> pyrr.Vector3:
        return self.__Rotation_Matrix

    @property
    def ScaleMatrix(self) -> pyrr.Vector3:
        return self.__Scale_Matrix

    @property
    def VertexArray(self) -> VertexArray:
        return self.__VertexArray

    def _RecalculateTransform(self) -> None:
        self.__Translation_Matrix = pyrr.matrix44.create_from_translation(self.__Translation)
        self.__Scale_Matrix       = pyrr.matrix44.create_from_scale(self.__Scale)

        self.__Rotation[0] %= 360
        self.__Rotation[1] %= 360
        self.__Rotation[2] %= 360

        rotX = pyrr.matrix44.create_from_x_rotation( radians(self.__Rotation.x) )
        rotY = pyrr.matrix44.create_from_y_rotation( radians(self.__Rotation.y) )
        rotZ = pyrr.matrix44.create_from_z_rotation( radians(self.__Rotation.z) )

        self.__Rotation_Matrix    = rotX @ rotY @ rotZ

        self.__Transform = self.__Scale_Matrix @ self.__Rotation_Matrix @ self.__Translation_Matrix

    def SetTranslation(self, translation: pyrr.Vector3) -> None:
        self.__Translation = translation
        
    def SetRotation(self, rotation: pyrr.Vector3) -> None:
        self.__Rotation = rotation
        
    def SetScale(self, scale: pyrr.Vector3) -> None:
        self.__Scale = scale

    def Translate(self, delta: pyrr.Vector3) -> None:
        self.__Translation = self.__Translation + delta

    def Rotate(self, delta: pyrr.Vector3) -> None:
        self.__Rotation = self.__Rotation + delta

    def Bind(self) -> None:
        self._RecalculateTransform()

        self.__Material.Bind()
        self.__Material.SetFields(self)
        self.__VertexArray.Bind()
