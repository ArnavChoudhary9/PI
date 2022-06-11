from PI import *
from Panels.SceneHierarchyPanel import *
from Panels.ContentBrowserPanel import *

INSTRUCTION_TEXT: str = \
"""Welcome to PI Engine Demo!
Current version: {0}
Current Configuration: {1}

Use WASD to move the Camera.
Left Shift and Left Ctrl to control the altitude.
Left Click and Drag to rotate Camera.""" \
    .format(PI_VERSION, PI_CONFIG)

class EditorLayer(Layer):
    __Scene : Scene
    __SceneHierarchyPanel: SceneHierarchyPanel
    __ContentBrowserPanel: ContentBrowserPanel
    __EditorCamera: EditorCamera

    __Framebuffer: Framebuffer
    __ViewportSize: ImVec2

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
    vSync = PI_V_SYNC

    def __init__(self, name: str = "EditorLayer") -> None:
        super().__init__(name=name)
        self.__ViewportSize = ImVec2( 0, 0 )
        self.__EditorCamera = EditorCamera(45, 1.778, 0.1, 1000)
        # self.__EditorCamera = PerspectiveCameraController(PerspectiveCamera(45, 1.778, 0.1, 1000))

    def OnAttach(self) -> None:
        timer = PI_TIMER("EditorLayer::OnAttach")
        self.__Scene = Scene()

        self.__SceneHierarchyPanel = SceneHierarchyPanel()
        self.__SceneHierarchyPanel.SetContext(self.__Scene)

        self.__ContentBrowserPanel = ContentBrowserPanel()

        specs = Framebuffer.Specs(1200, 600)
        specs.Attachments = (
            FramebufferAttachments.ColorAlpha, FramebufferAttachments.Depth
        )
        self.__Framebuffer: Framebuffer = Framebuffer.Create(specs)
        self.__Framebuffer.Unbind()

        self.__Framerate   = 60
        self.__ShowDebugStats = False

        self.__ViewportFocused : bool = True
        self.__ViewportHovered : bool = True

        self.__Panels.append(self.__SceneHierarchyPanel)
        self.__Panels.append(self.__ContentBrowserPanel)

        self.__SceneState = EditorLayer.SceneStateEnum.Edit

		# m_IconPlay = Texture2D::Create("Resources/Icons/PlayButton.png");
		# m_IconStop = Texture2D::Create("Resources/Icons/StopButton.png");

        self.__PlayIcon = Texture2D.Create(".\\Theta\\Resources\\Icons\\PlayButton.png")
        self.__StopIcon = Texture2D.Create(".\\Theta\\Resources\\Icons\\StopButton.png")

    def __NewScene(self) -> None:
        newScene = Scene()
        newScene.OnViewportResize(self.__Scene._ViewportWidth, self.__Scene._ViewportHeight)
        del self.__Scene
        self.__Scene = newScene
        self.__SceneHierarchyPanel.SetContext(self.__Scene)

    def __SaveScene(self) -> None:
        cancelled, fileName = UILib.DrawFileSaveDialog( ( ("PI scene file (*.PI)", ".PI"), ) )
        if not cancelled:
            if not fileName.endswith(".PI"): fileName += ".PI"
            Scene.Serialize(self.__Scene, fileName)

    def __LoadScene(self, filename: str=None) -> None:
        cancelled = False
        if not filename:
            cancelled, filename = UILib.DrawFileLoadDialog( ( ("PI scene file (*.PI)", ".PI"), ) )
        if not cancelled: self.__Scene = Scene.Deserialize(self.__Scene, filename)
        self.__SceneHierarchyPanel.SetContext(self.__Scene)

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

            if event.KeyCode == PI_KEY_S and control and shift:
                self.__SaveScene()
                return True

            if event.KeyCode == PI_KEY_O and control:
                self.__LoadScene()
                return True

        EventDispatcher(event).Dispach(CheckKeys, EventType.KeyPressed)

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
                    if imgui.menu_item("Save As", "Ctrl+Shift+S", False, True)[0]: self.__SaveScene()
                    if imgui.menu_item("Open", "Ctrl+O", False, True)[0]: self.__LoadScene()                        
                    if imgui.menu_item("Quit", "Ctrl+Q", False, True)[0]: StateManager.GetCurrentApplication().Close()
                    
                    imgui.end_menu()

                if imgui.begin_menu("Edit"):
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
                        PI_V_SYNC = self.vSync

                    imgui.text("FPS: {}".format(round(self.__Framerate)))  

            imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, ImVec2( 0, 0 ))
            with imgui.begin("Viewport"):
                viewportPanelSize = imgui.get_content_region_available()
                self.__ViewportSize = viewportPanelSize

                self.__ViewportFocused = imgui.is_window_focused()
                self.__ViewportHovered = imgui.is_window_hovered()
                
                app: PI_Application = StateManager.GetCurrentApplication()
                app.ImGuiLayer.BlockEvents(not self.__ViewportFocused or not self.__ViewportHovered)

                imgui.image(
                    self.__Framebuffer.GetColorAttachment(0).RendererID,
                    self.__ViewportSize.x, self.__ViewportSize.y,
                    ( 0, 1 ), ( 1, 0 )
                )

                if imgui.begin_drag_drop_target():
                    data: bytes = imgui.accept_drag_drop_payload("CONTENT_BROWSER_ITEM")
                    if data: self.__LoadScene(data.decode('UTF-8'))
                    imgui.end_drag_drop_target()

            imgui.pop_style_var()

            with imgui.begin("Instructions"):
                imgui.text(INSTRUCTION_TEXT)
            
            self.UI_Toolbar()

    def __OnScenePlay(self) -> None:
        self.__SceneState = EditorLayer.SceneStateEnum.Play

    def __OnScenePause(self) -> None: 
        self.__SceneState = EditorLayer.SceneStateEnum.Edit

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
                if self.__SceneState == EditorLayer.SceneStateEnum.Edit: self.__OnScenePlay()
                elif self.__SceneState == EditorLayer.SceneStateEnum.Play: self.__OnScenePause()

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
            self.__Scene.OnViewportResize(*self.__ViewportSize)

        with BindFramebuffer(self.__Framebuffer) as fb:
            if self.__SceneState == EditorLayer.SceneStateEnum.Edit:
                self.__Scene.OnUpdateEditor(float(timestep), self.__EditorCamera)
            elif self.__SceneState == EditorLayer.SceneStateEnum.Play:
                self.__Scene.OnUpdateRuntime(float(timestep))

            self.__Scene.Draw()
