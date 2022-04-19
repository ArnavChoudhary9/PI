# Hackey Fix for relative path problem
# TODO: Try to remove it later
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Main Code starts from here
from PI import *

class CubeLayer(Layer):
    __Scene : Scene
    __AssetManager: AssetManager
    __CameraController: PerspectiveCameraController

    __AutoRotate  : bool

    __Framebuffer: Framebuffer
    __ViewportSize: imgui.Vec2
    
    __Framerate: float
    __ShowDebugStats: bool
    vSync = PI_V_SYNC

    def __init__(self, name: str = "CubeLayer") -> None:
        super().__init__(name=name)
        self.__ViewportSize = imgui.Vec2( 0, 0 )
        self.__CameraController = PerspectiveCameraController(PerspectiveCamera(45, Input.GetWindow().AspectRatio))

    def OnAttach(self) -> None:
        self.__AssetManager = AssetManager()
        self.__Scene = Scene("Default 3D")

        mesh: Mesh = self.__Scene.LoadMesh(".\\Assets\\Meshes\\Sphere.obj")[0]
        mesh.Translate(pyrr.Vector3([ 3.0, 0.0, -7.0 ]))

        mesh: Mesh = self.__Scene.LoadMesh(".\\Assets\\Meshes\\TexturedCube.obj")[0]
        mesh.Translate(pyrr.Vector3([ -3.0, 0.0, -7.0 ]))

        mesh: Mesh = self.__Scene.LoadMesh(".\\Assets\\Meshes\\Monkey.obj")[0]
        mesh.Translate(pyrr.Vector3([ 0.0, -0.8, -7.0 ]))

        mesh: Mesh = self.__Scene.LoadMesh(".\\Assets\\Meshes\\Plane.obj")[0]
        mesh.Translate(pyrr.Vector3([ 0.0, -1.0, 0.0 ]))
        mesh.SetScale(pyrr.Vector3([ 15.0, 1.0, 15.0 ]))

        mesh: Mesh = self.__Scene.LoadMesh(".\\Assets\\Meshes\\Hut.obj")[0]
        mesh.Translate(pyrr.Vector3([ 7.5, 0.0, -10.0 ]))

        mesh: Mesh = self.__Scene.LoadMesh(".\\Assets\\Meshes\\Torus.obj")[0]
        mesh.Translate(pyrr.Vector3([ -7.5, -0.75, -10.0 ]))

        # Verb driven API
        (
            self.__Scene
                # Point Lights
                .CreatePointLight(
                    position=pyrr.Vector3([ -5.0, 0.0, -10.0 ]),
                    diffuse=pyrr.Vector3([ 1.0, 1.0, 1.0 ]),
                    intensity=3.5
                )

                .CreatePointLight(
                    position=pyrr.Vector3([ 5.0, 0.0, -10.0 ]),
                    diffuse=pyrr.Vector3([ 1.0, 1.0, 1.0 ]),
                    intensity=3.5
                )
                
                # Spot Lights
                .CreateSpotLight(
                    position=pyrr.Vector3([ 0.0, 5.0, -7.0 ]),
                    cutOff=30, outerCutOff= 35,
                    intensity=1.5
                )
                

                # Directional Light
                # This should be at last as it does not return Scene
                .DirectionalLight
                    .SetDirection(pyrr.Vector3([ 0.0, -1.0, -2.0 ]))
                    .SetIntensity(0)
        )

        self.__Framebuffer: Framebuffer = Framebuffer.Create(Framebuffer.Specs(
            256, 256
        ))

        self.__Framebuffer.Unbind()

        self.__AutoRotate  = False
        self.__Framerate   = 60
        self.__ShowDebugStats = False

    def OnEvent(self, event: Event) -> None:
        self.__CameraController.OnEvent(event)

    def OnImGuiRender(self) -> None:
        timer = PI_TIMER("CubeLayer::OnImGuiRender")
    
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

        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0.0, 0.0))
        with imgui.begin("DockSpace Demo", True, windowFlags):
            imgui.pop_style_var()

            if optFullscreen:
                imgui.pop_style_var(2)

            io = imgui.get_io()
            if io.config_flags & imgui.CONFIG_DOCKING_ENABLE:
                dockspaceID = imgui.get_id("Mydockspace")
                imgui.dockspace(dockspaceID, (0.0, 0.0), dockspaceFlage)

            with imgui.begin_menu_bar():
                if imgui.begin_menu("File"):
                    clicked, state = imgui.menu_item("Quit", "Ctrl+Q", False, True)
                    imgui.end_menu()

            with imgui.begin("Settings"):
                mesh: Mesh = self.__Scene.Meshes[0]
                changed, self.__AutoRotate = imgui.checkbox("Auto Rotate", self.__AutoRotate)
                
                imgui.text("\nTransform:")
                changed, translation = imgui.drag_float3("Location" , *mesh.Translation , change_speed=0.05 )
                if changed: mesh.SetTranslation(pyrr.Vector3([ *translation ]))

                changed, scale       = imgui.drag_float3("Scale"    , *mesh.Scale       , change_speed=0.05 )
                if changed: mesh.SetScale(pyrr.Vector3([ *scale ]))

                changed, rotation    = imgui.drag_float3("Rotation", *mesh.Rotation, change_speed=1)
                if changed: mesh.SetRotation(pyrr.Vector3([ *rotation ]))

                imgui.text("\nLight Transforms")

                light = self.__Scene.DirectionalLight
                changed, lightDir = imgui.drag_float3("LightDirection" , *light.Direction , change_speed=0.05 )
                if changed: light.SetDirection(pyrr.Vector3([ *lightDir ]))

                changed, lightColor = imgui.color_edit3("LightColor", *light.Diffuse)
                if changed:
                    color = pyrr.Vector3([ *lightColor ])
                    light.SetDiffuse(color)
                    light.SetAmbient(color * 0.2)
                    light.SetSpecular(color * 0.5)
            
                if PI_DEBUG:
                    imgui.text("\n")
                    if imgui.button("Open Debug Stats"): self.__ShowDebugStats = True
                        
                    if self.__ShowDebugStats:   
                        with imgui.begin("DEBUG Settings"):
                            clicked, self.vSync = imgui.checkbox("VSync", self.vSync)

                            if clicked:
                                Input.GetWindow().SetVSync(self.vSync)
                                PI_V_SYNC = self.vSync

                            imgui.text("FPS: {}".format(round(self.__Framerate)))  

            # imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, ( 0, 0 ))
            # with imgui.begin("Viewport"):
            #     viewportPanelSize = imgui.get_content_region_available()
            #     self.__ViewportSize = viewportPanelSize

            #     PI_CLIENT_TRACE("Viewport Size: {}", viewportPanelSize)

            #     imgui.image(
            #         self.__Framebuffer.ColorAttachment0,
            #         self.__ViewportSize.x, self.__ViewportSize.y,
            #         ( 0, 1 ), ( 1, 0 )
            #     )

            #     imgui.text("Test text.")
            # imgui.pop_style_var()

        with imgui.begin("Instructions"):
            imgui.text(
                "Welcome to PI Engine Demo!\nCurrent version: {}\nCurrent Configuration: {}\n\n"
                    .format(PI_VERSION, PI_CONFIG)
            )

            imgui.text("Use WASD to move the Camera.\nLeft Shift and Left Ctrl to control the altitude.\nRight Click and Drag to rotate Camera.\n\n")

            imgui.text("")

    def OnUpdate(self, timestep: Timestep) -> None: 
        timer = PI_TIMER("CubeLayer::OnUpdate")
        self.__Framerate = 1 / timestep.Seconds 
        self.__CameraController.OnUpdate(timestep.Seconds)

        spec = self.__Framebuffer.Spec
        if self.__ViewportSize.x > 0.0 \
            and self.__ViewportSize.y > 0.0 \
            and ( spec.Width != self.__ViewportSize[0] or spec.Height != self.__ViewportSize[1] ):
            
            self.__Framebuffer.Resize(*self.__ViewportSize)
            Renderer.OnResize(*self.__ViewportSize)
            self.__CameraController.Camera.SetAspectRatio(self.__ViewportSize.x / self.__ViewportSize.y)

        if self.__AutoRotate:
            self.__Scene.Meshes[0].Rotate(degrees([
                0.45 * timestep.Seconds,
                0.5  * timestep.Seconds,
                0.55 * timestep.Seconds
            ]))

        # self.__Framebuffer.Bind()

        # Renderer.OnResize(256, 256)
        # self.__CameraController.Camera.SetAspectRatio(1)

        with BeginRenderer(self.__CameraController.Camera):
            Renderer.SubmitScene(self.__Scene)
            
        # self.__Framebuffer.Unbind()
