# Hackey Fix for relative path problem
# TODO: Try to remove it later
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Main Code starts from here
from PI import *

class Sandbox2D(Layer):
    __AssetManager : AssetManager

    __Color : tuple
    __Camera: Camera
    __CameraController: OrthogrphicCameraController

    __LogoT : UUID
    __Logo  : UUID

    __Framerate: float
    vSync = PI_V_SYNC

    def __init__(self, name: str="Sandbox2DLayer") -> None:
        super().__init__(name)
        self.__Camera = OrthographicCamera(StateManager.GetCurrentWindow().AspectRatio)
        self.__Camera.SetPosition(pyrr.Vector3([ 0.0, 0.0, 0.1]))
        self.__CameraController = OrthogrphicCameraController(self.__Camera)

    def OnAttach(self) -> None:
        self.__AssetManager = AssetManager()

        self.__LogoT = self.__AssetManager.Load(
            AssetManager.AssetType.Texture2DAsset, ".\\InternalAssets\\Images\\Logo_Transperent.png"
        )
        self.__Logo  = self.__AssetManager.Load(
            AssetManager.AssetType.Texture2DAsset, ".\\InternalAssets\\Images\\Logo_HotShot.png"
        )

        self.__Color = (0.8, 0.2, 0.2)
        self.__Framerate = 60

    def OnImGuiRender(self) -> None:
        with imgui.begin("Settings"):
            changed, self.__Color = imgui.color_edit3("SquareColor", *self.__Color)

            if PI_DEBUG:
                imgui.text("\n")
                clicked, self.vSync = imgui.checkbox("VSync", self.vSync)
                imgui.text("FPS: {}".format(round(self.__Framerate)))

                if clicked:
                    StateManager.GetCurrentWindow().SetVSync(self.vSync)
                    PI_V_SYNC = self.vSync

    def OnEvent(self, event: Event) -> None:
        self.__CameraController.OnEvent(event)

    def OnUpdate(self, timestep) -> None:
        timer = PI_TIMER("EditorLayer::OnUpdate")
        self.__Framerate = 1 / timestep.Seconds
        self.__CameraController.OnUpdate(timestep.Seconds)

        drawtimer = PI_TIMER("EditorLayer::Draw")        
        with BeginRenderer2D(self.__Camera):
            inverseColor = 1-self.__Color[0], 1-self.__Color[1], 1-self.__Color[2] # Inverse of self.__Color

            # Verb driven API
            (
                Renderer2D
                
                .DrawQuad (
                    pos   = ( 0.0, 0.0, -0.1 ),
                    size  = ( 6.0, 6.0 ),
                    color = ( 0.25, 0.25, 0.25 ),
                    texture = self.__AssetManager.Get(self.__Logo),
                    tilingFactor = 30.0
                )

                .DrawQuad (
                    pos   = ( -0.5, 0.0 ),
                    size  = ( 0.5, 0.5 ),
                    color = self.__Color 
                )

                .DrawQuad (
                    pos   = ( 0.5, -0.5 ),
                    size  = ( 0.5, 0.75 ),
                    rotation = 30,
                    color = inverseColor 
                )
                
                .DrawQuad (
                    pos   = ( 0.75, 0.65 ),
                    size  = ( 0.75, 0.75 ),
                    texture = self.__AssetManager.Get(self.__LogoT)
                )
            )
