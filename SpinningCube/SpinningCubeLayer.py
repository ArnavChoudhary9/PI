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

        self.__AutoRotate  = True
        self.__Framerate   = 60

    def OnEvent(self, event: Event) -> None:
        self.__CameraController.OnEvent(event)

    def OnImGuiRender(self) -> None:
        timer = PI_TIMER("CubeLayer::OnImGuiRender")
        with imgui.begin("Settings"):
            mesh: Mesh = self.__AssetManager.Get(self.__Meshes[0])
            changed, self.__AutoRotate = imgui.checkbox("Auto Rotate", self.__AutoRotate)
            
            imgui.text("\nTransform:")
            changed, translation = imgui.drag_float3("Location" , *mesh.Translation , change_speed=0.05 )
            changed, scale       = imgui.drag_float3("Scale"    , *mesh.Scale       , change_speed=0.05 )

            mesh.SetTranslation(translation)
            mesh.SetScale(scale)

            changed, rotation = imgui.drag_float3("Rotation", *mesh.Rotation, change_speed=1)
            mesh.SetRotation(pyrr.Vector3([ *rotation ]))

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

        with BeginRenderer(self.__CameraController.Camera):
            for mesh in self.__Meshes:
                mesh = self.__AssetManager.Get(mesh)
                Renderer.SubmitMesh(mesh)
