from ..Renderer  import Camera, EditorCamera, RenderCommand
from ..Core      import PI_TIMER, PI_VERSION, Cache, Random
from .Components import *
from .Entity     import Entity
from ..Scripting import Color4, Color3

from ..Renderer import Renderer, DirectionalLight
from ..Logging  import PI_CORE_TRACE

from copy import deepcopy
import pyrr
import esper
import yaml
import os

from typing import Deque as _Deque

class PI_YAML:
    @staticmethod
    def EncodeVector3(dumper: yaml.Dumper, vector: pyrr.Vector3) -> yaml.Dumper:
        return dumper.represent_sequence("Vector3", [float(vector[0]), float(vector[1]), float(vector[2])], flow_style=True)

    @staticmethod
    def DecodeVector3(loader: yaml.Loader, node: yaml.Node) -> pyrr.Vector3:
        return pyrr.Vector3(loader.construct_sequence(node))
        
    @staticmethod
    def EncodeColor3(dumper: yaml.Dumper, color: Color3) -> yaml.Dumper:
        return dumper.represent_sequence(
            "Color3",
            [ float(color[0]), float(color[1]), float(color[2]) ],
            flow_style=True
        )

    @staticmethod
    def DecodeColor3(loader: yaml.Loader, node: yaml.Node) -> Color3:
        return Color3(loader.construct_sequence(node))
        
    @staticmethod
    def EncodeColor4(dumper: yaml.Dumper, color: Color4) -> yaml.Dumper:
        return dumper.represent_sequence(
            "Color4",
            [ float(color[0]), float(color[1]), float(color[2]), float(color[3]) ],
            flow_style=True
        )

    @staticmethod
    def DecodeColor4(loader: yaml.Loader, node: yaml.Node) -> Color4:
        return Color4(loader.construct_sequence(node))
        
    @staticmethod
    def EncodeVector4(dumper: yaml.Dumper, vector: pyrr.Vector4) -> yaml.Dumper:
        return dumper.represent_sequence(
            "Vector3",
            [ float(vector[0]), float(vector[1]), float(vector[2]), float(vector[3]) ],
            flow_style=True
        )

    @staticmethod
    def DecodeVector4(loader: yaml.Loader, node: yaml.Node) -> pyrr.Vector4:
        return pyrr.Vector4(loader.construct_sequence(node))

class Scene:
    _Registry: esper.World
    
    _ViewportWidth  : int = 1
    _ViewportHeight : int = 1

    _DirectionalLight: DirectionalLight = DirectionalLight(pyrr.Vector3([ 0, 0, 0 ]), intensity=0)

    _PointLights : _Deque[PointLight]
    _SpotLights  : _Deque[SpotLight]

    _DrawCamera: Camera

    _Filepath : str = None

    def __init__(self) -> None:
        self._Registry = esper.World()

        self._PointLights = []
        self._SpotLights = []

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
        self._Registry.add_processor(_TransformUpdater())

    @staticmethod
    def Serialize(scene, path: str) -> None:
        data = {}
        data["Scene"] = "Untitled"
        data["Version"] = PI_VERSION

        entities = []
        for entityID in range(1, scene._Registry._next_entity_id+1):
            if not scene._Registry.entity_exists(entityID): continue
            entity = Entity(entityID, scene)
            
            entityDict = {}
            entityDict["Entity"] = str(entity.GetComponent(IDComponent))

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

            if entity.HasComponent(ScriptComponent):
                component = entity.GetComponent(ScriptComponent)
                entityDict["ScriptComponent"] = {"Path": component.Path, "Variables": component.Variables}

            entities.append(entityDict)

        data["Entities"] = entities

        yaml.add_representer( Color3       , PI_YAML.EncodeColor3  )
        yaml.add_representer( pyrr.Vector3 , PI_YAML.EncodeVector3 )
        yaml.add_representer( Color4       , PI_YAML.EncodeColor4  )
        yaml.add_representer( pyrr.Vector4 , PI_YAML.EncodeVector4 )
        with open(path, 'w') as _file: yaml.dump(data, _file)
    
    @staticmethod
    def Deserialize(oldScene, path: str):
        yaml.add_constructor( "Color3"  , PI_YAML.DecodeColor3  )
        yaml.add_constructor( "Vector3" , PI_YAML.DecodeVector3 )
        yaml.add_constructor( "Color4"  , PI_YAML.DecodeColor4  )
        yaml.add_constructor( "Vector4" , PI_YAML.DecodeVector4 )
        
        data = {}
        with open(path, 'r') as _file: data = yaml.load(_file, yaml.Loader)

        scene = Scene()
        scene.OnViewportResize(oldScene._ViewportWidth, oldScene._ViewportHeight)

        entities = data["Entities"]
        for entity in entities:
            uuid = entity["Entity"]

            tagComponent = entity["TagComponent"]
            name = tagComponent["Tag"]

            deserializedEntity = scene.CreateEntityWithUUID(UUID(uuid), name)

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
            
            scriptComponent = entity.get("ScriptComponent", False)
            if scriptComponent:
                component = deserializedEntity.AddComponent(ScriptComponent, scriptComponent["Path"])
                variables = scriptComponent.get("Variables", False)
                if variables: component.SetVariables(variables)

        scene._Filepath = path
        return scene

    @staticmethod
    def Copy(oldScene):
        tempSceneName = "TempScene"
        tempFileDir = f"{Cache.GetLocalTempDirectory()}\\{tempSceneName}.PI"

        Scene.Serialize(oldScene, tempFileDir)
        newScene = Scene.Deserialize(oldScene, tempFileDir)
        os.remove(tempFileDir)

        return newScene

    @staticmethod
    def CopyComponent(ComponentType: CTV, srcRegistry: esper.World, dstRegistry: esper.World, uuidEntityMap: Dict[UUID, int]) -> None:
        for entity, (component, idComponent) in srcRegistry.get_components(ComponentType, IDComponent):
            uuid = idComponent.ID

            dstEntity = uuidEntityMap.get(uuid, None)
            PI_CORE_ASSERT(dstEntity != None, "Cannot find entity with matching UUID.")

            if ComponentType is MeshComponent: dstRegistry.add_component(dstEntity, component)
            elif ComponentType is ScriptComponent: dstRegistry.add_component(dstEntity, component.Copy())
            else: dstRegistry.add_component(dstEntity, deepcopy(component))

    def CreateEntity(self, name: str="Entity") -> Entity: return self.CreateEntityWithUUID(UUIDGenerator(), name)

    def CreateEntityWithUUID(self, uuid: UUID, name: str="Entity") -> Entity:
        entity = Entity(self._Registry.create_entity(), self)
        entity.AddComponent(IDComponent, uuid)
        entity.AddComponent(TagComponent, name)
        entity.AddComponent(TransformComponent)
        return entity

    def DestroyEntity(self, entity: Entity) -> None:
        if entity.HasComponent(LightComponent):
            light = entity.GetComponent(LightComponent).Light

            if   isinstance(light, DirectionalLight) : self._DirectionalLight.SetIntensity(0)
            
            elif isinstance(light, SpotLight):
                newLights = []

                for _light in self._SpotLights:
                    if _light is light: continue
                    _light.SetIndex(len(newLights))
                    newLights.append(_light)

                self._SpotLights = newLights

            elif isinstance(light, PointLight):
                newLights = []

                for _light in self._PointLights:
                    if _light is light: continue
                    _light.SetIndex(len(newLights))
                    newLights.append(_light)

                self._PointLights = newLights

        self._Registry.delete_entity(int(entity))

    def OnUpdateEditor(self, dt: float, camera: EditorCamera) -> None:
        self._DrawCamera = camera
        self._Registry.process(dt)

    def OnUpdateRuntime(self, dt: float) -> None:
        self._DrawCamera = None
        timer = PI_TIMER("Scene::OnUpdateRuntime")
        for entity, script in self._Registry.get_component(ScriptComponent):
            if script.Bound: script.OnUpdate(dt)
        self._Registry.process(dt)
        
    def Draw(self) -> None:
        if self._DrawCamera is None and self.PrimaryCameraEntity is None: return

        with Renderer.BeginScene(self, self._DrawCamera):
            for entity, meshComponent in self._Registry.get_component(MeshComponent):
                if not meshComponent.Initialized: continue
                mesh = meshComponent.MeshObject
                camera = self._DrawCamera if self._DrawCamera else self.PrimaryCameraEntity.GetComponent(CameraComponent).Camera.CameraObject
                
                mesh.Bind(
                    self._DirectionalLight,
                    self._PointLights, len(self._PointLights),
                    self._SpotLights , len(self._SpotLights),
                    camera.Position
                )

                mesh.Material.SetViewProjection(camera.ViewProjectionMatrix)
                mesh.Material.Shader.SetInt("u_EntityID", entity)

                mesh.VertexArray.Bind()
                RenderCommand.DrawIndexed(mesh.VertexArray)

                mesh.VertexArray.Unbind()
                mesh.Material.Shader.Unbind()

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

    def _OnComponentRemoved(self, entity: Entity, component: CTV) -> None:
        if isinstance(component, LightComponent):
            light = component.Light

            if   isinstance(light, DirectionalLight): self._DirectionalLight.SetIntensity(0)
            
            elif isinstance(light, SpotLight):
                newLights = []

                for _light in self._SpotLights:
                    if _light is light: continue
                    _light.SetIndex(len(newLights))
                    newLights.append(_light)

                self._SpotLights = newLights
            
            elif isinstance(light, PointLight):
                newLights = []

                for _light in self._PointLights:
                    if _light is light: continue
                    _light.SetIndex(len(newLights))
                    newLights.append(_light)

                self._PointLights = newLights
