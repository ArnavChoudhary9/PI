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
    def Load(path: str):
        from ..Core   import OBJReader
        objs = OBJReader.Read(path)
        materials = objs.materials
        meshes = objs.meshes

        objects = []

        for (nameMat, material), (nameMesh, mesh) in zip(materials.items(), meshes.items()):
            specular = (material.specular[0] + material.specular[1] + material.specular[2]) / 3
            mat = Material(
                Material.Type.StandardUnlit,
                diffuse=pyrr.Vector4([ *material.diffuse ]),
                specular=specular,
                name=nameMat
            )

            mesh = Mesh(
                vertices=material.vertices, indicies=list(range(0, int(len(material.vertices)/8))),
                layout=BufferLayout(
                    ( ShaderDataType.Float2, "a_TexCoord" ),
                    ( ShaderDataType.Float3, "a_Normal"   ),
                    ( ShaderDataType.Float3, "a_Position" )
                ),
                name=nameMesh, material=mat
            )

            objects.append(mesh)

        return objects

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

    def Bind(self, lightColor: pyrr.Vector3, lightPos: pyrr.Vector3, cameraPos: pyrr.Vector3) -> None:
        self._RecalculateTransform()

        self.__Material.Bind()
        self.__Material.SetFields(self, lightColor, lightPos, cameraPos)
        self.__VertexArray.Bind()
