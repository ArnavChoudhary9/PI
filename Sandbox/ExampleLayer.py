# Hackey Fix for relative path problem
# TODO: Try to remove it later
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Main Code starts from here
from PI import *

class ExampleLayer(Layer):
    __AssetManager: AssetManager

    __Color : tuple
    __Grid  : tuple

    __CameraController: CameraController

    __Framerate: float
    vSync = PI_V_SYNC

    def __init__(self, name: str="ExampleLayer") -> None:
        super().__init__(name)
        self.__CameraController = OrthogrphicCameraController(OrthographicCamera(Input.GetWindow().AspectRatio))

    def OnAttach(self) -> None:
        self.__AssetManager = AssetManager()
        
        self.__AssetManager.Load(
            AssetManager.AssetType.Texture2DAsset,
            ".\\Assets\\Images\\Logo_Transperent.png"
        )

        self.__Color = ( 0.8, 0.2, 0.2 )
        self.__Grid = ( 1, 1 )
        self.__Framerate = 60

    def OnEvent(self, event: Event) -> None:
        self.__CameraController.OnEvent(event)

    def OnImGuiRender(self) -> None:
        with imgui.begin("Settings"):
            imgui.text("Use WASD to move the Camera\nand Q & E to rotate it.")
            imgui.text("\n")

            changed, self.__Color = imgui.color_edit3("SquareColor", *self.__Color)

            imgui.text("\nThe following is the width and height of the grid")
            changed, self.__Grid = imgui.drag_int2(
                "Grid Size", *self.__Grid, change_speed=0.125, min_value=1, max_value=10
            )

            if PI_DEBUG:
                imgui.text("FPS: {}".format(round(self.__Framerate)))
                imgui.text("\n")

                clicked, self.vSync = imgui.checkbox("VSync", self.vSync)

                if clicked:
                    Input.GetWindow().SetVSync(self.vSync)
                    PI_V_SYNC = self.vSync

    def OnUpdate(self, timestep) -> None:
        timer = PI_TIMER("EditorLayer::OnUpdate")
        self.__Framerate = 1 / timestep.Seconds
        self.__CameraController.OnUpdate(timestep.Seconds)

        drawtimer = PI_TIMER("EditorLayer::Draw")
        with BeginRenderer2D(self.__CameraController.Camera):
            for i in range(self.__Grid[0]):
                for j in range(self.__Grid[1]):
                    Renderer2D.DrawQuad(
                        pos  = ( i*0.11, j*0.11 ),
                        size = ( 0.1, 0.1 ),
                        color = self.__Color
                    )

            Renderer2D.DrawQuad(
                pos  = ( -0.75, 0.5*(1 / 1.1) ),
                size = ( 1, 1 ),
                texture = self.__AssetManager.Get("Logo_Transperent")
            )
