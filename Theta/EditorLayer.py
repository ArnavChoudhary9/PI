from PI import *
from Panels.SceneHierarchyPanel import *
from Panels.ContentBrowserPanel import *

import json

INSTRUCTION_TEXT: str = \
"""Welcome to Theta: The PI Editor
Current version: {0}
Current Configuration: {1}

Content Browser:
-> Drag and drop scenes from ContentBrowser (./Scenes/*) to Viewport to load the scene.

-> Click on any object to select it.
-> Its properties will show up in the Properties panel.

-> You can also drag and drop meshes from ContentBrowser into Filter section in Mesh Component.

Editor Camera:
Use ALT to acitvate Camera movement.
Then, you can use:
Right mouse button -> Zoom,
Left mouse button -> Rotate,
Middle mouse -> Pan

Theme Editor:
-> You can open Theme Editor from Edit tab.""" \
    .format(PI_VERSION, PI_CONFIG)

class EditorLayer(Layer):
    __ActiveScene : Scene
    __EditorScene : Scene

    __SceneHierarchyPanel: SceneHierarchyPanel
    __ContentBrowserPanel: ContentBrowserPanel

    __EditorCamera: EditorCamera

    __Framebuffer: Framebuffer
    __ViewportSize: ImVec2

    __ViewportBounds : List[ImVec2]
    __HoveredEntity  : Entity = 0

    __ThemePreset: str
    __CurrentTheme: ImGuiTheme
    __CurrentThemeActive: ImGuiTheme

    __ViewportFocused : bool
    __ViewportHovered : bool

    __Panels: List = []

    class SceneStateEnum:
        Edit: int = 0
        Play: int = 1

    __SceneState: int
    __PlayIcon: Texture2D
    __StopIcon: Texture2D

    __Framerate: float
    __ShowDebugStats: bool
    __ShowThemeEditor: bool
    vSync = PI_V_SYNC

    def __init__(self, name: str = "EditorLayer") -> None:
        super().__init__(name=name)
        self.__ViewportSize = ImVec2( 0, 0 )
        self.__ViewportBounds = [ ImVec2( 0, 0 ) , ImVec2( 0, 0 ) ]
        self.__EditorCamera = EditorCamera(45, 1.778, 0.1, 1000)

    def OnAttach(self) -> None:
        timer = PI_TIMER("EditorLayer::OnAttach")

        self.__EditorScene = Scene()
        self.__ActiveScene = self.__EditorScene

        self.__SceneHierarchyPanel = SceneHierarchyPanel()
        self.__SceneHierarchyPanel.SetContext(self.__ActiveScene)

        self.__ContentBrowserPanel = ContentBrowserPanel()

        specs = Framebuffer.Specs()
        specs.Width = 1280
        specs.Height = 720
        specs.Attachments = Framebuffer.AttachmentSpecification(
            Framebuffer.TextureSpecification(Framebuffer.TextureSpecification(Framebuffer.TextureFormat.RGBA8)),
            Framebuffer.TextureSpecification(Framebuffer.TextureSpecification(Framebuffer.TextureFormat.RED_INTEGER)),
            Framebuffer.TextureSpecification(Framebuffer.TextureSpecification(Framebuffer.TextureFormat.DEPTH))
        )
        self.__Framebuffer: Framebuffer = Framebuffer.Create(specs)
        self.__Framebuffer.Unbind()

        self.__Framerate   = 60
        self.__ShowDebugStats = False
        self.__ShowThemeEditor = False

        _filename = f"{Cache.GetLocalSaveDirectory()}\\ThemePref.json"
        if os.path.exists(_filename):
            with open(_filename, 'r') as f: self.__ThemePreset = json.load(f)["Pref"]
        else: self.__ThemePreset = "Default Dark"

        if self.__ThemePreset == "Default Dark":
            self.__CurrentTheme: ImGuiTheme = ImGuiTheme.DefaultDark.Copy()
            self.__CurrentThemeActive: ImGuiTheme = ImGuiTheme.DefaultActive.Copy()
        
        elif self.__ThemePreset == "Default Light":
            self.__CurrentTheme: ImGuiTheme = ImGuiTheme.DefaultLight.Copy()
            self.__CurrentThemeActive: ImGuiTheme = ImGuiTheme.LightActive.Copy()
        
        elif self.__ThemePreset == "Ruth":
            self.__CurrentTheme: ImGuiTheme = ImGuiTheme.Ruth.Copy()
            self.__CurrentThemeActive: ImGuiTheme = ImGuiTheme.DefaultDark.Copy()
        
        elif self.__ThemePreset == "Custom":
            self.__CurrentTheme = ImGuiTheme()
            self.__CurrentThemeActive = ImGuiTheme()
            
            with open(f"{Cache.GetLocalSaveDirectory()}\\Theme.json", 'r') as f:
                for field, value in json.load(f).items():
                    self.__CurrentTheme.AddFields( { int(field) : ImVec4( value[0], value[1], value[2], value[3] ) } )
            with open(f"{Cache.GetLocalSaveDirectory()}\\ThemeActive.json", 'r') as f:
                for field, value in json.load(f).items():
                    self.__CurrentThemeActive.AddFields( { int(field) : ImVec4( value[0], value[1], value[2], value[3] ) } )

        ImGuiLayer.SetTheme(self.__CurrentTheme)

        self.__ViewportFocused : bool = True
        self.__ViewportHovered : bool = True

        self.__Panels.append(self.__SceneHierarchyPanel)
        self.__Panels.append(self.__ContentBrowserPanel)

        self.__SceneState = EditorLayer.SceneStateEnum.Edit

        try:
            self.__PlayIcon = Texture2D.Create( ".\\Theta\\Resources\\Icons\\PlayButton.png" )
            self.__StopIcon = Texture2D.Create( ".\\Theta\\Resources\\Icons\\StopButton.png" )

        # This is here for Building
        # 'cause the Build looks for files in '.'
        except FileNotFoundError:
            self.__PlayIcon = Texture2D.Create( ".\\Resources\\Icons\\PlayButton.png" )
            self.__StopIcon = Texture2D.Create( ".\\Resources\\Icons\\StopButton.png" )

    def __NewScene(self) -> None:
        self.__OnScenePause()
        
        newScene = Scene()
        newScene.OnViewportResize(self.__ActiveScene._ViewportWidth, self.__ActiveScene._ViewportHeight)
        self.__EditorScene = newScene
        self.__ActiveScene = self.__EditorScene
        self.__SceneHierarchyPanel.SetContext(self.__EditorScene)

    def __SaveScene(self, dialogbox: bool=False) -> None:
        self.__OnScenePause()
        
        if self.__ActiveScene._Filepath != None and not dialogbox:
            fileName = self.__ActiveScene._Filepath
            if not fileName.lower().endswith(".pi"): fileName += ".PI"
            Scene.Serialize(self.__ActiveScene, fileName)
            return
        
        elif self.__ActiveScene._Filepath == None and not dialogbox:
            PI_CORE_WARN("The scene should be saved first.")
            return

        if not dialogbox: return
        cancelled, fileName = UILib.DrawFileSaveDialog( ( ("PI scene file (*.PI)", ".PI"), ) )
        if not cancelled:
            if not fileName.lower().endswith(".pi"): fileName += ".PI"
            Scene.Serialize(self.__ActiveScene, fileName)

    def __LoadScene(self, filename: str=None) -> None:
        self.__OnScenePause()

        cancelled = False
        if not filename  : cancelled, filename = UILib.DrawFileLoadDialog( ( ("PI scene file (*.PI)", ".PI"), ) )
        if not cancelled : self.__EditorScene = Scene.Deserialize(self.__EditorScene, filename)
        self.__ActiveScene = self.__EditorScene
        self.__SceneHierarchyPanel.SetContext(self.__EditorScene)

    def OnEvent(self, event: Event) -> None:
        self.__EditorCamera.OnEvent(event)

        def CheckKeys(event: KeyPressedEvent) -> bool:
            control = Input.IsKeyPressed(PI_KEY_LEFT_CONTROL) or Input.IsKeyPressed(PI_KEY_RIGHT_CONTROL)
            shift   = Input.IsKeyPressed(PI_KEY_LEFT_SHIFT)   or Input.IsKeyPressed(PI_KEY_RIGHT_SHIFT)

            if event.KeyCode == PI_KEY_Q and control:
                StateManager.GetCurrentApplication().Close()
                return True

            if event.KeyCode == PI_KEY_N and control:
                self.__NewScene()
                return True

            if event.KeyCode == PI_KEY_S and control and not shift:
                self.__SaveScene()
                return True

            if event.KeyCode == PI_KEY_S and control and shift:
                self.__SaveScene(dialogbox=True)
                return True

            if event.KeyCode == PI_KEY_O and control:
                self.__LoadScene()
                return True

            if event.KeyCode == PI_KEY_F5 and not control and not shift:
                if self.__SceneState == EditorLayer.SceneStateEnum.Edit:
                    self.__OnScenePlay()
                else:
                    self.__OnScenePause()

        def MouseButtonClick(event: MouseButtonPressedEvent) -> bool:
            if event.ButtonCode == PI_MOUSE_BUTTON_LEFT:
                if self.__ViewportHovered and not Input.IsKeyPressed(PI_KEY_LEFT_ALT):
                    self.__SceneHierarchyPanel.SetSelectedEntity(self.__HoveredEntity)

        dispatcher = EventDispatcher(event)
        dispatcher.Dispach(CheckKeys, EventType.KeyPressed)
        dispatcher.Dispach(MouseButtonClick, EventType.MouseButtonPressed)

    def OnImGuiRender(self) -> None:
        ImGuiTimer = PI_TIMER("EditorLayer::OnImGuiRender")
    
        optFullscreen = True
        dockspaceFlage = imgui.DOCKNODE_NONE

        windowFlags = imgui.WINDOW_MENU_BAR | imgui.WINDOW_NO_DOCKING
        if optFullscreen:
            viewport = imgui.get_main_viewport()
            imgui.set_next_window_position(*viewport.pos)
            imgui.set_next_window_size(*viewport.size)

            imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0.0)
            imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0.0)

            windowFlags |= imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE | \
                imgui.WINDOW_NO_MOVE
            windowFlags |= imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_NO_NAV_FOCUS

        if dockspaceFlage & imgui.DOCKNODE_PASSTHRU_CENTRAL_NODE:
            windowFlags |= imgui.WINDOW_NO_BACKGROUND

        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, ImVec2(0.0, 0.0))
        with imgui.begin("DockSpace", True, windowFlags):
            imgui.pop_style_var()

            if optFullscreen:
                imgui.pop_style_var(2)

            io = imgui.get_io()
            if io.config_flags & imgui.CONFIG_DOCKING_ENABLE:
                dockspaceID = imgui.get_id("DockSpace")
                imgui.dockspace(dockspaceID, (0.0, 0.0), dockspaceFlage)

            with imgui.begin_menu_bar():
                if imgui.begin_menu("File"):
                    if imgui.menu_item("New", "Ctrl+N", False, True)[0]: self.__NewScene()
                    if imgui.menu_item("Save", "Ctrl+S", False, True)[0]: self.__SaveScene()
                    if imgui.menu_item("Save As", "Ctrl+Shift+S", False, True)[0]: self.__SaveScene(dialogbox=True)
                    if imgui.menu_item("Open", "Ctrl+O", False, True)[0]: self.__LoadScene()                        
                    if imgui.menu_item("Quit", "Ctrl+Q", False, True)[0]: StateManager.GetCurrentApplication().Close()
                    
                    imgui.end_menu()

                if imgui.begin_menu("Edit"):
                    if imgui.menu_item("Theme Editor")[0]: self.__ShowThemeEditor = True

                    if not self.__ShowDebugStats:
                        if imgui.menu_item("Open Debug Stats")[0]: self.__ShowDebugStats = True
                    else:
                        if imgui.menu_item("Close Debug Stats")[0]: self.__ShowDebugStats = False

                    imgui.end_menu()

            for panel in self.__Panels: panel.OnImGuiRender()

            if self.__ShowDebugStats:   
                with imgui.begin("DEBUG Settings"):
                    clicked, self.vSync = imgui.checkbox("VSync", self.vSync)

                    if clicked:
                        StateManager.GetCurrentWindow().SetVSync(self.vSync)

                        global PI_V_SYNC
                        PI_V_SYNC = self.vSync

                    imgui.text("FPS: {}".format(round(self.__Framerate)))
                    imgui.text("Hovered Entity: {}".format(int(self.__HoveredEntity) if self.__HoveredEntity else 0))

                    imgui.text("\nRenderer Stats:")
                    imgui.separator()
                    imgui.text("Draw Calls: {}".format(StateManager.Stats.DrawCalls))
                    
                    flags = imgui.TREE_NODE_OPEN_ON_ARROW | imgui.TREE_NODE_SPAN_AVAILABLE_WIDTH
                    if imgui.tree_node("Shaders (Binded {} times)".format(StateManager.Stats.Shaders.ShadersBinded),
                        flags=flags):
                        
                        imgui.text("Uniforms:")
                        imgui.text("\tTotal Uniforms Uploaded : {}" \
                            .format(StateManager.Stats.Shaders.Uniforms.TotalUniforms))

                        imgui.text("")
                        imgui.text("\tTotal Ints Uploaded : {}" \
                            .format(StateManager.Stats.Shaders.Uniforms.Ints))

                        imgui.text("\tTotal Floats Uploaded : {}" \
                            .format(StateManager.Stats.Shaders.Uniforms.Floats))

                        imgui.text("")
                        imgui.text("\tTotal Vector3's Uploaded : {}" \
                            .format(StateManager.Stats.Shaders.Uniforms.Vector3))

                        imgui.text("\tTotal Vector4's Uploaded : {}" \
                            .format(StateManager.Stats.Shaders.Uniforms.Vector4))

                        imgui.text("")
                        imgui.text("\tTotal Matrix 3x3 Uploaded : {}" \
                            .format(StateManager.Stats.Shaders.Uniforms.Matrix_3x3))

                        imgui.text("\tTotal Matrix 4x4 Uploaded : {}" \
                            .format(StateManager.Stats.Shaders.Uniforms.Matrix_4x4))

                        imgui.tree_pop()

            if self.__ShowThemeEditor: self.ThemeEditor()

            imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, ImVec2( 0, 0 ))
            with imgui.begin("Viewport"):
                viewportMinRegion = imgui.get_window_content_region_min()
                viewportMaxRegion = imgui.get_window_content_region_max()
                viewportOffset    = imgui.get_window_position()

                self.__ViewportBounds[0] = ImVec2(
                    viewportMinRegion[0] + viewportOffset[0],
                    viewportMinRegion[1] + viewportOffset[1]
                )
                self.__ViewportBounds[1] = ImVec2(
                    viewportMaxRegion[0] + viewportOffset[0],
                    viewportMaxRegion[1] + viewportOffset[1]
                )

                viewportPanelSize = imgui.get_content_region_available()
                self.__ViewportSize = viewportPanelSize

                self.__ViewportFocused = imgui.is_window_focused()
                self.__ViewportHovered = imgui.is_window_hovered()
                
                app: PI_Application = StateManager.GetCurrentApplication()
                app.ImGuiLayer.BlockEvents(not self.__ViewportFocused and not self.__ViewportHovered)

                imgui.image(
                    self.__Framebuffer.GetColorAttachment(0),
                    self.__ViewportSize.x, self.__ViewportSize.y,
                    ( 0, 1 ), ( 1, 0 )
                )

                if imgui.begin_drag_drop_target():
                    data: bytes = imgui.accept_drag_drop_payload("CONTENT_BROWSER_ITEM")
                    if data:
                        data = data.decode('UTF-8')
                        if not data.lower().endswith('.pi'): PI_CLIENT_WARN("File: {} is not a scene file", data)
                        else: self.__LoadScene(data)
                    imgui.end_drag_drop_target()

            imgui.pop_style_var()

            with imgui.begin("Instructions", flags=imgui.WINDOW_NO_FOCUS_ON_APPEARING):
                imgui.text_wrapped(INSTRUCTION_TEXT)
            
            self.UI_Toolbar()

    def __OnScenePlay(self) -> None:
        self.__SceneState = EditorLayer.SceneStateEnum.Play
        self.__ActiveScene = Scene.Copy(self.__EditorScene)
        self.__SceneHierarchyPanel.SetContext(self.__ActiveScene)
        self.__SceneHierarchyPanel.SetSelectedEntity(None)

        ImGuiLayer.SetTheme(self.__CurrentThemeActive)

    def __OnScenePause(self) -> None:
        self.__SceneState = EditorLayer.SceneStateEnum.Edit
        self.__ActiveScene = self.__EditorScene
        self.__SceneHierarchyPanel.SetContext(self.__EditorScene)
        self.__SceneHierarchyPanel.SetSelectedEntity(None)

        ImGuiLayer.SetTheme(self.__CurrentTheme)

    def ThemeEditor(self) -> None:
        with imgui.begin("Themes"):
            columnWidth = 150

            presets = [ "Default Dark", "Default Light", "Ruth", "Custom" ]
            changed, _, preset = UILib.DrawDropdown("Preset", presets.index(self.__ThemePreset), presets)
            self.__ThemePreset = preset

            if preset == "Custom":
                imgui.text("")
                imgui.separator()

                changed, newColor = UILib.DrawColor3Controls(
                    "Window Background", self.__CurrentTheme.Fields[imgui.COLOR_WINDOW_BACKGROUND], columnWidth
                )
                if changed:
                    self.__CurrentTheme.AddFields({
                        imgui.COLOR_WINDOW_BACKGROUND : ImVec4( *newColor, 1.0 ),
                        imgui.COLOR_CHILD_BACKGROUND  : ImVec4( 0.0, 0.0, 0.0, 0.0 ),

                        imgui.COLOR_TITLE_BACKGROUND : ImVec4( newColor[0] * 0.9, newColor[1] * 0.9, newColor[2] * 0.9, 1.0 ),
                        imgui.COLOR_TITLE_BACKGROUND_COLLAPSED : ImVec4( 1., 1.0, 1.0, 0.51 ),
                        imgui.COLOR_TITLE_BACKGROUND_ACTIVE
                            : ImVec4( newColor[0] * 0.8, newColor[1] * 0.8, newColor[2] * 0.8, 1.0 ),

                        imgui.COLOR_MENUBAR_BACKGROUND
                            : ImVec4( newColor[0] * 0.7, newColor[1] * 0.7, newColor[2] * 0.7, 1.0 ),
                    })

                changed, newColor = UILib.DrawColor3Controls(
                    "Text", self.__CurrentTheme.Fields[imgui.COLOR_TEXT], columnWidth
                )
                if changed:
                    h, s, v = imgui.color_convert_rgb_to_hsv(newColor[0], newColor[1], newColor[2])
                    v = (v * 0.6) if v > 0.5 else (v * 1.6)
                    rd, gd, bd = imgui.color_convert_hsv_to_rgb(h, s, v)

                    self.__CurrentTheme.AddFields({
                        imgui.COLOR_TEXT : ImVec4( *newColor, 1.0 ),
                        imgui.COLOR_TEXT_DISABLED : ImVec4( rd, gd, bd, 1.0 )
                    })

                changed, newColor = UILib.DrawColor3Controls(
                    "Input Background", self.__CurrentTheme.Fields[imgui.COLOR_FRAME_BACKGROUND], columnWidth
                )
                if changed:
                    h, s, v = imgui.color_convert_rgb_to_hsv(newColor[0], newColor[1], newColor[2])
                    v = (v * 0.45) if v > 0.5 else (v * 1.45)
                    rd, gd, bd = imgui.color_convert_hsv_to_rgb(h, s, v)

                    self.__CurrentTheme.AddFields({
                        imgui.COLOR_FRAME_BACKGROUND         : ImVec4( *newColor, 1.0 ),
                        imgui.COLOR_FRAME_BACKGROUND_HOVERED : ImVec4( rd, gd, bd, 1.0 ),
                        imgui.COLOR_FRAME_BACKGROUND_ACTIVE  : ImVec4( rd, gd, bd, 1.0 ),
                    })

                changed, newColor = UILib.DrawColor3Controls(
                    "Tabs", self.__CurrentTheme.Fields[imgui.COLOR_TAB], columnWidth
                )
                if changed:
                    h, s, v = imgui.color_convert_rgb_to_hsv(newColor[0], newColor[1], newColor[2])
                    v = v if v > 0.8 else (v * 1.25)
                    r, g, b = imgui.color_convert_hsv_to_rgb(h, s, v)

                    self.__CurrentTheme.AddFields({
                        imgui.COLOR_TAB         : ImVec4( *newColor, 1.0 ),
                        imgui.COLOR_TAB_HOVERED : ImVec4( r, g, b, 1.0 ),
                        imgui.COLOR_TAB_ACTIVE  : ImVec4( *newColor, 1.0 ),

                        imgui.COLOR_TAB_UNFOCUSED         : ImVec4( r, g, b, 1.0 ),
                        imgui.COLOR_TAB_UNFOCUSED_ACTIVE  : ImVec4( *newColor, 1.0 )
                    })

                changed, newColor = UILib.DrawColor3Controls(
                    "Buttons", self.__CurrentTheme.Fields[imgui.COLOR_BUTTON], columnWidth
                )
                if changed:
                    h, s, v = imgui.color_convert_rgb_to_hsv(newColor[0], newColor[1], newColor[2])
                    v = (v * 0.25) if v > 0.8 else (v * 1.1)
                    r, g, b = imgui.color_convert_hsv_to_rgb(h, s, v)

                    self.__CurrentTheme.AddFields({
                        imgui.COLOR_BUTTON         : ImVec4( *newColor, 0.40 ),
                        imgui.COLOR_BUTTON_HOVERED : ImVec4( *newColor, 1.00 ),
                        imgui.COLOR_BUTTON_ACTIVE  : ImVec4( r, g, b, 1.00 ),
                    })

                imgui.text("")

                imgui.push_id("WhilePlaying")
                imgui.text("While Playing")
                imgui.separator()

                changed, newColor = UILib.DrawColor3Controls(
                    "Window Background", self.__CurrentThemeActive.Fields[imgui.COLOR_WINDOW_BACKGROUND], columnWidth
                )
                if changed:
                    self.__CurrentThemeActive.AddFields({
                        imgui.COLOR_WINDOW_BACKGROUND : ImVec4( *newColor, 1.0 ),
                        imgui.COLOR_CHILD_BACKGROUND  : ImVec4( 0.0, 0.0, 0.0, 0.0 ),

                        imgui.COLOR_TITLE_BACKGROUND : ImVec4( newColor[0] * 0.9, newColor[1] * 0.9, newColor[2] * 0.9, 1.0 ),
                        imgui.COLOR_TITLE_BACKGROUND_COLLAPSED : ImVec4( 1., 1.0, 1.0, 0.51 ),
                        imgui.COLOR_TITLE_BACKGROUND_ACTIVE
                            : ImVec4( newColor[0] * 0.8, newColor[1] * 0.8, newColor[2] * 0.8, 1.0 ),

                        imgui.COLOR_MENUBAR_BACKGROUND
                            : ImVec4( newColor[0] * 0.7, newColor[1] * 0.7, newColor[2] * 0.7, 1.0 ),
                    })

                changed, newColor = UILib.DrawColor3Controls(
                    "Text", self.__CurrentThemeActive.Fields[imgui.COLOR_TEXT], columnWidth
                )
                if changed:
                    h, s, v = imgui.color_convert_rgb_to_hsv(newColor[0], newColor[1], newColor[2])
                    v = (v * 0.6) if v > 0.5 else (v * 1.6)
                    rd, gd, bd = imgui.color_convert_hsv_to_rgb(h, s, v)

                    self.__CurrentThemeActive.AddFields({
                        imgui.COLOR_TEXT : ImVec4( *newColor, 1.0 ),
                        imgui.COLOR_TEXT_DISABLED : ImVec4( rd, gd, bd, 1.0 )
                    })

                changed, newColor = UILib.DrawColor3Controls(
                    "Input Background", self.__CurrentThemeActive.Fields[imgui.COLOR_FRAME_BACKGROUND], columnWidth
                )
                if changed:
                    h, s, v = imgui.color_convert_rgb_to_hsv(newColor[0], newColor[1], newColor[2])
                    v = (v * 0.45) if v > 0.5 else (v * 1.45)
                    rd, gd, bd = imgui.color_convert_hsv_to_rgb(h, s, v)

                    self.__CurrentThemeActive.AddFields({
                        imgui.COLOR_FRAME_BACKGROUND         : ImVec4( *newColor, 1.0 ),
                        imgui.COLOR_FRAME_BACKGROUND_HOVERED : ImVec4( rd, gd, bd, 1.0 ),
                        imgui.COLOR_FRAME_BACKGROUND_ACTIVE  : ImVec4( rd, gd, bd, 1.0 ),
                    })

                changed, newColor = UILib.DrawColor3Controls(
                    "Tabs", self.__CurrentThemeActive.Fields[imgui.COLOR_TAB], columnWidth
                )
                if changed:
                    h, s, v = imgui.color_convert_rgb_to_hsv(newColor[0], newColor[1], newColor[2])
                    v = v if v > 0.8 else (v * 1.25)
                    r, g, b = imgui.color_convert_hsv_to_rgb(h, s, v)

                    self.__CurrentThemeActive.AddFields({
                        imgui.COLOR_TAB         : ImVec4( *newColor, 1.0 ),
                        imgui.COLOR_TAB_HOVERED : ImVec4( r, g, b, 1.0 ),
                        imgui.COLOR_TAB_ACTIVE  : ImVec4( *newColor, 1.0 ),

                        imgui.COLOR_TAB_UNFOCUSED         : ImVec4( r, g, b, 1.0 ),
                        imgui.COLOR_TAB_UNFOCUSED_ACTIVE  : ImVec4( *newColor, 1.0 )
                    })

                changed, newColor = UILib.DrawColor3Controls(
                    "Buttons", self.__CurrentThemeActive.Fields[imgui.COLOR_BUTTON], columnWidth
                )
                if changed:
                    h, s, v = imgui.color_convert_rgb_to_hsv(newColor[0], newColor[1], newColor[2])
                    v = (v * 0.25) if v > 0.8 else (v * 1.1)
                    r, g, b = imgui.color_convert_hsv_to_rgb(h, s, v)

                    self.__CurrentThemeActive.AddFields({
                        imgui.COLOR_BUTTON         : ImVec4( *newColor, 0.40 ),
                        imgui.COLOR_BUTTON_HOVERED : ImVec4( *newColor, 1.00 ),
                        imgui.COLOR_BUTTON_ACTIVE  : ImVec4( r, g, b, 1.00 ),
                    })
                
                imgui.pop_id()
                imgui.text("")

            imgui.set_cursor_pos_y(imgui.get_window_content_region_max()[1] - 25)
            imgui.set_cursor_pos_x(imgui.get_window_content_region_max()[0] - 90)

            save = imgui.button("Save")
            if imgui.is_item_hovered():
                imgui.begin_tooltip()
                imgui.text("Your Theme Preferences will be saved locally")
                imgui.end_tooltip()

            imgui.same_line()
            if imgui.button("Close"): self.__ShowThemeEditor = False

            if save:
                if preset == "Default Light":
                    self.__CurrentTheme = ImGuiTheme.DefaultLight.Copy()
                    self.__CurrentThemeActive = ImGuiTheme.LightActive.Copy()

                elif preset == "Default Dark":
                    self.__CurrentTheme = ImGuiTheme.DefaultDark.Copy()
                    self.__CurrentThemeActive = ImGuiTheme.Ruth.Copy()
                
                elif preset == "Ruth":
                    self.__CurrentTheme = ImGuiTheme.Ruth.Copy()
                    self.__CurrentThemeActive = ImGuiTheme.DefaultDark.Copy()

                with open(f"{Cache.GetLocalSaveDirectory()}\\ThemePref.json", 'w') as f: json.dump({"Pref": preset}, f)
                
                with open(f"{Cache.GetLocalSaveDirectory()}\\Theme.json", 'w') as f:
                    json.dump(self.__CurrentTheme.Fields, f)
                with open(f"{Cache.GetLocalSaveDirectory()}\\ThemeActive.json", 'w') as f:
                    json.dump(self.__CurrentThemeActive.Fields, f)

                ImGuiLayer.SetTheme(self.__CurrentTheme)
                self.__ShowThemeEditor = False

    def UI_Toolbar(self) -> None:
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, ImVec2(0, 2))
        imgui.push_style_var(imgui.STYLE_ITEM_INNER_SPACING, ImVec2(0, 0))
        imgui.push_style_color(imgui.COLOR_BUTTON, 0, 0, 0, 0)

        colors = imgui.get_style().colors
        buttonHovered = colors[imgui.COLOR_BUTTON_HOVERED]
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, buttonHovered.x, buttonHovered.y, buttonHovered.z, 0.5)
        buttonActive = colors[imgui.COLOR_BUTTON_ACTIVE]
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, buttonActive.x, buttonActive.y, buttonActive.z, 0.5)

        flags = imgui.WINDOW_NO_DECORATION | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_SCROLL_WITH_MOUSE
        with imgui.begin("##toolbar", flags=flags):
            size = imgui.get_window_height() - 4.0
            icon: Texture2D = self.__StopIcon if self.__SceneState == EditorLayer.SceneStateEnum.Play else self.__PlayIcon            
            imgui.set_cursor_pos_x((imgui.get_window_content_region_max()[0] * 0.5) - (size * 0.5))

            if imgui.image_button(icon.RendererID, size, size, (0, 0), (1, 1)):
                if   self.__SceneState == EditorLayer.SceneStateEnum.Edit: self.__OnScenePlay()
                elif self.__SceneState == EditorLayer.SceneStateEnum.Play: self.__OnScenePause()

            if imgui.is_item_hovered():
                imgui.begin_tooltip()
                imgui.text("You can hit F5 to Play/Pause")
                imgui.end_tooltip()

        imgui.pop_style_var(2)
        imgui.pop_style_color(3)

    def OnUpdate(self, timestep: Timestep) -> None: 
        timer = PI_TIMER("EditorLayer::OnUpdate")
        self.__Framerate = 1 / timestep.Seconds
        if self.__ViewportFocused: self.__EditorCamera.OnUpdate(timestep.Seconds)

        spec = self.__Framebuffer.Spec
        if self.__ViewportSize.x > 0.0 \
            and self.__ViewportSize.y > 0.0 \
            and ( spec.Width != self.__ViewportSize[0] or spec.Height != self.__ViewportSize[1] ):
            
            self.__Framebuffer.Resize(*self.__ViewportSize)
            Renderer.OnResize(*self.__ViewportSize)
            self.__EditorCamera.SetAspectRatio(self.__ViewportSize.x / self.__ViewportSize.y)
            self.__EditorScene.OnViewportResize(*self.__ViewportSize)
            self.__ActiveScene.OnViewportResize(*self.__ViewportSize)

        with self.__Framebuffer:
            RenderCommand.Clear()

            # Clear the 2nd Attachment to 0
            # NOTE: 0 is not a valid ID in esper
            self.__Framebuffer.ClearAttachment(1, Math.PythonInt32ToBytes(0))

            if self.__SceneState == EditorLayer.SceneStateEnum.Edit:
                self.__ActiveScene.OnUpdateEditor(float(timestep), self.__EditorCamera)
            elif self.__SceneState == EditorLayer.SceneStateEnum.Play:
                self.__ActiveScene.OnUpdateRuntime(float(timestep))
                
            self.__ActiveScene.Draw()

            mx, my = Input.GetMousePos()
            mx -= self.__ViewportBounds[0][0]
            my -= self.__ViewportBounds[0][1]
            viewportSize = ImVec2(
                self.__ViewportBounds[1][0] - self.__ViewportBounds[0][0],
                self.__ViewportBounds[1][1] - self.__ViewportBounds[0][1]
            )
            my = viewportSize[1] - my
            mouseX = int(mx)
            mouseY = int(my)

            if mouseX >= 0 and mouseY >= 0 and mouseX < int(viewportSize[0]) and mouseY < int(viewportSize[1]):
                pixelData = Math.BytesToPythonInt32(
                    self.__Framebuffer.ReadPixel(1, mouseX, mouseY),
                    byteorder='little'   # OpenGL retrives the values in reverse order
                )
                self.__HoveredEntity = Entity(pixelData, self.__ActiveScene) if pixelData != 0 else None
