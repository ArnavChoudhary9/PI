from .Entity     import Entity
from .Components import *

from ..Renderer import Renderer, DirectionalLight

import esper

from typing import Deque as _Deque

class Scene:
    _Registry: esper.World
    
    _ViewportWidth  : int = 1
    _ViewportHeight : int = 1

    _DirectionalLight: DirectionalLight = DirectionalLight(pyrr.Vector3([ 0, 0, 0 ]), intensity=0)

    _PointLights : _Deque[PointLight] = []
    _SpotLights  : _Deque[SpotLight]  = []

    def __init__(self) -> None: self._Registry = esper.World()

    def CreateEntity(self, name: str="Entity") -> Entity:
        entity = Entity(self._Registry.create_entity(), self)
        entity.AddComponent(TagComponent, name)
        entity.AddComponent(TransformComponent)
        return entity

    def DestroyEntity(self, entity: Entity) -> None:
        if entity.HasComponent(LightComponent):
            light = entity.GetComponent(LightComponent).Light

            if   isinstance(light, DirectionalLight): self._DirectionalLight.SetIntensity(0)
            elif isinstance(light, SpotLight): self._SpotLights.remove(light)
            elif isinstance(light, PointLight): self._PointLights.remove(light)

        self._Registry.delete_entity(int(entity))

    def OnUpdate(self, dt: float) -> None:
        self._Registry.process(dt)
        for entity, (meshComponent, transform) in self._Registry.get_components(MeshComponent, TransformComponent):
            mesh = meshComponent.MeshObject

            mesh.SetTranslation ( transform.Translation )
            mesh.SetRotation    ( transform.Rotation    )
            mesh.SetScale       ( transform.Scale       )
        
        for entity, (lightComponent, transform) in self._Registry.get_components(LightComponent, TransformComponent):
            light = lightComponent.Light
            light.SetPosition ( transform.Translation )

    def Draw(self) -> None:
        meshes = []
        for entity, meshComponent in self._Registry.get_component(MeshComponent):
            mesh = meshComponent.MeshObject
            meshes.append(mesh)

        Renderer.SubmitMeshes(meshes, self._DirectionalLight, self._PointLights, self._SpotLights)

    def OnViewportResize(self, width: int, height: int) -> None:
        self._ViewportWidth, self._ViewportHeight = width, height

        for entity, component in self._Registry.get_component(CameraComponent):
            if not component.FixedAspectRatio: component.Camera.CameraObject.SetAspectRatio(width / height)

    @property
    def PrimaryCameraEntity(self) -> Entity:
        for entity, component in self._Registry.get_component(CameraComponent):
            if component.Primary: return Entity(entity, self)

        return None

    def _OnComponentAdded(self, entity: Entity, component: CTV) -> None:
        if isinstance(component, CameraComponent):
            component.Camera.CameraObject.SetAspectRatio(self._ViewportWidth / self._ViewportHeight)

        elif isinstance(component, LightComponent):
            if   component.LightType == LightComponent.TypeEnum.Directional: self._DirectionalLight = component.Light

            elif component.LightType == LightComponent.TypeEnum.Point:
                component.Light.SetIndex( len( self._PointLights ) )
                self._PointLights.append(component.Light)

            elif component.LightType == LightComponent.TypeEnum.Spot:
                component.Light.SetIndex( len( self._SpotLights  ) )
                self._SpotLights.append(component.Light)
