import os
from typing import Tuple
from PI.ButtonCodes.KeyCodes import PI_KEY_ENTER
from PI.Core.Input import Input
from PI.Scene import *
from PI.Logging import PI_CLIENT_WARN
import imgui

class SceneHierarchyPanel:
    __Context: Scene
    __SelectionContext: Entity

    def __init__(self) -> None:
        self.__Context = Scene()
        self.__SelectionContext = None

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
    def DrawVector3Controls(lable: str, values: pyrr.Vector3, resetValue: float=0, columnWidth: float=100) -> Tuple[bool, pyrr.Vector3]:
        imgui.push_id(lable)

        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()

        imgui.push_item_width(imgui.calculate_item_width()/3)
        imgui.push_item_width(imgui.calculate_item_width()/2.5*2)
        imgui.push_item_width(imgui.calculate_item_width())

        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, imgui.Vec2( 0, 2 ))
        lineHeight = 23.5

        imgui.push_style_color(imgui.COLOR_BUTTON, 0.8, 0.1, 0.15, 1.0 )
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.9, 0.2, 0.2, 1.0 )
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.8, 0.1, 0.15, 1.0 )
        if imgui.button("X", lineHeight + 3.0, lineHeight): values.x = resetValue
        imgui.pop_style_color(3)

        imgui.same_line()
        XHasChanged, XChanged = imgui.drag_float("##X", values.x, 0.1, 0.0, 0.0, format="%.2f")
        imgui.pop_item_width()
        imgui.same_line()

        imgui.push_style_color(imgui.COLOR_BUTTON, 0.2, 0.7, 0.2, 1.0 )
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.3, 0.8, 0.3, 1.0 )
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.2, 0.7, 0.2, 1.0 )
        if imgui.button("Y", lineHeight + 3.0, lineHeight): values.y = resetValue
        imgui.pop_style_color(3)

        imgui.same_line()
        YHasChanged, YChanged = imgui.drag_float("##Y", values.y, 0.1, 0.0, 0.0, format="%.2f")
        imgui.pop_item_width()
        imgui.same_line()

        imgui.push_style_color(imgui.COLOR_BUTTON, 0.1, 0.25, 0.8, 1.0 )
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.2, 0.35, 0.9, 1.0 )
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.1, 0.25, 0.8, 1.0 )
        if imgui.button("Z", lineHeight + 3.0, lineHeight): values.z = resetValue
        imgui.pop_style_color(3)

        imgui.same_line()
        ZHasChanged, ZChanged = imgui.drag_float("##Z", values.z, 0.1, 0.0, 0.0, format="%.2f")
        imgui.pop_item_width()

        imgui.pop_style_var()
        imgui.columns(1)
        imgui.pop_id()

        if XHasChanged or YHasChanged or ZHasChanged: return True, pyrr.Vector3([ XChanged, YChanged, ZChanged ])
        else: return False, pyrr.Vector3([ values.x, values.y, values.z ])

    @staticmethod
    def DrawTextFieldControls(lable: str, value: str, columnWidth: float=50) -> Tuple[bool, str]:
        imgui.push_id(lable)

        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()
        
        imgui.push_item_width(imgui.calculate_item_width())
        changed, newPath = imgui.input_text("##Filter", value, 512)
        imgui.pop_item_width()

        imgui.columns(1)
        imgui.pop_id()

        return changed, newPath


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
                UIfunction(component)
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

            imgui.end_popup()

        imgui.pop_item_width()

        def _TransformUIFunction(component: TransformComponent) -> None:
            component.SetTranslation ( SceneHierarchyPanel.DrawVector3Controls( "Translation" , component.Translation ) [1] )
            component.SetRotation    ( SceneHierarchyPanel.DrawVector3Controls( "Rotation"    , component.Rotation    ) [1] )
            component.SetScale       ( SceneHierarchyPanel.DrawVector3Controls( "Scale"       , component.Scale, 1    ) [1] )

        def _MeshUIFunction(component: MeshComponent) -> None:
            changed, path = SceneHierarchyPanel.DrawTextFieldControls("Filter", component.Path)

            if changed: component.Path = path
            
            if Input.IsKeyPressed(PI_KEY_ENTER) and component.Path is not component.MeshObject.Path:
                if not os.path.exists(component.Path):
                    PI_CLIENT_WARN("Trying to load invalid Modle")
                    component.Path = component.MeshObject.Path
                    return

                component.MeshObject = Mesh.Load(component.Path)[0]
                component.Name = component.MeshObject.Name

        SceneHierarchyPanel.DrawComponent( "Transform", entity , TransformComponent , _TransformUIFunction )
        SceneHierarchyPanel.DrawComponent( "Mesh"     , entity , MeshComponent      , _MeshUIFunction      )

    def SetContext(self, scene: Scene) -> None: self.__Context = scene
    def SetSelectedEntity(self, entity: Entity) -> None: self.__SelectionContext = entity
    @property
    def SelectedEntity(self) -> Entity: return self.__SelectionContext
