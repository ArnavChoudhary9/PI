from PI import *

import os
from typing import List
import imgui

_ScriptFiles: List[str] = []
def _SearchForScripts(basePath: str=".\\Scripts", filter: str=".py", currentPath: list=[]) -> None:
    global _ScriptFiles
    currentPath.append(basePath)

    dir: list
    try: dir = os.listdir(basePath)
    except NotADirectoryError:
        if basePath.endswith(filter): _ScriptFiles.append(basePath)
        return

    for subDir in dir: _SearchForScripts(basePath + "/" + subDir, filter, currentPath)

    currentPath.pop()

def _ProcessScriptFiles(basePath: str, search: bool=False) -> List[str]:
    global _ScriptFiles
    
    if search:
        _ScriptFiles = ["."]
        _SearchForScripts(basePath)
    
    _scripts = []

    for script in _ScriptFiles:
        _scripts.append(script.replace("/", "\\"))
    
    if search: _ScriptFiles = _scripts
    return _scripts

class SceneHierarchyPanel:
    __Context: Scene
    __SelectionContext: Entity

    def __init__(self) -> None:
        self.__Context = Scene()
        self.__SelectionContext = None

        _ProcessScriptFiles(".\\Assets", True)

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

    def __DrawEntityNode(self, entity: Entity) -> None:
        tag = entity.GetComponent(TagComponent)

        flags = 0
        if self.__SelectionContext is entity: flags = imgui.TREE_NODE_SELECTED
        flags |= imgui.TREE_NODE_OPEN_ON_ARROW | imgui.TREE_NODE_SPAN_AVAILABLE_WIDTH

        # Adding this to make each entity unique
        # NOTE: int(entity) retrives its __EntityHandle
        opened = imgui.tree_node(str(tag) + f"##{int(entity)}", flags=flags)
        if imgui.is_item_clicked(): self.__SelectionContext = entity

        entityDelete = False
        if imgui.begin_popup_context_item():
            if imgui.menu_item("Delete Entity")[0]: entityDelete = True
            imgui.end_popup()

        if opened: imgui.tree_pop()

        if entityDelete:
            self.__Context.DestroyEntity(entity)
            if self.__SelectionContext is entity: self.__SelectionContext = None

    @staticmethod
    def DrawComponent(name: str, entity: Entity, componentType: CTV, UIfunction) -> None:
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
                imgui.end_popup()

            if isOpen:
                UIfunction(entity, component)
                imgui.tree_pop()

            if removeComponent: entity.RemoveComponent(componentType)

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
                    self.__SelectionContext.AddComponent(CameraComponent)
                else: PI_CLIENT_WARN("Entity already has a Camera Component")
                imgui.close_current_popup()

            # Meshes
            imgui.separator()
            if imgui.menu_item("Mesh")[0]:
                if not self.__SelectionContext.HasComponent(MeshComponent):
                    self.__SelectionContext.AddComponent(MeshComponent, "")
                else: PI_CLIENT_WARN("Entity already has a Mesh Component")
                imgui.close_current_popup()

            if imgui.menu_item("Cube")[0]:
                if not self.__SelectionContext.HasComponent(MeshComponent):
                    self.__SelectionContext.AddComponent(MeshComponent, ".\\Assets\\Internal\\Meshes\\Cube.obj")
                else: PI_CLIENT_WARN("Entity already has a Mesh Component")
                imgui.close_current_popup()
                
            if imgui.menu_item("Sphere")[0]:
                if not self.__SelectionContext.HasComponent(MeshComponent):
                    self.__SelectionContext.AddComponent(MeshComponent, ".\\Assets\\Internal\\Meshes\\Sphere.obj")
                else: PI_CLIENT_WARN("Entity already has a Mesh Component")
                imgui.close_current_popup()
                
            if imgui.menu_item("Cyliender")[0]:
                if not self.__SelectionContext.HasComponent(MeshComponent):
                    self.__SelectionContext.AddComponent(MeshComponent, ".\\Assets\\Internal\\Meshes\\Cylinder.obj")
                else: PI_CLIENT_WARN("Entity already has a Mesh Component")
                imgui.close_current_popup()
                
            if imgui.menu_item("Cone")[0]:
                if not self.__SelectionContext.HasComponent(MeshComponent):
                    self.__SelectionContext.AddComponent(MeshComponent, ".\\Assets\\Internal\\Meshes\\Cone.obj")
                else: PI_CLIENT_WARN("Entity already has a Mesh Component")
                imgui.close_current_popup()
                
            if imgui.menu_item("Torus")[0]:
                if not self.__SelectionContext.HasComponent(MeshComponent):
                    self.__SelectionContext.AddComponent(MeshComponent, ".\\Assets\\Internal\\Meshes\\Torus.obj")
                else: PI_CLIENT_WARN("Entity already has a Mesh Component")
                imgui.close_current_popup()

            imgui.separator()
            if imgui.menu_item("Script")[0]:
                if not self.__SelectionContext.HasComponent(ScriptComponent):
                    self.__SelectionContext.AddComponent(ScriptComponent, ".")
                else: PI_CLIENT_WARN("Entity already has a Script Component")
                imgui.close_current_popup()

            imgui.end_popup()

        imgui.pop_item_width()

        def _TransformUIFunction(entity: Entity, component: TransformComponent) -> None:
            component.SetTranslation ( UILib.DrawVector3Controls( "Translation" , component.Translation      ) [1] )
            component.SetRotation    ( UILib.DrawVector3Controls( "Rotation"    , component.Rotation, 0, 0.5 ) [1] )
            component.SetScale       ( UILib.DrawVector3Controls( "Scale"       , component.Scale, 1         ) [1] )

        def _MeshUIFunction(entity: Entity, component: MeshComponent) -> None:
            changed, path = UILib.DrawTextFieldControls("Filter", component.Path)

            if changed: component.Path = path
            
            if Input.IsKeyPressed(PI_KEY_ENTER) and component.Path is not component.MeshObject.Path:
                if not os.path.exists(component.Path):
                    PI_CLIENT_WARN("Trying to load invalid Modle")
                    component.Path = component.MeshObject.Path
                    return

                entity.RemoveComponent(MeshComponent)
                entity.AddComponent(MeshComponent, component.Path).Init()

        def _ScriptUIFunction(entity: Entity, component: ScriptComponent) -> None:
            scripts = _ProcessScriptFiles(".\\Assets")
            
            if component.Bound:
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
                    
                    if variableChanged: setattr(component.Script, name, new)
                if len(component.Variables) != 0: imgui.text("")

            changed, index, path = UILib.DrawDropdown("Script", scripts.index(component.Path), scripts)

            if changed:
                _ProcessScriptFiles(".\\Assets", True)
                entity.RemoveComponent(ScriptComponent)
                entity.AddComponent(ScriptComponent, path)

        def _LightUIFunction(entity: Entity, component: LightComponent) -> None:
            lightTypes = ["Directional", "Point", "Spot"]
            changed, lightType, lightTypeStr = UILib.DrawDropdown("Light Type", component.LightType, lightTypes, columnWidth=100)

            changed, new = UILib.DrawFloatControls("Intensity", component.Light.Intensity, minValue=0.01, maxValue=1000)
            if changed: component.Light.SetIntensity(new)
            
            imgui.separator()
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

        def _CameraUIFunction(entity: Entity, component: CameraComponent) -> None:
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

        SceneHierarchyPanel.DrawComponent( "Transform" , entity , TransformComponent , _TransformUIFunction )
        SceneHierarchyPanel.DrawComponent( "Mesh"      , entity , MeshComponent      , _MeshUIFunction      )
        SceneHierarchyPanel.DrawComponent( "Script"    , entity , ScriptComponent    , _ScriptUIFunction    )
        SceneHierarchyPanel.DrawComponent( "Light"     , entity , LightComponent     , _LightUIFunction     )
        SceneHierarchyPanel.DrawComponent( "Camera"    , entity , CameraComponent    , _CameraUIFunction    )

    def SetContext(self, scene: Scene) -> None: self.__Context = scene
    def SetSelectedEntity(self, entity: Entity) -> None: self.__SelectionContext = entity
    @property
    def SelectedEntity(self) -> Entity: return self.__SelectionContext
