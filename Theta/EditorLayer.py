from PI import *

from ImGuiElements.SceneHierarchyPanel import *
from ImGuiElements.ContentBrowserPanel import *
from ImGuiElements.DebugLogger         import *
from ImGuiElements.ProjectSettingsTab  import *
from ImGuiElements.DebugStatsPanel     import *
from ImGuiElements.ThemeEditorTab      import *

from ImGuiElements.UndoManager import *

INSTRUCTION_TEXT: str = \
"""Welcome to Theta: The PI Editor
Current version: {0}
Current Configuration: {1}

Content Browser:
-> Drag and drop scenes from ContentBrowser (Scenes/*) to Viewport to load the scene.

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
    __ActiveProject : Project

    __ActiveScene : Scene
    __EditorScene : Scene

    __SceneHierarchyPanel : SceneHierarchyPanel
    __ThemeEditor         : ThemeEditor
    __ProjectSettingsTab  : ProjectSettingsTab
    __ContentBrowser      : ContentBrowserPanel
    __DebugLogger         : DebugLogger

    __EditorCamera: EditorCamera

    __Framebuffer: Framebuffer
    __ViewportSize: ImVec2

    __ViewportBounds : List[ImVec2]
    __HoveredEntity  : Entity = 0

    __ViewportFocused : bool
    __ViewportHovered : bool

    __Panels: List = []

    class SceneStateEnum:
        Edit  : int = 0
        Play  : int = 1
        Pause : int = 2

    __SceneState: int
    __Icons: Dict[str, Texture2D]

    __Framerate: float
    __LastFrameTime: float

    __ShowDebugStats: bool

    __ShowProjectTab: bool
    __Temp_ProjectName: str
    __Temp_ProjectPath: str

    vSync = PI_V_SYNC

    def __init__(self, name: str="EditorLayer") -> None:
        super().__init__(name=name)
        self.__ViewportSize = ImVec2( 0, 0 )
        self.__ViewportBounds = [ ImVec2( 0, 0 ) , ImVec2( 0, 0 ) ]
        self.__EditorCamera = EditorCamera(45, 1.778, 0.1, 1000)

    def OnAttach(self) -> None:
        timer = PI_TIMER("EditorLayer::OnAttach")

        self.__ActiveProject = Project(projFileLoc="DefaultProject\\DefaultProject.PIProj")
        ScriptingEngine.Init(str(self.__ActiveProject.ScriptsLocation))

        self.__EditorScene = self.__ActiveProject.StartScene
        self.__ActiveScene = self.__EditorScene

        self.__SceneHierarchyPanel = SceneHierarchyPanel(self.__ActiveProject)
        self.__SceneHierarchyPanel.SetContext(self.__ActiveScene)

        self.__DebugLogger = DebugLogger()
        UndoManager()        # Init UndoManager

        specs = Framebuffer.Specs()
        specs.Width = 1280
        specs.Height = 720
        specs.AttachmentSpecification = Framebuffer.AttachmentSpecification(
            TextureSpecification( TextureFormat.RGBA8       ),
            TextureSpecification( TextureFormat.RED_INTEGER ),
            TextureSpecification( TextureFormat.DEPTH       )
        )
        self.__Framebuffer: Framebuffer = Framebuffer.Create(specs)
        self.__Framebuffer.Unbind()

        self.__Framerate = 60
        self.__ShowDebugStats = False
        self.__ShowProjectTab = False

        self.__Temp_ProjectName = ""
        self.__Temp_ProjectPath = ""

        self.__ThemeEditor = ThemeEditor()
        self.__ProjectSettingsTab = ProjectSettingsTab()
        self.__ContentBrowser = ContentBrowserPanel(self.__ActiveProject)

        self.__ViewportFocused : bool = True
        self.__ViewportHovered : bool = True

        self.__Panels.append(self.__SceneHierarchyPanel)
        self.__Panels.append(self.__ContentBrowser)
        self.__Panels.append(self.__DebugLogger)

        self.__SceneState = EditorLayer.SceneStateEnum.Edit
        self.__Icons = {}

        try:
            self.__Icons["Play"]   = Texture2D.Create( ".\\Theta\\Resources\\Icons\\PlayButton.png"  )
            self.__Icons["Stop"]   = Texture2D.Create( ".\\Theta\\Resources\\Icons\\StopButton.png"  )
            self.__Icons["Pause"]  = Texture2D.Create( ".\\Theta\\Resources\\Icons\\PauseButton.png" )
            self.__Icons["Step"]   = Texture2D.Create( ".\\Theta\\Resources\\Icons\\StepButton.png"  )
            self.__Icons["Restart"] = Texture2D.Create( ".\\Theta\\Resources\\Icons\\ResartButton.png"  )

        # This is here for Building
        # 'cause the Build looks for files in '.'
        except FileNotFoundError:
            self.__Icons["Play"]   = Texture2D.Create( ".\\Resources\\Icons\\PlayButton.png"   )
            self.__Icons["Stop"]   = Texture2D.Create( ".\\Resources\\Icons\\StopButton.png"   )
            self.__Icons["Pause"]  = Texture2D.Create( ".\\Resources\\Icons\\PauseButton.png"  )
            self.__Icons["Step"]   = Texture2D.Create( ".\\Resources\\Icons\\StepButton.png"   )
            self.__Icons["Restart"] = Texture2D.Create( ".\\Resources\\Icons\\ResartButton.png" )

    def __NewScene(self) -> None:
        self.__OnSceneStop()
        
        newScene = Scene()
        newScene.OnViewportResize(self.__ActiveScene._ViewportWidth, self.__ActiveScene._ViewportHeight)
        self.__EditorScene = newScene
        self.__ActiveScene = self.__EditorScene
        self.__SceneHierarchyPanel.SetContext(self.__EditorScene)

    def __SaveScene(self, dialogbox: bool=False) -> None:
        self.__OnSceneStop()
        
        if self.__ActiveScene._Filepath != None and not dialogbox:
            fileName = self.__ActiveScene._Filepath
            if not fileName.lower().endswith(".pi"): fileName += ".PI"
            Scene.Serialize(self.__ActiveScene, fileName)
            return
        
        elif self.__ActiveScene._Filepath == None and not dialogbox:
            PI_CORE_WARN("The scene should be saved first.")
            DebugConsole.Warn("The scene should be saved first.")
            return

        if not dialogbox: return
        cancelled, fileName = UILib.DrawFileSaveDialog( ( ("PI scene file (*.PI)", ".PI"), ) )
        if not cancelled:
            if not fileName.lower().endswith(".pi"): fileName += ".PI"
            Scene.Serialize(self.__ActiveScene, fileName)

    def __LoadScene(self, filename: str=None) -> None:
        self.__OnSceneStop()

        cancelled = False
        if not filename  : cancelled, filename = UILib.DrawFileLoadDialog( ( ("PI scene file (*.PI)", ".PI"), ) )
        if not cancelled : self.__EditorScene = Scene.Deserialize(self.__EditorScene, filename)
        self.__ActiveScene = self.__EditorScene
        self.__SceneHierarchyPanel.SetContext(self.__EditorScene)
    
    def __LoadProject(self, filename: str=None) -> None:
        if filename is None:
            cancil, filename = UILib.DrawFileLoadDialog(( ("PI Project File (*.PIProj)", ".PIProj"), ))
            if cancil: return

        self.__ActiveProject = Project(projFileLoc=filename)
        self.__LoadScene(str(self.__ActiveProject.StartSceneLocation))
        self.__ContentBrowser.SetProject(self.__ActiveProject)

        self.__ProjectSettingsTab.Init()

    def __Undo(self) -> None:
        event = UndoManager.GetInstance().PopUndo()
        if   type(event) == UndoEvent: return
        elif type(event) == ComponentDeletionEvent:
            event.Entity._AddComponentInstance(event.ComponentDeleted)

    def __Redo(self) -> None:
        event = UndoManager.GetInstance().PopRedo()
        if   type(event) == UndoEvent: return
        elif type(event) == ComponentDeletionEvent:
            event.Entity.RemoveComponent(type(event.ComponentDeleted))

    def __CheckKeys(self, event: KeyPressedEvent) -> bool:
        control = Input.IsKeyPressed(PI_KEY_LEFT_CONTROL) or Input.IsKeyPressed(PI_KEY_RIGHT_CONTROL)
        shift   = Input.IsKeyPressed(PI_KEY_LEFT_SHIFT)   or Input.IsKeyPressed(PI_KEY_RIGHT_SHIFT)

        if control:
            if not shift:
                if event.KeyCode == PI_KEY_Q:
                    StateManager.GetCurrentApplication().Close()
                    return True

                if event.KeyCode == PI_KEY_N:
                    self.__NewScene()
                    return True

                if event.KeyCode == PI_KEY_S and not shift:
                    if not shift: self.__SaveScene()
                    else: self.__SaveScene(dialogbox=True)
                    return True

                if event.KeyCode == PI_KEY_O:
                    self.__LoadScene()
                    return True

                if event.KeyCode == PI_KEY_Z:
                    self.__Undo()
                    return True

                if event.KeyCode == PI_KEY_Y:
                    self.__Redo()
                    return True
            
            else:
                if event.KeyCode == PI_KEY_F5:
                    self.__SceneRestart()
                    return True

        else:
            if event.KeyCode == PI_KEY_F5:
                if not shift and self.__SceneState == EditorLayer.SceneStateEnum.Edit:
                    self.__OnScenePlay()
                elif shift and self.__SceneState != EditorLayer.SceneStateEnum.Edit:
                    self.__OnSceneStop()
                elif not shift and self.__SceneState == EditorLayer.SceneStateEnum.Pause:
                    self.__OnSceneResume()
                return True

            if not shift:
                if event.KeyCode == PI_KEY_F6:
                    if self.__SceneState == EditorLayer.SceneStateEnum.Play: self.__OnScenePause()
                    return True
                
                if event.KeyCode == PI_KEY_F10:
                    if self.__SceneState == EditorLayer.SceneStateEnum.Pause:
                        self.__ActiveScene.OnUpdateRuntime(self.__LastFrameTime)
                    return True
                
                if event.KeyCode in [PI_KEY_DELETE, PI_KEY_X]:
                    selectedEntity = self.__SceneHierarchyPanel.SelectedEntity
                    if selectedEntity: self.__ActiveScene.DestroyEntity(selectedEntity)
                    self.__SceneHierarchyPanel.SetSelectedEntity(None)
                    return True
                
            else:
                if event.KeyCode == PI_KEY_D:
                    selection = self.__SceneHierarchyPanel.SelectedEntity
                    if selection: self.__ActiveScene.DuplicateEntity(selection)
                    return True
                
                if event.KeyCode == PI_KEY_N:
                    self.__ActiveScene.CreateEntity("New Entity")
                    return True

        return False

    def __MouseButtonClick(self, event: MouseButtonPressedEvent) -> bool:
        if event.ButtonCode == PI_MOUSE_BUTTON_LEFT:
            if self.__ViewportHovered and not Input.IsKeyPressed(PI_KEY_LEFT_ALT):
                self.__SceneHierarchyPanel.SetSelectedEntity(self.__HoveredEntity)

    def OnEvent(self, event: Event) -> None:
        self.__EditorCamera.OnEvent(event)

        dispatcher = EventDispatcher(event)
        dispatcher.Dispach(self.__CheckKeys, EventType.KeyPressed)
        dispatcher.Dispach(self.__MouseButtonClick, EventType.MouseButtonPressed)

    def OnImGuiRender(self) -> None:    
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
                    if imgui.menu_item("Theme Editor")[0]: self.__ThemeEditor.Show()
                    if imgui.menu_item("Project Settings")[0]: self.__ProjectSettingsTab.Show()

                    imgui.separator()
                    if not self.__ShowDebugStats:
                        if imgui.menu_item("Open Debug Stats")[0]: self.__ShowDebugStats = True
                    else:
                        if imgui.menu_item("Close Debug Stats")[0]: self.__ShowDebugStats = False

                    imgui.end_menu()

                if imgui.begin_menu("Project"):
                    if imgui.menu_item( "Open Project" )[0]: self.__LoadProject()
                    if imgui.menu_item( "New Project"  )[0]: self.__ShowProjectTab = True

                    imgui.end_menu()

            for panel in self.__Panels: panel.OnImGuiRender()

            if self.__ShowDebugStats:   
                self.vSync = DebugStatsPanel.OnImGuiRender(self.__Framerate, self.__HoveredEntity)

            if self.__ShowProjectTab:
                with imgui.begin("New Project"):
                    _, self.__Temp_ProjectName = UILib.DrawTextFieldControls(
                        "Name", self.__Temp_ProjectName, columnWidth=75
                    )

                    _, self.__Temp_ProjectPath = UILib.DrawSelectableDirField(
                        "Location", self.__Temp_ProjectPath, columnWidth=75
                    )

                    imgui.set_cursor_pos_x(imgui.get_window_content_region_max()[0] - 100)
                    imgui.set_cursor_pos_y(imgui.get_window_content_region_max()[1] - 25)

                    if UILib.DrawButton("Close"): self.__ShowProjectTab = False
                    imgui.same_line()
                    if UILib.DrawButton("Create"):
                        if self.__Temp_ProjectName != "" and self.__Temp_ProjectPath != "":
                            path = f"{self.__Temp_ProjectPath}\\{self.__Temp_ProjectName}"
                            Project(self.__Temp_ProjectName, newLoc=path)
                            self.__LoadProject(f"{path}\\{self.__Temp_ProjectName}.PIProj")
                            self.__ShowProjectTab = False

                        else: PI_CLIENT_ERROR("Cannot Make Project without Name or Path")

            self.__ThemeEditor.OnImGuiRender()
            self.__ProjectSettingsTab.OnImGuiRender(
                self.__ThemeEditor.CurrentTheme.Fields[imgui.COLOR_WINDOW_BACKGROUND],
                self.__ThemeEditor.CurrentTheme.Fields[imgui.COLOR_BUTTON_ACTIVE]
            )

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

                        if data.lower().endswith('.pi'): self.__LoadScene(data)  
                        elif data.lower().endswith('.obj'):
                            entity = self.__ActiveScene.CreateEntity("New Entity")
                            entity.AddComponent(MeshComponent, data)
                        else: PI_CLIENT_WARN("File: {} is not a Scene/Mesh file", data)
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

        DebugConsole.Clear()
        self.__DebugLogger.ErrorOccurred = False
        
        self.__ActiveScene.OnStartRuntime()
        self.__ThemeEditor.SetCurrentActiveTheme()

        if (self.__ProjectSettingsTab.Settings["Debugging.EnableDebugging"] and
            self.__ProjectSettingsTab.Settings["Debugging.WaitOnPlay"]):
            ScriptingEngine.Debugger.AttachToDebugger()

    def __OnSceneStop(self) -> None:
        self.__SceneState = EditorLayer.SceneStateEnum.Edit
        self.__ActiveScene.OnStopRuntime()

        self.__ActiveScene = self.__EditorScene

        self.__SceneHierarchyPanel.SetContext(self.__EditorScene)
        self.__SceneHierarchyPanel.SetSelectedEntity(None)
        self.__ThemeEditor.SetCurrentTheme()

    def __OnScenePause(self) -> None:
        if self.__SceneState == EditorLayer.SceneStateEnum.Edit: return
        self.__SceneState = EditorLayer.SceneStateEnum.Pause

    def __OnSceneResume(self) -> None:
        if self.__SceneState == EditorLayer.SceneStateEnum.Edit: return
        self.__SceneState = EditorLayer.SceneStateEnum.Play

    def __SceneRestart(self) -> None:
        if self.__SceneState == EditorLayer.SceneStateEnum.Edit: return
        if self.__SceneState == EditorLayer.SceneStateEnum.Pause: self.__OnSceneResume()
        self.__OnSceneStop()
        self.__OnScenePlay()

    def UI_Toolbar(self) -> None:
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, ImVec2(0, 2))
        imgui.push_style_var(imgui.STYLE_ITEM_INNER_SPACING, ImVec2(0, 0))
        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, ImVec2(0, 0))
        imgui.push_style_color(imgui.COLOR_BUTTON, 0, 0, 0, 0)

        colors = imgui.get_style().colors
        buttonHovered = colors[imgui.COLOR_BUTTON_HOVERED]
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, buttonHovered.x, buttonHovered.y, buttonHovered.z, 0.5)
        buttonActive = colors[imgui.COLOR_BUTTON_ACTIVE]
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, buttonActive.x, buttonActive.y, buttonActive.z, 0.5)

        flags = imgui.WINDOW_NO_DECORATION | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_SCROLL_WITH_MOUSE
        with imgui.begin("##toolbar", flags=flags):
            size = imgui.get_window_height() - 4.0
            icon: Texture2D = (
                self.__Icons["Stop"] 
                if self.__SceneState != EditorLayer.SceneStateEnum.Edit
                else self.__Icons["Play"]
            )

            cursorStartPos = {
                EditorLayer.SceneStateEnum.Edit  : 1*(size * 0.5),
                EditorLayer.SceneStateEnum.Play  : 3*(size * 0.5),
                EditorLayer.SceneStateEnum.Pause : 4*(size * 0.5)
            }
            imgui.set_cursor_pos_x(
                (imgui.get_window_content_region_max()[0] * 0.5) - cursorStartPos[self.__SceneState]
            )

            if imgui.image_button(icon.RendererID, size, size, (0, 0), (1, 1)):
                if    self.__SceneState == EditorLayer.SceneStateEnum.Edit: self.__OnScenePlay()
                else: self.__OnSceneStop()

            UILib.TooltipIfHovered(
                "Play (F5)"
                if self.__SceneState == EditorLayer.SceneStateEnum.Edit else
                "Stop (Shift+F5)"
            )

            if self.__SceneState != EditorLayer.SceneStateEnum.Edit:
                imgui.same_line()

                if not self.__SceneState == EditorLayer.SceneStateEnum.Pause:
                    imgui.push_style_color(imgui.COLOR_BUTTON, 0, 0, 0, 0)
                else: imgui.push_style_color(imgui.COLOR_BUTTON, 0.35, 0.35, 0.35, 1)

                if imgui.image_button(self.__Icons["Pause"].RendererID, size, size, (0, 0), (1, 1)):
                    if   self.__SceneState == EditorLayer.SceneStateEnum.Play  : self.__OnScenePause  ()
                    elif self.__SceneState == EditorLayer.SceneStateEnum.Pause : self.__OnSceneResume ()

                imgui.pop_style_color()

                UILib.TooltipIfHovered(
                    "Pause (F6)"
                    if self.__SceneState == EditorLayer.SceneStateEnum.Play else
                    "Resume (F5)"
                )

                imgui.same_line()
                if imgui.image_button(self.__Icons["Restart"].RendererID, size, size, (0, 1), (1, 0)):
                    self.__SceneRestart()

                UILib.TooltipIfHovered("Restart (Shift+Ctrl+F5)")

            if self.__SceneState == EditorLayer.SceneStateEnum.Pause:
                imgui.same_line()
                if imgui.image_button(self.__Icons["Step"].RendererID, size, size, (0, 0), (1, 1)):
                    self.__ActiveScene.OnUpdateRuntime(self.__LastFrameTime)
                UILib.TooltipIfHovered("Step (F10)")

        imgui.pop_style_color(3)
        imgui.pop_style_var(3)

    def OnUpdate(self, timestep: Timestep) -> None:
        self.__Framerate = 1 / timestep.FixedTime
        self.__LastFrameTime = timestep.FixedTime

        if self.__ViewportFocused: self.__EditorCamera.OnUpdate(timestep.FixedTime)

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
                self.__ActiveScene.OnUpdateEditor(timestep.FixedTime, self.__EditorCamera)
            elif self.__SceneState == EditorLayer.SceneStateEnum.Play:
                self.__ActiveScene.OnUpdateRuntime(min(timestep.GameDelta, 1/10))   # This is to stop abrupt behaviour in scripts
            elif self.__SceneState == EditorLayer.SceneStateEnum.Pause:
                self.__ActiveScene.OnUpdateEditor(timestep.Seconds, self.__EditorCamera)
                
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

        if self.__SceneState == EditorLayer.SceneStateEnum.Play and self.__DebugLogger.ErrorOccurred:
            self.__DebugLogger.ErrorOccurred = False
            self.__OnSceneStop()
