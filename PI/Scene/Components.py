from ..Logging.logger import PI_CORE_ASSERT
from ..Renderer.Mesh  import Mesh
from ..Renderer.Light import *
from .SceneCamera import SceneCamera
from ..Scripting  import ImportClass

import pyrr
from modulefinder import Module
from multipledispatch import dispatch
from dataclasses import dataclass

from typing import Callable, TypeVar, Dict, Any

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

    Initialized: bool = False

    @dispatch(Mesh)
    def __init__(self, mesh: Mesh) -> None:
        self.MeshObject = mesh
        self.Name       = mesh.Name
        self.Path       = mesh.Path
        self.Initialized= True

    @dispatch(str)
    def __init__(self, path: str) -> None:
        self.Path: str  = path

    def Init(self) -> None:
        if self.Path != "" and not self.Initialized:
            self.MeshObject: Mesh = Mesh.Load(self.Path)[0]
            self.Name = self.MeshObject.Name

            self.Initialized = True

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
class ScriptComponent:
    Bound  : bool = False

    Entity = None
    Script : Module

    Path   : str
    _Path  : str
    Name   : str

    @property
    def Variables(self) -> Dict[str, Any]:
        return { name: instance for name, instance in self.Script.__dict__.items() if not name.startswith("_") }

    OnAttach: Callable[[], None]
    OnDetach: Callable[[], None]
    OnUpdate: Callable[[float], None]

    def __init__(self, pathToScript: str, entity) -> None:
        self.Entity = entity
        self.Path  = pathToScript
        self._Path = pathToScript

    def ImportModule(self) -> None:
        self.Name = "Script not set"
        if self.Path == ".": return
        
        self.Name, self.Script = ImportClass(self.Path, False)
        self.Bind()

    def Bind(self) -> None:
        if self.Bound: return

        self.Script = self.Script(self.Entity)
        self.OnAttach: Callable[[], None] = self.Script.OnAttach
        self.OnDetach: Callable[[], None] = self.Script.OnDetach
        self.OnUpdate: Callable[[float], None] = self.Script.OnUpdate

        self.OnAttach()

        self.Bound = True

CTV = TypeVar("CTV",
        TagComponent, TransformComponent, CameraComponent, MeshComponent, LightComponent, ScriptComponent
    )
