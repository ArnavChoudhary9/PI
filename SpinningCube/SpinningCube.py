# Hackey Fix for relative path problem
# TODO: Try to remove it later
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Main Code starts from here
from PI import *

from time import time

frames = 0

class CubeLayer(Layer):
    __VertexArray : VertexArray
    __Shader      : Shader

    __Translation : tuple
    __Scale       : tuple
    __Rotation    : list
    __AutoRotate  : tuple
    
    __Camera: Camera

    __Framerate: float
    vSync = PI_V_SYNC

    def __init__(self, camera, name: str = "CubeLayer") -> None:
        super().__init__(name=name)
        self.__Camera = camera

    def OnAttach(self) -> None:
        self.__VertexArray: VertexArray = VertexArray.Create()
        
        vertices = [
            #   Locations             Colors
            -0.5, -0.5,  0.5,   0.8, 0.2, 0.2, 1.0,
            -0.5,  0.5,  0.5,   0.2, 0.8, 0.2, 1.0,
            -0.5, -0.5, -0.5,   0.2, 0.2, 0.8, 1.0,
            -0.5,  0.5, -0.5,   0.2, 0.8, 0.8, 1.0,

             0.5, -0.5,  0.5,   0.8, 0.2, 0.8, 1.0,
             0.5,  0.5,  0.5,   0.8, 0.8, 0.2, 1.0,
             0.5, -0.5, -0.5,   0.8, 0.8, 0.8, 1.0,
             0.5,  0.5, -0.5,   0.2, 0.4, 0.6, 1.0
        ]
        
        indices = [
            1, 2, 0,
            3, 6, 2,

            7, 4, 6,
            5, 0, 4,

            6, 0, 2,
            3, 5, 7,

            1, 3, 2,
            3, 7, 6,

            7, 5, 4,
            5, 1, 0,

            6, 4, 0,
            3, 1, 5,
        ]

        vertexBuffer: VertexBuffer = VertexBuffer.Create(vertices)
        vertexBuffer.SetLayout(BufferLayout(
            ( ShaderDataType.Float3, "a_Position" ),
            ( ShaderDataType.Float4, "a_Color"    )
        ))

        self.__VertexArray.AddVertexBuffer(vertexBuffer)
        self.__VertexArray.SetIndexBuffer(IndexBuffer.Create(indices))
        self.__VertexArray.Unbind()

        self.__Translation = ( 0.40,  0.00, -3.00 )
        self.__Scale       = ( 1.00,  1.00,  1.00 )
        self.__Rotation    = [ 0.00,  0.00,  0.00 ]
        self.__AutoRotate  = True
        self.__Framerate   = 60

        self.__Shader: Shader = Shader.Create(".\\Assets\\Shaders\\3DCubeShader.glsl")

    def OnImGuiRender(self) -> None:
        imgui.begin("Settings")

        changed, self.__AutoRotate = imgui.checkbox("Auto Rotate", self.__AutoRotate)
        
        imgui.text("\nTransform:")
        changed, self.__Translation = imgui.drag_float3("Location" , *self.__Translation , change_speed=0.05 )
        changed, self.__Scale       = imgui.drag_float3("Scale"    , *self.__Scale       , change_speed=0.05 )

        if not self.__AutoRotate:
            changed, rotation = imgui.drag_float3("Rotation", *self.__Rotation, change_speed=1)
            self.__Rotation = list(rotation)

        if PI_DEBUG:
            imgui.text("\nFPS: {}".format(round(self.__Framerate)))
            
            clicked, self.vSync = imgui.checkbox("VSync", self.vSync)

            if clicked:
                Input.GetWindow().SetVSync(self.vSync)
                PI_V_SYNC = self.vSync

        imgui.end()

    def OnUpdate(self, timestep) -> None:
        timer = PI_TIMER("CubeLayer::OnUpdate")
        self.__Framerate = 1 / timestep.Seconds 
        
        if self.__AutoRotate:
            self.__Rotation[0] += degrees(0.45 * timestep.Seconds)
            self.__Rotation[1] += degrees(0.5  * timestep.Seconds)
            self.__Rotation[2] += degrees(0.65 * timestep.Seconds)

        self.__Rotation[0] %= 360
        self.__Rotation[1] %= 360
        self.__Rotation[2] %= 360

        rotX = pyrr.Matrix44.from_x_rotation( radians(self.__Rotation[0]) )
        rotY = pyrr.Matrix44.from_y_rotation( radians(self.__Rotation[1]) )
        rotZ = pyrr.Matrix44.from_z_rotation( radians(self.__Rotation[2]) )

        rotation = rotX @ rotY @ rotZ

        translationMatrix = pyrr.matrix44.create_from_translation(pyrr.Vector3([ *self.__Translation ]))
        scaleMatrix = pyrr.matrix44.create_from_scale(pyrr.Vector3([ *self.__Scale ]))

        self.__Shader.Bind()
        self.__Shader.UploadUniformMat4( "u_Translation" , translationMatrix )
        self.__Shader.UploadUniformMat4( "u_Rotation"    , rotation          )
        self.__Shader.UploadUniformMat4( "u_Scale"       , scaleMatrix       )

        Renderer.BeginScene(self.__Camera)
        Renderer.Submit(self.__Shader, self.__VertexArray)
        Renderer.EndScene()

class SpinningCube(PI_Application):
    def __init__(self, name: str, props: WindowProperties=WindowProperties()) -> None:
        super().__init__(name, props=props)
        self._Camera = PerspectiveCamera(45, self._Window.AspectRatio)
        self._LayerStack.PushLayer(CubeLayer(self._Camera))

    def Run(self) -> None:
        global frames
        runTimer = PI_TIMER("Application::Run")

        while (self._Running):
            updateTimer = PI_TIMER("Application::Update")
            super().Run()

            frames += 1

def CreateApp() -> PI_Application:
    return SpinningCube("Spinning Cube", WindowProperties(
        title="Spinning Cube", width=1200, height=600
    ))

App.CreateApplication = CreateApp

start = time()
main()
print("Average FPS: {}".format( frames / (time() - start) ))
