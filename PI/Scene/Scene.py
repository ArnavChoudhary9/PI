from ..Core import PI_TIMER
from .Components import *
from .Entity     import Entity


from ..Renderer import Renderer, DirectionalLight
from ..Logging import PI_CORE_TRACE

import pyrr
import esper
import yaml

from typing import Deque as _Deque

class PI_YAML:
    @staticmethod
    def EncodeVector3(dumper: yaml.Dumper, vector: pyrr.Vector3) -> yaml.Dumper:
        return dumper.represent_sequence("Vector3", [float(vector[0]), float(vector[1]), float(vector[2])], flow_style=True)

    @staticmethod
    def DecodeVector3(loader: yaml.Loader, node: yaml.Node) -> pyrr.Vector3:
        return pyrr.Vector3(loader.construct_sequence(node))
        
    @staticmethod
    def EncodeVector4(dumper: yaml.Dumper, vector: pyrr.Vector4) -> yaml.Dumper:
        return dumper.represent_sequence(
            "Vector3",
            [ float(vector[0]), float(vector[1]), float(vector[2]), float(vector[3]) ],
            flow_style=True
        )

    @staticmethod
    def DecodeVector3(loader: yaml.Loader, node: yaml.Node) -> pyrr.Vector3:
        return pyrr.Vector3(loader.construct_sequence(node))

class Scene:
    _Registry: esper.World
    
    _ViewportWidth  : int = 1
    _ViewportHeight : int = 1

    _DirectionalLight: DirectionalLight = DirectionalLight(pyrr.Vector3([ 0, 0, 0 ]), intensity=0)

    _PointLights : _Deque[PointLight] = []
    _SpotLights  : _Deque[SpotLight]  = []

    def __init__(self) -> None:
        self._Registry = esper.World()

        class _ScriptProcessor(esper.Processor):
            def process(self, dt: float):
                timer = PI_TIMER("SctipoProcessor::process")
                for entity, script in self.world.get_component(ScriptComponent):
                    if script.Bound: script.OnUpdate(dt)

        class _TransformUpdater(esper.Processor):
            def process(self, dt: float):
                for entity, (meshComponent, transform) in self.world.get_components(MeshComponent, TransformComponent):
                    if not meshComponent.Initialized: continue
                    mesh = meshComponent.MeshObject

                    mesh.SetTranslation ( transform.Translation )
                    mesh.SetRotation    ( transform.Rotation    )
                    mesh.SetScale       ( transform.Scale       )
                
                for entity, (lightComponent, transform) in self.world.get_components(LightComponent, TransformComponent):
                    light = lightComponent.Light
                    light.SetPosition ( transform.Translation )

                for entity, (cameraComponent, transform) in self.world.get_components(CameraComponent, TransformComponent):
                    camera = cameraComponent.Camera.CameraObject
                    camera.SetPosition( transform.Translation )
                    camera.SetRotation( transform.Rotation    )

        self._Registry.add_processor(_ScriptProcessor())
        self._Registry.add_processor(_TransformUpdater())

    def __del__(self) -> None:
        for entityID in range(1, self._Registry._next_entity_id+1):
            if not self._Registry.entity_exists(entityID): continue
            self.DestroyEntity(Entity(entityID, self))

    @staticmethod
    def Serialize(scene, path: str) -> None:
        data = {}
        data["Scene"] = "Untitled"

        entities = []
        for entityID in range(1, scene._Registry._next_entity_id+1):
            if not scene._Registry.entity_exists(entityID): continue
            entity = Entity(entityID, scene)
            
            entityDict = {}
            entityDict["Entity"] = 1234567890123456

            if entity.HasComponent(TagComponent):
                entityDict["TagComponent"] = { "Tag": entity.GetComponent(TagComponent).Tag }
            
            if entity.HasComponent(TransformComponent):
                tc = entity.GetComponent(TransformComponent)
                entityDict["TransformComponent"] = {
                    "Translation": tc.Translation,
                    "Rotation"   : tc.Rotation,
                    "Scale"      : tc.Scale      
                }

            if entity.HasComponent(MeshComponent):
                mc = entity.GetComponent(MeshComponent)
                entityDict["MeshComponent"] = { "Path": mc.Path }

            if entity.HasComponent(CameraComponent):
                cc = entity.GetComponent(CameraComponent)
                cameraComponent = {}

                sceneCamera = {}
                sceneCamera["ProjectionType"] = cc.Camera.ProjectionType

                cameraComponent["Camera"] = sceneCamera
                cameraComponent["IsPrimary"] = cc.Primary
                cameraComponent["FixedAspectRatio"] = cc.FixedAspectRatio

                entityDict["CameraComponent"] = cameraComponent

            if entity.HasComponent(LightComponent):
                lc = entity.GetComponent(LightComponent)
                lightDict = {}

                lightDict["LightType"] = lc.LightType
                lightDict["Intensity"] = lc.Light.Intensity

                lightDict["Diffuse"] = lc.Light.Diffuse
                lightDict["Specular"] = lc.Light.Specular

                if lc.LightType is LightComponent.TypeEnum.Directional:
                    lightDict["Direction"] = lc.Light.Direction

                if lc.LightType is LightComponent.TypeEnum.Spot:
                    lightDict["Direction"] = lc.Light.Direction
                    lightDict["CutOff"] = lc.Light.CutOff
                    lightDict["OuterCutOff"] = lc.Light.OuterCutOff

                entityDict["LightComponent"] = lightDict

            entities.append(entityDict)

        data["Entities"] = entities

        yaml.add_representer(pyrr.Vector3, PI_YAML.EncodeVector3)
        with open(path, 'w') as _file: yaml.dump(data, _file)
    
    @staticmethod
    def Deserialize(oldScene, path: str):
        yaml.add_constructor("Vector3", PI_YAML.DecodeVector3)
        
        data = {}
        with open(path, 'r') as _file: data = yaml.load(_file, yaml.Loader)

        scene = Scene()
        scene.OnViewportResize(oldScene._ViewportWidth, oldScene._ViewportHeight)

        entities = data["Entities"]
        for entity in entities:
            uuid = entity["Entity"]

            name = ""
            tagComponent = entity["TagComponent"]
            name = tagComponent["Tag"]
            PI_CORE_TRACE("Deserialized entity with ID = {}, name = {}", uuid, name)

            deserializedEntity = scene.CreateEntity(name)

            transformComponent = entity["TransformComponent"]
            tc = deserializedEntity.GetComponent(TransformComponent)
            tc.SetTranslation(transformComponent["Translation"])
            tc.SetRotation(transformComponent["Rotation"])
            tc.SetScale(transformComponent["Scale"])

            meshComponent = entity.get("MeshComponent", False)
            if meshComponent: deserializedEntity.AddComponent(MeshComponent, meshComponent["Path"]).Init()

            cameraComponent = entity.get("CameraComponent", False)
            if cameraComponent: deserializedEntity.AddComponent(
                    CameraComponent,
                    SceneCamera(cameraComponent["Camera"]["ProjectionType"]),
                    cameraComponent["IsPrimary"], cameraComponent["FixedAspectRatio"]
                )

            lightComponent = entity.get("LightComponent", False)
            if lightComponent:
                lightType = lightComponent["LightType"]

                if lightType is LightComponent.TypeEnum.Point:
                    deserializedEntity.AddComponent(LightComponent, lightType,
                        diffuse=lightComponent["Diffuse"],
                        specular=lightComponent["Specular"],
                        intensity=lightComponent["Intensity"]
                    )

                if lightType is LightComponent.TypeEnum.Directional:
                    deserializedEntity.AddComponent(LightComponent, lightType,
                        direction=lightComponent["Direction"],
                        diffuse=lightComponent["Diffuse"],
                        specular=lightComponent["Specular"],
                        intensity=lightComponent["Intensity"]
                    )

                if lightType is LightComponent.TypeEnum.Spot:
                    deserializedEntity.AddComponent(LightComponent, lightType,
                        direction=lightComponent["Direction"],
                        cutOff=lightComponent["CutOff"],
                        outerCutOff=lightComponent["OuterCutOff"],
                        diffuse=lightComponent["Diffuse"],
                        specular=lightComponent["Specular"],
                        intensity=lightComponent["Intensity"]
                    )

        del oldScene
        return scene

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

    def OnUpdate(self, dt: float) -> None: self._Registry.process(dt)
        
    def Draw(self) -> None:
        meshes = []
        for entity, meshComponent in self._Registry.get_component(MeshComponent):
            if not meshComponent.Initialized: continue
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

        elif isinstance(component, ScriptComponent) : component.ImportModule()
        elif isinstance(component, MeshComponent)   : component.Init()
