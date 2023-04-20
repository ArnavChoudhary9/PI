from ..Logging.logger import PI_CORE_ASSERT
from ..Renderer.Mesh  import Mesh
from ..Renderer.Material import Material
from ..Renderer.Light    import *
from ..Scripting  import *
from ..Physics    import *
from ..AssetManager.AssetManager import AssetManager
from .SceneCamera import SceneCamera

import pyrr

from uuid import UUID
from uuid import uuid4 as UUIDGenerator

from multipledispatch import dispatch
from dataclasses import dataclass

from typing import Callable, TypeVar, Dict, Any

# They are applied to all Entities
class IDComponent:
    ID: UUID

    def __init__ (self, id: UUID): self.ID = id

    @property
    def HEX(self) -> str: return self.ID.hex

    def __int__  (self) -> int : return self.ID.int
    def __str__  (self) -> str : return str(self.ID)
    def __repr__ (self) -> str : return self.ID.__repr__()
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

    def Copy(self, recipientEntity):
        component = TransformComponent()

        component.Translation = self.Translation .copy()
        component.Rotation    = self.Rotation    .copy()
        component.Scale       = self.Scale       .copy()

        return component

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

    def Copy(self, recipientEntity):
        component = CameraComponent(SceneCamera(self.Camera.ProjectionType), self.Primary, self.FixedAspectRatio)
        component.Camera.CameraObject.SetAspectRatio(self.Camera.CameraObject.AspectRatio)
        return component
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
        self.Path: str  = AssetManager.GetInstance().GetAbsolutePath(path)

    def Init(self) -> None:
        if self.Path == ".": return
        if AssetManager.GetInstance().GetRelativePath(self.Path) != '.' and not self.Initialized:
            mesh = AssetManager.GetInstance().Load(AssetManager.AssetType.MeshAsset, self.Path)
            self.MeshObject: Mesh = AssetManager.GetInstance().Get(mesh)
            self.Name = self.MeshObject.Name

            self.Initialized = True

    def __str__(self) -> str: return self.Name

    def Copy(self, recipientEntity): return MeshComponent(self.Path)
class MaterialComponent:
    MaterialObject : Material
    Textured       : bool = False
    Name           : str
    Path           : str

    Initialized: bool = False

    @dispatch(Material)
    def __init__(self, material: Material) -> None:
        self.MaterialObject = material
        self.Name           = material.Name
        self.Path           = "."

        if self.MaterialObject.AlbedoMap is not None: self.Textured = True

        self.Initialized = True

    @dispatch(str)
    def __init__(self, path: str) -> None:
        self.Path: str = path

    def Init(self) -> None:
        if self.Path == ".": return
        if AssetManager.GetInstance().GetRelativePath(self.Path) != '.' and not self.Initialized:
            mesh: Mesh = AssetManager.GetInstance().Get(self.Path)
            self.MaterialObject: Material = mesh.Material
            self.Name = self.MaterialObject.Name

            if self.MaterialObject.AlbedoMap is not None: self.Textured = True

            self.Initialized = True

    def __str__(self) -> str: return self.Name

    def Copy(self, recipientEntity): return MaterialComponent(self.Path)
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

    def Copy(self, recipientEntity):
        light = self.Light
        
        if self.LightType == LightComponent.TypeEnum.Directional:
            return LightComponent(
                LightComponent.TypeEnum.Directional, light.Direction, light.Diffuse, light.Specular, light.Intensity
            )

        elif self.LightType == LightComponent.TypeEnum.Point:
            lightToReturn = LightComponent(
                LightComponent.TypeEnum.Point, diffuse=light.Diffuse, specular=light.Specular, intensity=light.Intensity
            )

            lightToReturn.Light.SetIndex(light.Index)
            return lightToReturn
class ScriptComponent:
    Bound  : bool = False

    Entity = None
    Script = None

    Name   : str
    Module : str

    OnAttach: Callable[[], None]
    OnDetach: Callable[[], None]
    OnUpdate: Callable[[float], None]

    def __init__(self, module: str, name: str, entity) -> None:
        self.Entity = entity
        self.Module = module
        self.Name   = name

    def Bind(self) -> None:
        if self.Bound: return
        if self.Name == "": return

        try: self.Script: Script = ScriptingEngine.Modules[self.Module].AllScripts[self.Name]
        except KeyError as _:
            self.Bound = False
            return

        self.Script.Bind(self.Entity)
        self.Script.BindFunctions("OnAttach", "OnDetach", "OnUpdate")

        self.OnAttach: Callable[[], None] = self.Script.OnAttach
        self.OnDetach: Callable[[], None] = self.Script.OnDetach
        self.OnUpdate: Callable[[float], None] = self.Script.OnUpdate

        self.Bound = True

    @property
    def Variables(self) -> Dict[str, Any]: return self.Script.ExternalVariables
    @property
    def Namespace(self) -> str: return f"{self.Module}.{self.Name}"
    def SetVariables(self, map: Dict[str, Any]) -> None: self.Script.SetVariables(map)

    def Reload(self) -> None:
        self.Bound = False
        self.Bind()

    def Copy(self, recipientEntity):
        component = ScriptComponent(self.Module, self.Name, recipientEntity)
        component.Bind()
        component.SetVariables(self.Variables)

        return component

class CollidorComponent:
    class Shapes:
        Box, Plane \
            = range(2)
        
    def __init__(self,
        _type: int, scale: pyrr.Vector3=pyrr.Vector3([ 1, 1, 1 ]),
        up: pyrr.Vector3=pyrr.Vector3([ 0, 1, 0 ]), dist: float = 0.0
    ) -> None:
        self.Type = _type
        self._InitData = (scale, up, dist)      # For Copying
        if   _type == CollidorComponent.Shapes.Box   : self.Collidor = BoxCollider(bounds=scale)
        elif _type == CollidorComponent.Shapes.Plane : self.Collidor = PlaneCollider(
            bounds=pyrr.Vector3([ dist, 0, 0 ]), up=up
        )
    def Copy(self, recipientEntity): return CollidorComponent(self.Type, *self._InitData)
class RigidBodyComponent:
    def __init__(self, mat: PySicsMaterial) -> None:
        self._Mat = mat         # For Copying
        self.RigidBody = RigidBody(mat)

    def Copy(self, recipientEntity): return RigidBodyComponent(self._Mat)

CTV = TypeVar("CTV",
        IDComponent, TagComponent, TransformComponent,
        CameraComponent, MeshComponent, MaterialComponent, LightComponent, ScriptComponent,
        CollidorComponent, RigidBodyComponent
    )
