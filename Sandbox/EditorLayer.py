# Hackey Fix for relative path problem
# TODO: Try to remove it later
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Main Code starts from here
from PI import *

class EditorLayer(Layer):
    __VertexArray : VertexArray
    __SquareVA    : VertexArray

    __AssetManager: AssetManager

    __Color : tuple
    __Grid  : tuple

    __Camera: Camera
    
    __CameraMoveSpeed = 3
    __CameraRotationSpeed = 135

    __Framerate: float
    vSync = PI_V_SYNC

    def __init__(self, camera: Camera, name: str="EditorLayer") -> None:
        super().__init__(name)
        self.__Camera = camera

    def OnAttach(self) -> None:
        self.__VertexArray: VertexArray = VertexArray.Create()
        self.__AssetManager = AssetManager()

        vertices = [
            -0.5, -0.5, 0.0,    0.8, 0.2, 0.8, 1.0,
             0.5, -0.5, 0.0,    0.8, 0.8, 0.2, 1.0,
             0.0,  0.5, 0.0,    0.2, 0.8, 0.8, 1.0
        ]               # The Z is 0.001 because GL_DEPTH_TEST is enabled

        vertexBuffer: VertexBuffer = VertexBuffer.Create(vertices)
        vertexBuffer.SetLayout(BufferLayout(
            ( ShaderDataType.Float3, "a_Position" ),
            ( ShaderDataType.Float4, "a_Color" ),
        ))

        self.__VertexArray.AddVertexBuffer(vertexBuffer)
        self.__VertexArray.SetIndexBuffer(IndexBuffer.Create([ 0, 1, 2 ]))
        self.__VertexArray.Unbind()

        self.__SquareVA: VertexArray = VertexArray.Create()
        self.__SquareVA.Bind()

        SquareVertices = [
        #      Locations        Texture Coord
            -0.5, -0.5, 0.0,      0.0, 0.0,
             0.5, -0.5, 0.0,      1.0, 0.0,
             0.5,  0.5, 0.0,      1.0, 1.0,
            -0.5,  0.5, 0.0,      0.0, 1.0
        ]

        squareVB: VertexBuffer = VertexBuffer.Create(SquareVertices)
        squareVB.SetLayout(BufferLayout(
            ( ShaderDataType.Float3, "a_Position" ),
            ( ShaderDataType.Float2, "a_TexCoord" )
        ))

        self.__SquareVA.AddVertexBuffer(squareVB)
        self.__SquareVA.SetIndexBuffer(IndexBuffer.Create([ 0, 1, 2, 2, 3, 0 ]))
        self.__SquareVA.Unbind()

        self.__AssetManager.Load(AssetManager.AssetType.ShaderAsset, ".\\Assets\\Shaders\\BasicShader.glsl")
        self.__AssetManager.Load(AssetManager.AssetType.ShaderAsset, ".\\Assets\\Shaders\\FlatColorShader.glsl")

        texShader: Shader = self.__AssetManager.Load(AssetManager.AssetType.ShaderAsset, ".\\Assets\\Shaders\\TextureShader.glsl")
        texture: Texture2D = self.__AssetManager.Load(AssetManager.AssetType.Texture2DAsset, ".\\Assets\\Images\\Logo_Transperent.png")

        texture.Bind()
        texShader.Bind()
        texShader.UploadUniformInt("u_Texture", 0)

        self.__Color = (0.8, 0.2, 0.2)
        self.__Grid = (1, 1)
        self.__Framerate = 60

    def OnEvent(self, event: Event) -> None:
        event.Handled = EventDispatcher(event).Dispach(
            lambda event: self.__Camera.SetScale( self.__Camera.Scale - (event.OffsetY * 0.05) + 0.001 ),
            EventType.MouseScrolled
        )
        
        self.__CameraMoveSpeed = self.__Camera.Scale * 1.25

    def OnImGuiRender(self) -> None:
        with BeginImGui("Settings"):
            imgui.text("Use arrow keys to move the Camera\nand Right Shift and Right Ctrl to rotate it.")
            imgui.text("\n")

            changed, self.__Color = imgui.color_edit3("SquareColor", *self.__Color)

            imgui.text("\nThe following is the width and height of the grid")
            changed, self.__Grid = imgui.drag_int2(
                "Grid Size", *self.__Grid, change_speed=0.125, min_value=1, max_value=10
            )

            if PI_DEBUG:
                imgui.text("\nTotal draw calls: {}".format(self.__Grid[0]*self.__Grid[1] + 1))
                imgui.text("FPS: {}".format(round(self.__Framerate)))
                
                imgui.text("\n")

                clicked, self.vSync = imgui.checkbox("VSync", self.vSync)

                if clicked:
                    Input.GetWindow().SetVSync(self.vSync)
                    PI_V_SYNC = self.vSync

    def OnUpdate(self, timestep) -> None:
        timer = PI_TIMER("EditorLayer::OnUpdate")
        self.__Framerate = 1 / timestep.Seconds

        if (Input.IsKeyPressed(PI_KEY_W)):
            self.__Camera.SetPosition(
                self.__Camera.Position + pyrr.Vector3([0, self.__CameraMoveSpeed * timestep.Seconds, 0])
            )
        if (Input.IsKeyPressed(PI_KEY_S)):
            self.__Camera.SetPosition(
                self.__Camera.Position - pyrr.Vector3([0, self.__CameraMoveSpeed * timestep.Seconds, 0])
            )

        if (Input.IsKeyPressed(PI_KEY_A)):
            self.__Camera.SetPosition(
                self.__Camera.Position - pyrr.Vector3([self.__CameraMoveSpeed * timestep.Seconds, 0, 0])
            )
        if (Input.IsKeyPressed(PI_KEY_D)):
            self.__Camera.SetPosition(
                self.__Camera.Position + pyrr.Vector3([self.__CameraMoveSpeed * timestep.Seconds, 0, 0])
            )

        if (Input.IsKeyPressed(PI_KEY_Q)):
            self.__Camera.SetRotation(self.__Camera.Rotation - self.__CameraRotationSpeed * timestep.Seconds)
        if (Input.IsKeyPressed(PI_KEY_E)):
            self.__Camera.SetRotation(self.__Camera.Rotation + self.__CameraRotationSpeed * timestep.Seconds)

        drawtimer = PI_TIMER("EditorLayer::Draw")
        with BeginRenderer(self.__Camera):
            scale = pyrr.matrix44.create_from_scale(pyrr.Vector3([ 0.1, 0.1, 0.1 ]))
            self.__AssetManager.Get("FlatColorShader").Bind()

            self.__AssetManager.Get("FlatColorShader") \
                .UploadUniformFloat3("u_Color", pyrr.Vector3([ *self.__Color ]))

            for i in range(self.__Grid[0]):
                for j in range(self.__Grid[1]):
                    pos = pyrr.Vector3([ i*0.11, j*0.11, 0 ])
                    translation = pyrr.matrix44.create_from_translation(pos)
                    transform = scale @ translation
                    
                    Renderer.Submit(self.__AssetManager.Get("FlatColorShader"), self.__SquareVA, transform)
            
            scale = pyrr.matrix44.create_from_scale(pyrr.Vector3([ 1, 1, 1 ]))
            translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([ -0.75, 0.5*(1 / 1.1), 0 ]))
            transform = scale @ translation

            Renderer.Submit(self.__AssetManager.Get("TextureShader"), self.__SquareVA, transform)
            # Renderer.Submit(self.__Shader, self.__VertexArray)
