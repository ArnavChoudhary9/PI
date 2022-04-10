# Hackey Fix for relative path problem
# TODO: Try to remove it later
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Main Code starts from here
from PI import *

class CubeLayer(Layer):
    __Meshes : list
    __AssetManager: AssetManager
    __CameraController: PerspectiveCameraController

    __Light : Light

    __AutoRotate  : bool
    
    __Framerate: float
    vSync = PI_V_SYNC

    def __init__(self, camera, name: str = "CubeLayer") -> None:
        super().__init__(name=name)
        self.__CameraController = PerspectiveCameraController(camera)

    def OnAttach(self) -> None:
        self.__AssetManager = AssetManager()
        self.__Meshes = []

        mesh: Mesh = self.__AssetManager.Load(AssetManager.AssetType.MeshAsset, ".\\Assets\\Meshes\\Sphere.obj")
        mesh.Translate(pyrr.Vector3([ 3.0, 0.0, -7.0 ]))
        self.__Meshes.append(mesh.Name)

        mesh: Mesh = self.__AssetManager.Load(AssetManager.AssetType.MeshAsset, ".\\Assets\\Meshes\\Cube.obj")
        mesh.Translate(pyrr.Vector3([ -3.0, 0.0, -7.0 ]))
        self.__Meshes.append(mesh.Name)

        mesh: Mesh = self.__AssetManager.Load(AssetManager.AssetType.MeshAsset, ".\\Assets\\Meshes\\Monkey.obj")
        mesh.Translate(pyrr.Vector3([ 0.0, -0.8, -7.0 ]))
        self.__Meshes.append(mesh.Name)

        mesh: Mesh = self.__AssetManager.Load(AssetManager.AssetType.MeshAsset, ".\\Assets\\Meshes\\Plane.obj")
        mesh.Translate(pyrr.Vector3([ 0.0, -1.0, 0.0 ]))
        mesh.SetScale(pyrr.Vector3([ 15.0, 1.0, 15.0 ]))
        self.__Meshes.append(mesh.Name)

        mesh: Mesh = self.__AssetManager.Load(AssetManager.AssetType.MeshAsset, ".\\Assets\\Meshes\\Hut.obj")
        mesh.Translate(pyrr.Vector3([ 7.5, 0.0, -10.0 ]))
        self.__Meshes.append(mesh.Name)

        mesh: Mesh = self.__AssetManager.Load(AssetManager.AssetType.MeshAsset, ".\\Assets\\Meshes\\Torus.obj")
        mesh.Translate(pyrr.Vector3([ -7.5, -0.75, -10.0 ]))
        self.__Meshes.append(mesh.Name)
        
        self.__Light = Light(position=pyrr.Vector3([ 0.0, 5.0, 10.0 ]))

        self.__AutoRotate  = False
        self.__Framerate   = 60

    def OnEvent(self, event: Event) -> None:
        self.__CameraController.OnEvent(event)

    def OnImGuiRender(self) -> None:
        timer = PI_TIMER("CubeLayer::OnImGuiRender")
        
        # optFullscreen = True
        # dockspaceFlage = imgui.DOCKNODE_NONE

        # windowFlags = imgui.WINDOW_MENU_BAR | imgui.WINDOW_NO_DOCKING
        # if optFullscreen:
        #     viewport = imgui.get_main_viewport()
        #     imgui.set_next_window_position(*viewport.pos)
        #     imgui.set_next_window_size(*viewport.size)

        #     imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0.0)
        #     imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0.0)

        #     windowFlags |= imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE | \
        #         imgui.WINDOW_NO_MOVE
        #     windowFlags |= imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_NO_NAV_FOCUS

        # if dockspaceFlage & imgui.DOCKNODE_PASSTHRU_CENTRAL_NODE:
        #     windowFlags |= imgui.WINDOW_NO_BACKGROUND

        # imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0.0, 0.0))
        # with imgui.begin("DockSpace Demo", True, windowFlags):
        #     imgui.pop_style_var()

        #     if optFullscreen:
        #         imgui.pop_style_var(2)

        #     io = imgui.get_io()
        #     if io.config_flags & imgui.CONFIG_DOCKING_ENABLE:
        #         dockspaceID = imgui.get_id("Mydockspace")
        #         imgui.dockspace(dockspaceID, (0.0, 0.0), dockspaceFlage)

        #     with imgui.begin_menu_bar():
        #         if imgui.begin_menu("File"):
        #             clicked, state = imgui.menu_item("Quit", "Ctrl+Q", False, True)
        #             imgui.end_menu()

        #     with imgui.begin("Settings"):
        #         mesh: Mesh = self.__AssetManager.Get(self.__Meshes[0])
        #         changed, self.__AutoRotate = imgui.checkbox("Auto Rotate", self.__AutoRotate)
                
        #         imgui.text("\nTransform:")
        #         changed, translation = imgui.drag_float3("Location" , *mesh.Translation , change_speed=0.05 )
        #         changed, scale       = imgui.drag_float3("Scale"    , *mesh.Scale       , change_speed=0.05 )

        #         mesh.SetTranslation(translation)
        #         mesh.SetScale(scale)

        #         changed, rotation = imgui.drag_float3("Rotation", *mesh.Rotation, change_speed=1)
        #         mesh.SetRotation(pyrr.Vector3([ *rotation ]))

        #         if PI_DEBUG:
        #             imgui.text("\nFPS: {}".format(round(self.__Framerate)))
                    
        #             clicked, self.vSync = imgui.checkbox("VSync", self.vSync)

        #             if clicked:
        #                 Input.GetWindow().SetVSync(self.vSync)
        #                 PI_V_SYNC = self.vSync

        with imgui.begin("Settings"):
            mesh: Mesh = self.__AssetManager.Get(self.__Meshes[0])
            changed, self.__AutoRotate = imgui.checkbox("Auto Rotate", self.__AutoRotate)
            
            imgui.text("\nTransform:")
            changed, translation = imgui.drag_float3("Location" , *mesh.Translation , change_speed=0.05 )
            changed, scale       = imgui.drag_float3("Scale"    , *mesh.Scale       , change_speed=0.05 )
            changed, rotation    = imgui.drag_float3("Rotation", *mesh.Rotation, change_speed=1)
            
            mesh.SetTranslation(pyrr.Vector3([ *translation ]))
            mesh.SetScale(pyrr.Vector3([ *scale ]))
            mesh.SetRotation(pyrr.Vector3([ *rotation ]))

            imgui.text("\nLight Transforms")

            changed, lightPos   = imgui.drag_float3("LightLocation" , *self.__Light.Position , change_speed=0.05 )
            changed, lightColor = imgui.color_edit3("LightColor", *self.__Light.Diffuse)

            color = pyrr.Vector3([ *lightColor ])

            self.__Light.SetPosition(pyrr.Vector3([ *lightPos ]))
            self.__Light.SetDiffuse(color)
            self.__Light.SetAmbient(color * 0.15)

            if PI_DEBUG:
                imgui.text("\nFPS: {}".format(round(self.__Framerate)))
                
                clicked, self.vSync = imgui.checkbox("VSync", self.vSync)

                if clicked:
                    Input.GetWindow().SetVSync(self.vSync)
                    PI_V_SYNC = self.vSync

    def OnUpdate(self, timestep: Timestep) -> None:
        timer = PI_TIMER("CubeLayer::OnUpdate")
        self.__Framerate = 1 / timestep.Seconds 
        self.__CameraController.OnUpdate(timestep.Seconds)

        if self.__AutoRotate:
            self.__AssetManager.Get(self.__Meshes[0]).Rotate(degrees([
                0.45 * timestep.Seconds,
                0.5  * timestep.Seconds,
                0.55 * timestep.Seconds
            ]))

        with BeginRenderer(self.__CameraController.Camera, self.__Light):
            for mesh in self.__Meshes:
                mesh = self.__AssetManager.Get(mesh)
                Renderer.SubmitMesh(mesh)
