from .Texture import Texture2D
from .VertexArray import *
from .Buffer import *
from .Material import *
from .Light import DirectionalLight, PointLight, SpotLight

import pyrr
from multipledispatch import dispatch
from math import radians
from typing import List

class Mesh:
    __slots__ = "__VertexArray", "__VertexBuffer", "__IndexBuffer", \
        "__Translation", "__Rotation", "__Scale", \
        "__Translation_Matrix", "__Rotation_Matrix", "__Scale_Matrix", "__Transform", "__Transformed", \
        "__Name", "__Path", "__Material"

    @dispatch(list, list, BufferLayout)
    def __init__(self, vertices: list, indicies: list, layout: BufferLayout,
        name: str=Random.GenerateName("Mesh"),
        translation : pyrr.Vector3=pyrr.Vector3([ 0, 0, 0 ]),
        rotation    : pyrr.Vector3=pyrr.Vector3([ 0, 0, 0 ]),
        scale       : pyrr.Vector3=pyrr.Vector3([ 1, 1, 1 ])
        ) -> None:

        self.__Name = name
        self.__Path = "Internally Created Mesh"
        self.__Material = Material(Material.Type.StandardPhong)

        self.__Translation = translation
        self.__Rotation    = rotation
        self.__Scale       = scale

        self.__Transformed: bool = False

        self._RecalculateTransform()

        self.__VertexArray  : VertexArray  = VertexArray.Create()
        self.__VertexBuffer : VertexBuffer = VertexBuffer.Create(vertices)
        self.__IndexBuffer  : IndexBuffer  = IndexBuffer.Create(indicies)

        self.__VertexBuffer.SetLayout(layout)

        self.__VertexArray.AddVertexBuffer(self.__VertexBuffer)
        self.__VertexArray.SetIndexBuffer(self.__IndexBuffer)
        self.__VertexArray.Unbind()

    @dispatch(VertexArray, VertexBuffer, IndexBuffer)
    def __init__(self, vertexArray: VertexArray, vertexBuffer: VertexBuffer, indexBuffer: IndexBuffer,
        name: str=Random.GenerateName("Mesh"),
        translation : pyrr.Vector3=pyrr.Vector3([ 0, 0, 0 ]),
        rotation    : pyrr.Vector3=pyrr.Vector3([ 0, 0, 0 ]),
        scale       : pyrr.Vector3=pyrr.Vector3([ 1, 1, 1 ])
        ) -> None:

        self.__Name = name
        self.__Path = "Internally Created Mesh"
        self.__Material = Material(Material.Type.StandardPhong)

        self.__Translation = translation
        self.__Rotation    = rotation
        self.__Scale       = scale

        self.__Transformed: bool = False

        self._RecalculateTransform()

        self.__VertexArray  : VertexArray  = vertexArray
        self.__VertexBuffer : VertexBuffer = vertexBuffer
        self.__IndexBuffer  : IndexBuffer  = indexBuffer
        
        self.__VertexArray.Unbind()

    @staticmethod
    def Load(path: str):
        from ..Core import OBJReader
        objs = OBJReader.Read(path)
        materials = objs.materials
        meshes = objs.meshes

        objects = []

        for (nameMat, material), (nameMesh, mesh) in zip(materials.items(), meshes.items()):
            mat: Material = None

            if material.texture is not None:
                if material.texture_specular_color is not None:
                    mat = Material(
                        Material.Type.Standard | Material.Type.Lit | Material.Type.Phong | Material.Type.Textured,
                        textureAlbedo=Texture2D.Create(material.texture.path),
                        textureSpecular=Texture2D.Create(material.texture_specular_color.path),
                        tilingFactor=material.texture.options.s[0],
                        name=nameMat
                    )
                
                else:
                    mat = Material(
                        Material.Type.Standard | Material.Type.Lit | Material.Type.Phong | Material.Type.Textured,
                        textureAlbedo=Texture2D.Create(material.texture.path),
                        tilingFactor=material.texture.options.s[0],
                        name=nameMat
                    )

            else:
                mat = Material(
                    Material.Type.Standard | Material.Type.Lit | Material.Type.Phong,
                    diffuse=pyrr.Vector4([ *material.diffuse ]),
                    specular=pyrr.Vector4([ *material.specular ]),
                    name=nameMat
                )

            mesh = Mesh(
                material.vertices, list(range(0, int(len(material.vertices)/8))),
                BufferLayout(
                    ( ShaderDataType.Float2, "a_TexCoord" ),
                    ( ShaderDataType.Float3, "a_Normal"   ),
                    ( ShaderDataType.Float3, "a_Position" )
                ),
                name=nameMesh
            )
            mesh.__Path = path
            mesh.SetMaterial(mat)

            objects.append(mesh)

        return objects

    @property
    def Name(self) -> str: return self.__Name
    @property
    def Path(self) -> str: return self.__Path
    @property
    def Material(self) -> Material: return self.__Material
    @property
    def Transform(self) -> pyrr.Matrix44: return self.__Transform
    @property
    def Translation(self) -> pyrr.Vector3: return self.__Translation
    @property
    def Rotation(self) -> pyrr.Vector3: return self.__Rotation
    @property
    def Scale(self) -> pyrr.Vector3: return self.__Scale
    @property
    def TranslationMatrix(self) -> pyrr.Vector3: return self.__Translation_Matrix
    @property
    def RotationMatrix(self) -> pyrr.Vector3: return self.__Rotation_Matrix
    @property
    def ScaleMatrix(self) -> pyrr.Vector3: return self.__Scale_Matrix
    @property
    def VertexArray(self) -> VertexArray: return self.__VertexArray
    @property
    def VertexBuffer(self) -> VertexBuffer: return self.__VertexBuffer
    @property
    def IndexBuffer(self) -> IndexBuffer: return self.__IndexBuffer

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

    def SetMaterial(self, material: Material) -> None: self.__Material = material

    def SetTranslation(self, translation: pyrr.Vector3):
        self.__Translation = translation
        self.__Transformed = True

        return self
        
    def SetRotation(self, rotation: pyrr.Vector3):
        self.__Rotation = rotation
        self.__Transformed = True

        return self
        
    def SetScale(self, scale: pyrr.Vector3):
        self.__Scale = scale
        self.__Transformed = True

        return self

    def Translate(self, delta: pyrr.Vector3):
        self.__Translation = self.__Translation + delta
        self.__Transformed = True

        return self

    def Rotate(self, delta: pyrr.Vector3):
        self.__Rotation = self.__Rotation + delta
        self.__Transformed = True

        return self

    def Bind(self,
        directionalLight: DirectionalLight,
        pointLights: List[PointLight], pointLightLen: int,
        spotLights : List[SpotLight] , spotLightLen : int,
        cameraPos: pyrr.Vector3
        ) -> None:

        if self.__Transformed:
            self._RecalculateTransform()
            self.__Transformed = False

        self.__Material.Bind()
        self.__Material.SetFields(self, cameraPos)

        # Light stuff
        if Material.Type.Is(self.__Material.MatType, Material.Type.Lit):
            directionalLight.UploadPropertiesToShader(self.__Material.Shader)
        
            for light in pointLights:
                light.UploadPropertiesToShader(self.__Material.Shader)

            self.__Material.Shader.SetInt("u_NumPointLights", pointLightLen)
        
            for light in spotLights:
                light.UploadPropertiesToShader(self.__Material.Shader)

            self.__Material.Shader.SetInt("u_NumSpotLights", spotLightLen)

        self.__VertexArray.Bind()
