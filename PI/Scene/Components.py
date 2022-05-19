from pathlib import Path
from ..Logging.logger import PI_CORE_ASSERT
from ..Renderer.Mesh  import Mesh
from ..Renderer.Light import *
import pyrr
from .SceneCamera import SceneCamera

from multipledispatch import dispatch
from dataclasses import dataclass

from typing import TypeVar as _TypeVar

# They are applied to all Entities
class TagComponent:
    Tag: str

    def __init__(self, tag: str="Entity") -> None: self.Tag = tag
    def __str__(self) -> str: return self.Tag
class TransformComponent:
    Translation : pyrr.Vector3 = pyrr.Vector3([ 0.0, 0.0, 0.0 ])
    Rotation    : pyrr.Vector3 = pyrr.Vector3([ 0.0, 0.0, 0.0 ])
    Scale       : pyrr.Vector3 = pyrr.Vector3([ 1.0, 1.0, 1.0 ])

    def __init__(self, translation: pyrr.Vector3=pyrr.Vector3([ 0.0, 0.0, 0.0 ])) -> None: self.Translation = translation

    @property
    def Transform(self) -> pyrr.matrix44:
        rotation: pyrr.Matrix44

        rotX = pyrr.matrix44.create_from_x_rotation(self.Rotation.x)
        rotY = pyrr.matrix44.create_from_y_rotation(self.Rotation.y)
        rotZ = pyrr.matrix44.create_from_z_rotation(self.Rotation.z)

        rotation = rotX @ rotY @ rotZ

        location = pyrr.matrix44.create_from_translation(self.Translation)
        scale = pyrr.matrix44.create_from_scale(self.Scale)

        return scale @ rotation @ location

    def __pyrr_Matrix44__(self) -> pyrr.Matrix44: return self.Transform

    def SetTranslation(self, pos: pyrr.Vector3) -> None:
        self.Translation = pos

    def Translate(self, delta: pyrr.Vector3) -> None:
        self.Translation = self.Translation + delta

    def SetRotation(self, rotation: pyrr.Vector3) -> None:
        self.Rotation = rotation
    
    def Rotate(self, delta: pyrr.Vector3) -> None:
        self.Rotation = self.Rotation + delta

    def SetScale(self, scale: pyrr.Vector3) -> None:
        self.Scale = scale

# They are only appiled to selective Entities
class CameraComponent:
    Camera: SceneCamera

    Primary          : bool
    FixedAspectRatio : bool

    def __init__(self, camera: SceneCamera, isPrimary: bool=True, isFixedAspectratio: bool=False) -> None:
        self.Camera = camera
        self.Primary = isPrimary
        self.FixedAspectRatio = isFixedAspectratio

    def __bool__(self) -> bool: return self.Primary
class MeshComponent:
    MeshObject : Mesh
    Name       : str
    Path       : str

    @dispatch(Mesh)
    def __init__(self, mesh: Mesh) -> None:
        self.MeshObject = mesh
        self.Name       = mesh.Name
        self.Path       = mesh.Path

    @dispatch(str)
    def __init__(self, path: str) -> None:
        self.MeshObject : Mesh = Mesh.Load(path)[0]
        self.Name       : str  = self.MeshObject.Name
        self.Path       : str  = path

    def __str__(self) -> str: return self.Name
class LightComponent:
    @dataclass(frozen=True)
    class TypeEnum:
        Directional : int = 0
        Point       : int = 1
        Spot        : int = 2

    LightType: int
    Light: Light

    def __init__(self, _type: int, *args, **kwargs) -> None:
        if   _type == LightComponent.TypeEnum.Directional : self.Light = DirectionalLight(*args, **kwargs)
        elif _type == LightComponent.TypeEnum.Point       : self.Light = PointLight(*args, **kwargs, index=0)
        elif _type == LightComponent.TypeEnum.Spot        : self.Light = SpotLight(*args, **kwargs, index=0)
        else: PI_CORE_ASSERT(False, "Wrong light type!")

        self.LightType = _type

CTV = _TypeVar("CTV",
        TagComponent, TransformComponent, CameraComponent, MeshComponent, LightComponent
    )
