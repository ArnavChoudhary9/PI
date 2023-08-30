from ..Renderer  import Camera, EditorCamera, RenderCommand, Material
from ..Core      import PI_TIMER, PI_VERSION, Timer
from ..Utility   import Cache
from .Components import *
from .Entity     import Entity
from ..Scripting import Color4, Color3

from ..Renderer import Renderer, DirectionalLight

from ..AssetManager.AssetManager import AssetManager

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

    __ToDestroy: List[Entity]
    __ToDuplicate: List[Entity]

    __Running: bool
    __RBWorld: PySics

    def __init__(self) -> None:
        self._Registry = esper.World()

        self._PointLights = []
        self._SpotLights = []

        self.__Running = False

        self.__ToDestroy = []
        self.__ToDuplicate = []

        class _TransformUpdater(esper.Processor):
            def process(self, dt: float, running: bool):                
                for entity, (lightComponent, transform) in self.world.get_components(LightComponent, TransformComponent):
                    light = lightComponent.Light
                    light.SetPosition ( transform.Translation )

                for entity, (cameraComponent, transform) in self.world.get_components(CameraComponent, TransformComponent):
                    camera = cameraComponent.Camera.CameraObject
                    camera.SetPosition( transform.Translation )
                    camera.SetRotation( transform.Rotation    )

                if not running: return
                for entity, (rbComponent, transform) in self.world.get_components(RigidBodyComponent, TransformComponent):
                    transform.SetTranslation(rbComponent.RigidBody.Position)
                    transform.SetRotation(rbComponent.RigidBody.Rotation)

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
                entityDict["MeshComponent"] = { "Path": AssetManager.GetInstance().GetRelativePath(mc.Path) }

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
                if component.Bound:
                    entityDict["ScriptComponent"] = {"Namespace": component.Namespace, "Variables": component.Variables}

            if entity.HasComponent(CollidorComponent):
                component = entity.GetComponent(CollidorComponent)
                entityDict["CollidorComponent"] = { "Type": component.Type, "Scale": component.Collidor.Scale }

            if entity.HasComponent(RigidBodyComponent):
                component = entity.GetComponent(RigidBodyComponent)
                entityDict["RigidBodyComponent"] = {
                    "IsStatic": component.RigidBody.IsStatic, "Mass": component.RigidBody.Mass 
                }

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
                namespace = scriptComponent["Namespace"]
                module, script = namespace.split(".")
                component = deserializedEntity.AddComponent(ScriptComponent, module, script)
                variables = scriptComponent.get("Variables", False)
                if variables: component.SetVariables(variables)
            
            collidorComponent = entity.get("CollidorComponent", False)
            if collidorComponent:
                collidor = deserializedEntity.AddComponent(CollidorComponent, collidorComponent["Type"])
                collidor.Collidor.SetScale(collidorComponent["Scale"])
            
            rigidbodyComponent = entity.get("RigidBodyComponent", False)
            if rigidbodyComponent:
                transform: TransformComponent = deserializedEntity.GetComponent(TransformComponent)

                collidor: Collider = None
                if deserializedEntity.HasComponent(CollidorComponent):
                    collidor = deserializedEntity.GetComponent(CollidorComponent).Collidor
                else:
                    collidor = deserializedEntity.AddComponent(CollidorComponent, CollidorComponent.Shapes.Box).Collidor
                    collidor.SetScale(transform.Scale)

                mat = PySicsMaterial(
                    mass=rigidbodyComponent["Mass"], isStatic=rigidbodyComponent["IsStatic"],
                    position=transform.Translation, rotation=transform.Rotation, collider=collidor
                )
                rb = deserializedEntity.AddComponent(RigidBodyComponent, mat)

        scene._Filepath = path
        return scene

    @staticmethod
    def Copy(oldScene):
        tempSceneName = str(UUIDGenerator())
        tempFileDir = f"{Cache.GetLocalTempDirectory()}\\{tempSceneName}.PI"

        Scene.Serialize(oldScene, tempFileDir)
        newScene = Scene.Deserialize(oldScene, tempFileDir)
        os.remove(tempFileDir)

        return newScene

    @staticmethod
    def CopyComponent(component: CTV, dstEntity: Entity) -> None:
        if type(component) in [IDComponent, TagComponent, TransformComponent]: return
        if dstEntity.HasComponent(type(component)): return
        dstEntity._AddComponentInstance(component.Copy(dstEntity))

    def CreateEntity(self, name: str="Entity") -> Entity: return self.CreateEntityWithUUID(UUIDGenerator(), name)

    def CreateEntityWithUUID(self, uuid: UUID, name: str="Entity") -> Entity:
        entity = Entity(self._Registry.create_entity(), self)
        entity.AddComponent(IDComponent, uuid)
        entity.AddComponent(TagComponent, name)
        entity.AddComponent(TransformComponent)
        return entity

    def DuplicateEntity(self, entity: Entity) -> Entity:
        newEntity = self.CreateEntity(entity.GetComponent(TagComponent).Tag)
        
        newTC = newEntity .GetComponent( TransformComponent )
        oldTC = entity    .GetComponent( TransformComponent ).Copy(newEntity)
        newTC.SetTranslation ( oldTC.Translation )
        newTC.SetRotation    ( oldTC.Rotation    )
        newTC.SetScale       ( oldTC.Scale       )
        
        for component in entity.AllComponents: Scene.CopyComponent(component, newEntity)
        return newEntity

    def DefferedDuplicateEntity(self, entity: Entity) -> None:
        if entity not in self.__ToDuplicate: self.__ToDuplicate.append(entity)

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

        if entity.HasComponent(RigidBodyComponent):
            if not self.__Running: return
            self.__RBWorld.DeleteRigidBody(entity.GetComponent(RigidBodyComponent).RigidBody)

        self._Registry.delete_entity(int(entity), immediate=True)

    def DefferedDestroy(self, entity: Entity) -> None:
        if entity not in self.__ToDestroy: self.__ToDestroy.append(entity)

    def OnStartRuntime(self) -> None:
        self.__Running = True
        self.__RBWorld = PySics()

        for entity, script in self._Registry.get_component(ScriptComponent):
            if script.Bound: script.OnAttach()

        for entity, rb in self._Registry.get_component(RigidBodyComponent):
            self.__RBWorld.AddRigidBody(rb.RigidBody)

        self.__RBWorld.OnSimulationStart()

    def OnStopRuntime(self) -> None:
        self.__Running = False
        
        try:
            self.__RBWorld.OnSimulationEnd()
            del self.__RBWorld
        except: pass

        for entity, script in self._Registry.get_component(ScriptComponent):
            if script.Bound:
                script.OnDetach()
                script.Reload()

    def HandleDefferedStuff(self) -> None:
        for entity in self.__ToDuplicate:
            self.__ToDuplicate.remove(entity)
            self.DuplicateEntity(entity)

        for entity in self.__ToDestroy:
            self.__ToDestroy.remove(entity)
            self.DestroyEntity(entity)

    def OnUpdateEditor(self, dt: float, camera: EditorCamera) -> None:
        self._DrawCamera = camera
        self._Registry.process(dt, self.__Running)
        self.HandleDefferedStuff()

    def OnUpdateRuntime(self, dt: float) -> None:
        self._DrawCamera = None
        for entity, script in self._Registry.get_component(ScriptComponent):
            if script.Bound: script.OnUpdate(dt)
 
        self.__RBWorld.Update(dt)
        self._Registry.process(dt, self.__Running)

        self.HandleDefferedStuff()
    
    def Draw(self) -> None:
        if self._DrawCamera is None and self.PrimaryCameraEntity is None: return
        camera = self._DrawCamera if self._DrawCamera else \
            self.PrimaryCameraEntity.GetComponent(CameraComponent).Camera.CameraObject

        with Renderer.BeginScene(self, self._DrawCamera):
            for entity, (meshComponent, materialComponent, transform) in \
                self._Registry.get_components(MeshComponent, MaterialComponent, TransformComponent):

                if not meshComponent.Initialized: continue

                mesh = meshComponent.MeshObject

                mesh.SetTranslation ( transform.Translation )
                mesh.SetRotation    ( transform.Rotation    )
                mesh.SetScale       ( transform.Scale       )

                mesh._RecalculateTransform()

                material: Material = materialComponent.MaterialObject
                material.Bind()
                material.SetFields(mesh, camera.Position)

                # Light stuff
                if Material.Type.Is(material.MatType, Material.Type.Lit):
                    self._DirectionalLight.UploadPropertiesToShader(material.Shader)
                
                    for light in self._PointLights:
                        light.UploadPropertiesToShader(material.Shader)
                
                    for light in self._SpotLights:
                        light.UploadPropertiesToShader(material.Shader)

                    material.Shader.SetInt("u_NumPointLights", len(self._PointLights))
                    material.Shader.SetInt("u_NumSpotLights", len(self._SpotLights))

                material.SetViewProjection(camera.ViewProjectionMatrix)
                material.Shader.SetInt("u_EntityID", entity)

                RenderCommand.DrawIndexed(mesh.VertexArray)

                material.Shader.Unbind()
                mesh.VertexArray.Unbind()

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

        elif isinstance(component, ScriptComponent):
            component.Bind()
            if self.__Running: component.OnAttach()

        elif isinstance(component, MeshComponent):
            component.Init()
            if component.Path != "" and not entity.HasComponent(MaterialComponent):
                entity.AddComponent(MaterialComponent, component.Path)
        
        elif isinstance(component, MaterialComponent): component.Init()

        elif isinstance(component, RigidBodyComponent):
            if self.__Running: self.__RBWorld.AddRigidBody(component.RigidBody)

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

        if isinstance(component, RigidBodyComponent):
            if not self.__Running: return
            self.__RBWorld.DeleteRigidBody(component.RigidBody)
