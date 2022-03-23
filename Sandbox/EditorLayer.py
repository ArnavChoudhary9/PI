# Hackey Fix for relative path problem
# TODO: Try to remove it later
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Main Code starts from here
from Jordan import *

class EditorLayer(Layer):
    __VertexArray : VertexArray
    __Shader      : Shader

    __SquareVA     : VertexArray
    __FlatColorShader : Shader

    __Color : tuple
    __Grid  : tuple

    __Camera: Camera
    
    __CameraMoveSpeed = 3
    __CameraRotationSpeed = 135

    __Framerate: float

    def __init__(self, camera: Camera, name: str="EditorLayer") -> None:
        super().__init__(name)
        self.__Camera = camera

    def OnAttach(self) -> None:
        self.__VertexArray: VertexArray = VertexArray.Create()

        vertices = [
            -0.5, -0.5, 0.001,    0.8, 0.2, 0.8, 1.0,
             0.5, -0.5, 0.001,    0.8, 0.8, 0.2, 1.0,
             0.0,  0.5, 0.001,    0.2, 0.8, 0.8, 1.0
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
            -0.5, -0.5, 0.0,
             0.5, -0.5, 0.0,
             0.5,  0.5, 0.0,
            -0.5,  0.5, 0.0
        ]

        squareVB: VertexBuffer = VertexBuffer.Create(SquareVertices)
        squareVB.SetLayout(BufferLayout(
            ( ShaderDataType.Float3, "a_Position" ),
        ))

        self.__SquareVA.AddVertexBuffer(squareVB)
        self.__SquareVA.SetIndexBuffer(IndexBuffer.Create([ 0, 1, 2, 2, 3, 0 ]))
        self.__SquareVA.Unbind()

        # This is a basic Shader so it is included in Jordan
        self.__Shader: Shader = Shader.Create( ".\Assets\\Shaders\\BasicShader.glsl"     )
        self.__FlatColorShader: Shader = Shader.Create( ".\Assets\\Shaders\\FlatColorShader.glsl" )

        self.__Color = (0.8, 0.2, 0.2)
        self.__Grid = (1, 1)
        self.__Framerate = 60

    def OnImGuiRender(self) -> None:
        imgui.begin("Settings")

        imgui.text("Use arrow keys to move the Camera\nand Right Shift and Right Ctrl to rotate it.")
        imgui.text("\n")

        changed, self.__Color = imgui.color_edit3("SquareColor", *self.__Color)

        imgui.text("\nThe following is the width and height of the grid")
        changed, self.__Grid = imgui.drag_int2(
            "Grid Size", *self.__Grid, change_speed=0.125, min_value=1, max_value=10
        )

        if JD_DEBUG:
            imgui.text("\nTotal draw calls: {}".format(self.__Grid[0]*self.__Grid[1]))
            imgui.text("FPS: {}".format(round(self.__Framerate)))

        imgui.end()

    def OnUpdate(self, timestep) -> None:
        timer = JD_TIMER("EditorLayer::OnUpdate")
        self.__Framerate = 1 / timestep.Seconds

        if (Input.IsKeyPressed(JD_KEY_UP)):
            self.__Camera.SetPosition(
                self.__Camera.Position + pyrr.Vector3([0, self.__CameraMoveSpeed * timestep.Seconds, 0])
            )
        if (Input.IsKeyPressed(JD_KEY_DOWN)):
            self.__Camera.SetPosition(
                self.__Camera.Position - pyrr.Vector3([0, self.__CameraMoveSpeed * timestep.Seconds, 0])
            )

        if (Input.IsKeyPressed(JD_KEY_LEFT)):
            self.__Camera.SetPosition(
                self.__Camera.Position - pyrr.Vector3([self.__CameraMoveSpeed * timestep.Seconds, 0, 0])
            )
        if (Input.IsKeyPressed(JD_KEY_RIGHT)):
            self.__Camera.SetPosition(
                self.__Camera.Position + pyrr.Vector3([self.__CameraMoveSpeed * timestep.Seconds, 0, 0])
            )

        if (Input.IsKeyPressed(JD_KEY_RIGHT_SHIFT)):
            self.__Camera.SetRotation(self.__Camera.Rotation - self.__CameraRotationSpeed * timestep.Seconds)
        if (Input.IsKeyPressed(JD_KEY_RIGHT_CONTROL)):
            self.__Camera.SetRotation(self.__Camera.Rotation + self.__CameraRotationSpeed * timestep.Seconds)

        drawtimer = JD_TIMER("EditorLayer::Draw")
        Renderer.BeginScene(self.__Camera)

        scale = pyrr.matrix44.create_from_scale(pyrr.Vector3([ 0.1, 0.1, 0.1 ]))

        for i in range(self.__Grid[0]):
            for j in range(self.__Grid[1]):
                pos = pyrr.Vector3([ i*0.11, j*0.11, 0 ])
                translation = pyrr.matrix44.create_from_translation(pos)
                transform = scale @ translation

                self.__FlatColorShader.Bind()
                self.__FlatColorShader.UploadUniformFloat3("u_Color", pyrr.Vector3([
                    self.__Color[0], self.__Color[1], self.__Color[2]
                ]))
                
                Renderer.Submit(self.__FlatColorShader, self.__SquareVA, transform)

        # Renderer.Submit(self.__Shader, self.__VertexArray)

        Renderer.EndScene()
