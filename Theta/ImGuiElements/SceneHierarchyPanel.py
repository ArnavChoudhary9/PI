from PI import *
from .UndoManager import *

import os
import imgui

class SceneHierarchyPanel:
    __Context          : Scene
    __SelectionContext : Entity
    __CopiedTransform  : TransformComponent
    __CopiedComponent  : CTV

    def __init__(self, project: Project) -> None:
        self.__Context = Scene()
        self.__SelectionContext = None
        self.__CopiedTransform: TransformComponent = None
        self.__CopiedComponent: CTV = None

    def OnImGuiRender(self) -> None:
        with imgui.begin("Scene Heirarchy"):
            for entity in self.__Context._Registry._entities.keys():
                self.__DrawEntityNode(Entity(entity, self.__Context))

            if imgui.is_mouse_down(0) and imgui.is_window_hovered(): self.__SelectionContext = None

            if imgui.begin_popup_context_window(popup_flags=imgui.POPUP_NO_OPEN_OVER_ITEMS|imgui.POPUP_MOUSE_BUTTON_RIGHT):
                if imgui.menu_item("Create Empty Entity")[0]: self.__Context.CreateEntity("Empty Entity")
                imgui.end_popup()

        with imgui.begin("Properties"):
            if self.__SelectionContext is not None:
                self.__DrawComponents(self.__SelectionContext)
                if self.__CopiedComponent and \
                    imgui.begin_popup_context_window( popup_flags=imgui.POPUP_NO_OPEN_OVER_ITEMS|imgui.POPUP_MOUSE_BUTTON_RIGHT):
                    if imgui.menu_item("Paste Component")[0]:
                        componentType = type(self.__CopiedComponent)
                        if self.__SelectionContext.HasComponent(componentType):
                            self.__SelectionContext.RemoveComponent(componentType)
                        self.__SelectionContext._AddComponentInstance(self.__CopiedComponent.Copy(self.__SelectionContext))
                        self.__CopiedComponent = None
                    imgui.end_popup()

    def __DrawEntityNode(self, entity: Entity) -> None:
        tag = entity.GetComponent(TagComponent)

        flags = 0
        if self.__SelectionContext is entity: flags = imgui.TREE_NODE_SELECTED
        flags |= imgui.TREE_NODE_OPEN_ON_ARROW | imgui.TREE_NODE_SPAN_AVAILABLE_WIDTH

        # Adding this to make each entity unique
        # NOTE: int(entity) retrives its __EntityHandle
        opened = imgui.tree_node(str(tag) + f"##{int(entity)}", flags=flags)
        if imgui.is_item_clicked(): self.__SelectionContext = entity
        
        if imgui.begin_popup_context_item():
            if imgui.menu_item("Duplicate Entity") [0]: self.__Context.DefferedDuplicateEntity(entity)
            if imgui.menu_item("Delete Entity")    [0]:
                self.__Context.DefferedDestroy(entity)
                if self.__SelectionContext == entity: self.__SelectionContext = None
            imgui.end_popup()

        if opened: imgui.tree_pop()

    def DrawComponent(self, name: str, entity: Entity, componentType: CTV, UIfunction) -> None:
        flags = imgui.TREE_NODE_DEFAULT_OPEN | imgui.TREE_NODE_FRAMED | imgui.TREE_NODE_SPAN_AVAILABLE_WIDTH | \
            imgui.TREE_NODE_ALLOW_ITEM_OVERLAP | imgui.TREE_NODE_FRAME_PADDING
        
        if entity.HasComponent(componentType):
            component = entity.GetComponent(componentType)
            contentReginAvailable = imgui.get_content_region_available()

            imgui.push_style_var(imgui.STYLE_FRAME_PADDING, ( 4, 4 ))
            lineHeight = 26
            imgui.separator()
            isOpen = imgui.tree_node(name, flags)
            imgui.pop_style_var()

            imgui.same_line(contentReginAvailable.x - lineHeight * 0.5)
            if imgui.button("+", lineHeight, lineHeight): imgui.open_popup("ComponentSettings")

            removeComponent = False
            if imgui.begin_popup("ComponentSettings"):
                if imgui.menu_item("Remove Component")[0]: removeComponent = True

                if componentType is TransformComponent:
                    if imgui.menu_item("Copy Transform")[0]: self.__CopiedTransform = entity.GetComponent(TransformComponent)
                    if self.__CopiedTransform and imgui.menu_item("Paste Transform")[0]:
                        transfrom = entity.GetComponent(TransformComponent).Copy(entity)
                        transfrom.SetTranslation ( self.__CopiedTransform.Translation )
                        transfrom.SetRotation    ( self.__CopiedTransform.Rotation    )
                        transfrom.SetScale       ( self.__CopiedTransform.Scale       )
                        self.__CopiedTransform = None
                    
                else:
                    if imgui.menu_item("Copy Component")[0]: self.__CopiedComponent = entity.GetComponent(componentType)
                    if self.__CopiedComponent and isinstance(self.__CopiedComponent, componentType) \
                        and imgui.menu_item("Paste Component")[0]:
                        entity.RemoveComponent(componentType)
                        entity._AddComponentInstance(self.__CopiedComponent.Copy(entity))
                        self.__CopiedComponent = None
                    
                imgui.end_popup()

            if isOpen:
                UIfunction(entity, component)
                imgui.tree_pop()

            if removeComponent:
                UndoManager.GetInstance().PushUndo(ComponentDeletionEvent(entity.GetComponent(componentType), entity))
                entity.RemoveComponent(componentType)

    # ---------------------- Component UI Functions ----------------------
    @staticmethod
    def __TransformUIFunction(entity: Entity, component: TransformComponent) -> None:
        changedT, newT = UILib.DrawVector3Controls("Translation", component.Translation)
        changedR, newR = UILib.DrawVector3Controls("Rotation", component.Rotation, 0, 0.5 )
        changedS, newS = UILib.DrawVector3Controls("Scale", component.Scale, 1)

        if changedT or changedR or changedS:
            UndoManager().GetInstance().PushUndo(ComponentChangedEvent(component, entity,
                prevVals= (
                    component.Translation,
                    component.Rotation,
                    component.Scale
                ), 
                newVals=( newT, newR, newS )))
            
            component.SetTranslation(newT)
            component.SetRotation(newR)
            component.SetScale(newS)
    @staticmethod
    def __MeshUIFunction(entity: Entity, component: MeshComponent) -> None:
        path = AssetManager.GetInstance().GetRelativePath(component.Path)
        changed, path, dragDrop = UILib.DrawTextFieldControls(
            "Filter", path, acceptDragDrop=True,
            filter=".obj", tooltip="You can drag drop meshes from Content Browser.")

        if changed: 
            if not dragDrop: path = AssetManager.GetInstance().GetAbsolutePath(path)
            component.Path = path

        if (Input.IsKeyPressed(PI_KEY_ENTER) or dragDrop):
            if not os.path.exists(component.Path):
                PI_CLIENT_WARN("Trying to load invalid Model")
                DebugConsole.Warn("Trying to load invalid Model")
                if hasattr(component, "MeshObject"): component.Path = component.MeshObject.Path
                else: component.Path = ""
                return

            if not component.Path.endswith((".obj",)):
                if hasattr(component, "MeshObject"): component.Path = component.MeshObject.Path
                else: component.Path = ""
                return

            entity.RemoveComponent(MeshComponent)
            if entity.HasComponent(MaterialComponent): entity.RemoveComponent(MaterialComponent)
            entity.AddComponent(MeshComponent, component.Path).Init()
    @staticmethod
    def __MaterialUIFunction(entity: Entity, component: MaterialComponent) -> None:
        changed, component.Textured = UILib.DrawBoolControls("Textured", component.Textured)

        changed, color = UILib.DrawColor4Controls("Diffuse", component.MaterialObject.Diffuse)
        if changed: component.MaterialObject.SetDiffuse(color)

        if component.Textured:
            pass
        elif Material.Type.Is(component.MaterialObject.MatType, Material.Type.Textured):
            component.MaterialObject.SetType(component.MaterialObject.MatType ^ Material.Type.Textured)
        
        changed, color = UILib.DrawColor4Controls("Specular", component.MaterialObject.Specular)
        if changed: component.MaterialObject.SetSpecular(color)
        
        changed, shininess = UILib.DrawIntControls("Shininess", component.MaterialObject.Shininess,
            minValue=1, maxValue=128)
        if changed: component.MaterialObject.SetShininess(shininess)
    @staticmethod
    def __ScriptUIFunction(entity: Entity, component: ScriptComponent) -> None:
        if component.Bound:
            component.Reload()
            for name, instance in component.Variables.items():
                variableChanged, new = False, instance

                if isinstance(instance, pyrr.Vector3):
                    variableChanged, new = UILib.DrawVector3Controls(name, instance, columnWidth=100)

                if isinstance(instance, str):
                    variableChanged, new = UILib.DrawTextFieldControls(name, instance, columnWidth=100)
                
                if isinstance(instance, float):
                    variableChanged, new = UILib.DrawFloatControls(name, instance, columnWidth=100)
                
                if isinstance(instance, int) and not isinstance(instance, bool):
                    variableChanged, new = UILib.DrawIntControls(name, instance, columnWidth=100)

                if isinstance(instance, bool):
                    variableChanged, new = UILib.DrawBoolControls(name, instance, columnWidth=100)
                    new = bool(new)

                if isinstance(instance, Color4):
                    variableChanged, new = UILib.DrawColor4Controls(name, instance, columnWidth=100)
                    new = Color4(new)
                
                if variableChanged: component.SetVariables({name: new})
            if len(component.Variables) != 0: imgui.text("")

        modules = ScriptingEngine.Modules
        scripts = ['.']
        for name, module in modules.items():
            for script_name, script in module.AllScriptsExtending(Behaviour).items():
                scripts.append(f"{name}.{script_name}")

        try: changed, index, namespace = UILib.DrawDropdown("Script", scripts.index(component.Namespace), scripts)
        except ValueError as _:
            changed, index, namespace = UILib.DrawDropdown("Script", 0, scripts)

        if changed:
            entity.RemoveComponent(ScriptComponent)
            module, script = namespace.split('.')
            entity.AddComponent(ScriptComponent, module, script)
    @staticmethod
    def __LightUIFunction(entity: Entity, component: LightComponent) -> None:
        lightTypes = ["Directional", "Point", "Spot"]
        changed, lightType, lightTypeStr = UILib.DrawDropdown("Light Type", component.LightType, lightTypes, columnWidth=100)
        if changed:
            entity.RemoveComponent(LightComponent)

            if lightType is LightComponent.TypeEnum.Point : entity.AddComponent(LightComponent, lightType)
            if lightType is LightComponent.TypeEnum.Spot  : entity.AddComponent(LightComponent, lightType) 

        changed, new = UILib.DrawFloatControls("Intensity", component.Light.Intensity, minValue=0.01, maxValue=1000)
        if changed: component.Light.SetIntensity(new)
        
        imgui.separator()
        if isinstance(component.Light, SpotLight):
            light = component.Light

            changed, new = UILib.DrawFloatControls("Inner Angle", light.CutOff,
                speed=0.1, minValue=0.01, maxValue=light.OuterCutOff)
            if changed: light.SetCutOff(new)
            
            changed, new = UILib.DrawFloatControls("Outer Angle", light.OuterCutOff,
                speed=0.1, minValue=light.CutOff, maxValue=359.99)
            if changed: light.SetOuterCutOff(new)

        isEqual = component.Light.Diffuse is component.Light.Ambient is component.Light.Specular
        changed, lock = UILib.DrawBoolControls("Lock", isEqual)

        if changed and not lock:
            component.Light.SetAmbient(component.Light.Diffuse + (1 / 255))
            component.Light.SetSpecular(component.Light.Diffuse + (1 / 255))

        changed, new = UILib.DrawColor3Controls("Diffuse", component.Light.Diffuse)
        if changed: component.Light.SetDiffuse(pyrr.Vector3(new))
        
        changed, new = UILib.DrawColor3Controls("Ambient", component.Light.Ambient)
        if changed and not lock: component.Light.SetAmbient(pyrr.Vector3(new))
        
        changed, new = UILib.DrawColor3Controls("Specular", component.Light.Specular)
        if changed and not lock: component.Light.SetSpecular(pyrr.Vector3(new))
        
        if lock:
            component.Light.SetAmbient(component.Light.Diffuse)
            component.Light.SetSpecular(component.Light.Diffuse)
        imgui.separator()
    @staticmethod
    def __CameraUIFunction(entity: Entity, component: CameraComponent) -> None:
        camera = component.Camera
        projections = ["Orthographic", "Perspective"]
        
        changed, new = UILib.DrawBoolControls("Primary", component.Primary)
        if changed: component.Primary = new

        projectionChanged, projection, projStr = UILib.DrawDropdown("Projection", camera.ProjectionType, projections, columnWidth=100)
        if projectionChanged: camera.SetProjection(projection)

        imgui.separator()
        if projection is SceneCamera.ProjectionTypeEnum.Orthographic:
            camera: OrthographicCamera = camera.CameraObject

            changed, new = UILib.DrawFloatControls("Scale", camera.Scale)
            if changed: camera.SetScale(new)

            changed, camera._Near = UILib.DrawFloatControls("Near", camera._Near, minValue=0.01, maxValue=1000)
            if changed: camera.SetScale(camera.Scale)

            changed, camera._Far = UILib.DrawFloatControls("Far", camera._Far, minValue=0.01, maxValue=1000)
            if changed: camera.SetScale(camera.Scale)

            changed, component.FixedAspectRatio = UILib.DrawBoolControls(
                "Fixed Aspect Ratio", component.FixedAspectRatio, columnWidth=125
            )

        elif projection is SceneCamera.ProjectionTypeEnum.Perspective:
            camera: PerspectiveCamera = camera.CameraObject

            changed, new = UILib.DrawFloatControls("FOV", camera.FOV, minValue=0.01, maxValue=359.99)
            if changed: camera.SetFOV(new)

            changed, new = UILib.DrawFloatControls("Near", camera._Near, minValue=0.01, maxValue=1000)
            if changed:
                camera._Near = new
                camera.RecalculateProjection()

            changed, new = UILib.DrawFloatControls("Far", camera._Far, minValue=0.01, maxValue=1000)
            if changed:
                camera._Far = new
                camera.RecalculateProjection()
    @staticmethod
    def __CollidorUIFunction(entity: Entity, component: CollidorComponent) -> None:
        shapes = ["Box", "Plane"]
        changed, index, new = UILib.DrawDropdown("Shape", component.Type, shapes)
        if changed:
            entity.RemoveComponent(CollidorComponent)
            entity.AddComponent(CollidorComponent, index)

        if index == CollidorComponent.Shapes.Box:
            changed, new = UILib.DrawVector3Controls(
                "Scale", component.Collidor.Scale,
                resetValue=1, columnWidth=50
            )

            if changed: component.Collidor.SetScale(new)
    @staticmethod
    def __RigidBodyUIFunction(entity: Entity, component: RigidBodyComponent) -> None:
        changed, new = UILib.DrawBoolControls("Static", component.RigidBody.IsStatic, columnWidth=50)
        if changed:
            component.RigidBody.IsStatic = new
            if new: component.RigidBody.Mass = 0.0

        if not component.RigidBody.IsStatic:
            _, component.RigidBody.Mass = UILib.DrawFloatControls("Mass", component.RigidBody.Mass, columnWidth=50)
    # ----------------------------------------------------------------------

    def __DrawComponents(self, entity: Entity) -> None:
        if entity.HasComponent(TagComponent):
            tag = entity.GetComponent(TagComponent).Tag
            changed, entity.GetComponent(TagComponent).Tag = imgui.input_text("##Tag", tag, 256)

        imgui.same_line()
        imgui.push_item_width(-1)

        if imgui.button("Add Component"): imgui.open_popup("AddComponent")

        if imgui.begin_popup("AddComponent"):
            if imgui.menu_item("Camera")[0]:
                if not self.__SelectionContext.HasComponent(CameraComponent):
                    self.__SelectionContext.AddComponent(CameraComponent, SceneCamera(SceneCamera.ProjectionTypeEnum.Perspective))
                else:
                    PI_CLIENT_WARN("Entity already has a Camera Component")
                    DebugConsole.Warn("Entity already has a Camera Component")
                imgui.close_current_popup()

            # Meshes
            if imgui.begin_menu("Mesh"):
                if imgui.menu_item("Empty Mesh")[0]:
                    if not self.__SelectionContext.HasComponent(MeshComponent):
                        self.__SelectionContext.AddComponent(MeshComponent, ".")
                    else:
                        PI_CLIENT_WARN("Entity already has a Mesh Component")
                    imgui.close_current_popup()

                imgui.separator()
                if imgui.menu_item("Cube")[0]:
                    if not self.__SelectionContext.HasComponent(MeshComponent):
                        self.__SelectionContext.AddComponent(MeshComponent, ".\\InternalAssets\\Meshes\\Cube.obj")
                    else:
                        PI_CLIENT_WARN("Entity already has a Mesh Component")
                    imgui.close_current_popup()
                    
                if imgui.menu_item("Sphere")[0]:
                    if not self.__SelectionContext.HasComponent(MeshComponent):
                        self.__SelectionContext.AddComponent(MeshComponent, ".\\InternalAssets\\Meshes\\Sphere.obj")
                    else:
                        PI_CLIENT_WARN("Entity already has a Mesh Component")
                    imgui.close_current_popup()
                    
                if imgui.menu_item("Cyliender")[0]:
                    if not self.__SelectionContext.HasComponent(MeshComponent):
                        self.__SelectionContext.AddComponent(MeshComponent, ".\\InternalAssets\\Meshes\\Cylinder.obj")
                    else:
                        PI_CLIENT_WARN("Entity already has a Mesh Component")
                    imgui.close_current_popup()
                    
                if imgui.menu_item("Plane")[0]:
                    if not self.__SelectionContext.HasComponent(MeshComponent):
                        self.__SelectionContext.AddComponent(MeshComponent, ".\\InternalAssets\\Meshes\\Plane.obj")
                    else:
                        PI_CLIENT_WARN("Entity already has a Mesh Component")
                    imgui.close_current_popup()
                    
                if imgui.menu_item("Cone")[0]:
                    if not self.__SelectionContext.HasComponent(MeshComponent):
                        self.__SelectionContext.AddComponent(MeshComponent, ".\\InternalAssets\\Meshes\\Cone.obj")
                    else:
                        PI_CLIENT_WARN("Entity already has a Mesh Component")
                    imgui.close_current_popup()
                    
                if imgui.menu_item("Torus")[0]:
                    if not self.__SelectionContext.HasComponent(MeshComponent):
                        self.__SelectionContext.AddComponent(MeshComponent, ".\\InternalAssets\\Meshes\\Torus.obj")
                    else:
                        PI_CLIENT_WARN("Entity already has a Mesh Component")
                    imgui.close_current_popup()

                imgui.end_menu()

            if imgui.menu_item("Material")[0]:
                if not self.__SelectionContext.HasComponent(MaterialComponent):
                    self.__SelectionContext.AddComponent(MaterialComponent,
                        Material(Material.Type.Standard | Material.Type.Lit | Material.Type.Phong)
                    )
                else:
                    PI_CLIENT_WARN("Entity already has a Material Component")
                imgui.close_current_popup()

            if imgui.menu_item("Light")[0]:
                if not self.__SelectionContext.HasComponent(LightComponent):
                    self.__SelectionContext.AddComponent(LightComponent, LightComponent.TypeEnum.Point)
                else:
                    PI_CLIENT_WARN("Entity already has a Light Component")
                imgui.close_current_popup()

            if imgui.menu_item("Script")[0]:
                if not self.__SelectionContext.HasComponent(ScriptComponent):
                    self.__SelectionContext.AddComponent(ScriptComponent, "", "")
                else:
                    PI_CLIENT_WARN("Entity already has a Script Component")
                imgui.close_current_popup()

            if imgui.menu_item("Collidor")[0]:
                if not self.__SelectionContext.HasComponent(CollidorComponent):
                    collidor = self.__SelectionContext.AddComponent(CollidorComponent, CollidorComponent.Shapes.Box).Collidor
                    collidor.SetScale(entity.GetComponent(TransformComponent).Scale)
                else:
                    PI_CLIENT_WARN("Entity already has a Collidor Component")
                imgui.close_current_popup()

            if imgui.menu_item("RigidBody")[0]:
                collidor: Collider = None
                transform: TransformComponent = entity.GetComponent(TransformComponent)

                if not self.__SelectionContext.HasComponent(CollidorComponent):
                    collidor = self.__SelectionContext.AddComponent(CollidorComponent, CollidorComponent.Shapes.Box)
                else: collidor = entity.GetComponent(CollidorComponent)

                if not self.__SelectionContext.HasComponent(RigidBodyComponent):
                    material = PySicsMaterial(collider=collidor)
                    material.Position = transform.Translation
                    material.Rotation = transform.Rotation
                    self.__SelectionContext.AddComponent(RigidBodyComponent, material)
                else:
                    PI_CLIENT_WARN("Entity already has a RigidBody Component")
                imgui.close_current_popup()

            imgui.end_popup()

        imgui.pop_item_width()

        self.DrawComponent( "Transform" , entity , TransformComponent , SceneHierarchyPanel.__TransformUIFunction )
        self.DrawComponent( "Mesh"      , entity , MeshComponent      , SceneHierarchyPanel.__MeshUIFunction      )
        self.DrawComponent( "Material"  , entity , MaterialComponent  , SceneHierarchyPanel.__MaterialUIFunction  )
        self.DrawComponent( "Script"    , entity , ScriptComponent    , SceneHierarchyPanel.__ScriptUIFunction    )
        self.DrawComponent( "Light"     , entity , LightComponent     , SceneHierarchyPanel.__LightUIFunction     )
        self.DrawComponent( "Camera"    , entity , CameraComponent    , SceneHierarchyPanel.__CameraUIFunction    )
        self.DrawComponent( "Collidor"  , entity , CollidorComponent  , SceneHierarchyPanel.__CollidorUIFunction  )
        self.DrawComponent( "RigidBody" , entity , RigidBodyComponent , SceneHierarchyPanel.__RigidBodyUIFunction )

    def SetContext(self, scene: Scene) -> None: self.__Context = scene
    def SetSelectedEntity(self, entity: Entity) -> None: self.__SelectionContext = entity
    @property
    def SelectedEntity(self) -> Entity: return self.__SelectionContext
