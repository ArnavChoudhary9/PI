from re import S
from .Shader import Shader
from .Texture import Texture2D
from ..Logging.logger import PI_CORE_ASSERT

import pyrr
from random import randrange
from typing import Final

# This just shifts 1 to i th BIT
def BIT(i: int) -> int:
    return int(1 << i)

class Material:
    class Type:
        Null : Final[int] = 0b00000000

        # Type
        #     Standard => 0b00000001
        #     Custom   => 0b00000010
        Standard : Final[int] = BIT(0)
        Custom   : Final[int] = BIT(1)

        # Lit or not
        #     Unlit => 0b00000000
        #     Lit   => 0b00000100
        Lit : Final[int] = BIT(2)

        # Shading type
        #     None  => 0b00000000
        #     Phong => 0b00001000
        #     PBR   => 0b00010000
        Phong : Final[int] = BIT(3)
        PBR   : Final[int] = BIT(4)

        # Textured or not
        #    Not Textured => 0b00000000
        #    Textured     => 0b00100000
        Textured : Final[int] = BIT(5)

        @staticmethod
        def Is(_type: int, flag: int) -> int:
            return _type & flag

        @staticmethod
        def AddFlag(_type: int, flag: int) -> int:
            _type |= flag
            return _type
        

    __slots__ = "__Shader", \
        "__TextureAlbedo", "__TextureSpecular", "__TilingFactor", \
        "__Diffuse", "__Specular", "__Shininess", \
        "__Name", "__Type"

    def __init__(self,
        _type: int,

        diffuse  : pyrr.Vector4=pyrr.Vector4([ 0.8, 0.8, 0.8, 1.0 ]),
        specular : pyrr.Vector4=pyrr.Vector4([ 0.5, 0.5, 0.5, 1.0 ]),
        
        textureAlbedo   : Texture2D=None,
        textureSpecular : Texture2D=None,

        tilingFactor : float = 1.0,

        shininess: float=32,
        name: str="Material_{}".format(randrange(0, 10000))
        ) -> None:

        if Material.Type.Is(_type, Material.Type.Lit):
            if Material.Type.Is(_type, Material.Type.Phong):
                if Material.Type.Is(_type, Material.Type.Textured):
                    self.__Shader : Shader = Shader.Create(".\\Assets\\Shaders\\StandardLitPhong_Textured_3D.glsl")
                elif not Material.Type.Is(_type, Material.Type.Textured):
                    self.__Shader : Shader = Shader.Create(".\\Assets\\Shaders\\StandardLitPhong_NonTextured_3D.glsl")
                else: PI_CORE_ASSERT(False, "Unsupported Shader type.")
            
            else: PI_CORE_ASSERT(False, "Unsupported Shader type.")

        elif not Material.Type.Is(_type, Material.Type.Lit):
            if Material.Type.Is(_type, Material.Type.Textured):
                self.__Shader : Shader = Shader.Create(".\\Assets\\Shaders\\StandardUnlit_Textured_3D.glsl")
            elif not Material.Type.Is(_type, Material.Type.Textured):
                self.__Shader : Shader = Shader.Create(".\\Assets\\Shaders\\StandardUnlit_NonTextured_3D.glsl")
            else: PI_CORE_ASSERT(False, "Unsupported Shader type.")

        else: PI_CORE_ASSERT(False, "Unsupported Shader type.")

        self.__TextureAlbedo   : Texture2D = textureAlbedo
        self.__TextureSpecular : Texture2D = textureSpecular

        self.__TilingFactor : float = tilingFactor

        self.__Diffuse  = diffuse
        self.__Specular = specular
        self.__Shininess= shininess

        self.__Name     = name
        self.__Type     = _type

    @property
    def Name(self) -> str:
        return self.__Name

    @property
    def MatType(self) -> int:
        return self.__Type

    @property
    def Shader(self) -> Shader:
        return self.__Shader

    def Bind(self) -> None:
        self.__Shader.Bind()

    def SetViewProjection(self, matrix: pyrr.Matrix44) -> None:
        self.__Shader.Bind()
        self.__Shader.SetMat4("u_ViewProjection", matrix)

    def SetFields(self, mesh, cameraPos: pyrr.Vector3) -> None:
        self.__Shader.Bind()
        self.__Shader.SetMat4("u_Transform", mesh.Transform)

        self.__Shader.SetFloat3("u_Material.Diffuse", pyrr.Vector3.from_vector4(self.__Diffuse)[0])

        if Material.Type.Is(self.__Type, Material.Type.Lit) \
            and Material.Type.Is(self.__Type, Material.Type.Phong):
            self.__Shader.SetFloat3("u_CameraPos", cameraPos)

        if Material.Type.Is(self.__Type, Material.Type.Phong):
            if self.__TextureSpecular is None:
                self.__Shader.SetFloat3("u_Material.Specular", pyrr.Vector3.from_vector4(self.__Specular)[0])
                self.__Shader.SetBool("u_Material.IsSpecularMap", False)

            self.__Shader.SetFloat("u_Material.Shininess", self.__Shininess)

            if self.__TextureSpecular is not None and Material.Type.Is(self.__Type, Material.Type.Textured):
                self.__TextureSpecular.Bind(1)
                self.__Shader.SetInt("u_Material.SpecularMap", 1)
                self.__Shader.SetBool("u_Material.IsSpecularMap", True)
            
        if Material.Type.Is(self.__Type, Material.Type.Textured):
            self.__Shader.SetFloat("u_Material.TilingFactor", self.__TilingFactor)
                
            self.__TextureAlbedo.Bind(0)
            self.__Shader.SetInt("u_Material.AlbedoMap", 0)
        
