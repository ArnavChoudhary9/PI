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

    __Framerate: float
    vSync = PI_V_SYNC

    def __init__(self, camera: OrthographicCamera, name: str="Sandbox2DLayer") -> None:
        super().__init__(name)
        self.__Camera = camera
        self.__CameraController = OrthogrphicCameraController(camera)

    def OnAttach(self) -> None:
        self.__AssetManager = AssetManager()

        self.__AssetManager.Load(AssetManager.AssetType.Texture2DAsset, ".\\Assets\\Images\\Logo_Transperent.png")
        self.__AssetManager.Load(AssetManager.AssetType.Texture2DAsset, ".\\Assets\\Images\\Logo_HotShot.png")

        self.__Color = (0.8, 0.2, 0.2)
        self.__Framerate = 60

    def OnImGuiRender(self) -> None:
        with imgui.begin("Settings"):
            changed, self.__Color = imgui.color_edit3("SquareColor", *self.__Color)

            if PI_DEBUG:
                imgui.text("FPS: {}".format(round(self.__Framerate)))
                
                imgui.text("\n")

                clicked, self.vSync = imgui.checkbox("VSync", self.vSync)

                if clicked:
                    Input.GetWindow().SetVSync(self.vSync)
                    PI_V_SYNC = self.vSync

    def OnEvent(self, event: Event) -> None:
        self.__CameraController.OnEvent(event)

    def OnUpdate(self, timestep) -> None:
        timer = PI_TIMER("EditorLayer::OnUpdate")
        self.__Framerate = 1 / timestep.Seconds
        self.__CameraController.OnUpdate(timestep.Seconds)

        drawtimer = PI_TIMER("EditorLayer::Draw")        
        with BeginRenderer2D(self.__Camera):
            Renderer2D.DrawQuad(
                pos   = ( 0.0, 0.0, -0.1 ),
                size  = ( 7.5, 7.5 ),
                color = ( 0.25, 0.25, 0.25 ),
                texture = self.__AssetManager.Get("Logo_HotShot"),
                tilingFactor = 35.0
            )

            Renderer2D.DrawQuad(
                pos   = ( -0.5, 0.0 ),
                size  = ( 0.5, 0.5 ),
                color = self.__Color 
            )
            
            color = 1-self.__Color[0], 1-self.__Color[1], 1-self.__Color[2]      # Inverse of self.__Color
            Renderer2D.DrawQuad(
                pos   = ( 0.5, -0.5 ),
                size  = ( 0.5, 0.75 ),
                rotation = 30,
                color = color 
            )

            Renderer2D.DrawQuad(
                pos   = ( 0.75, 0.65 ),
                size  = ( 0.75, 0.75 ),
                texture = self.__AssetManager.Get("Logo_Transperent")
            )
