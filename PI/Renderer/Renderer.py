from ..Logging      import PI_CORE_ASSERT
from ..Core         import PI_TIMER, PI_DEBUG
from ..Core.StateManager import StateManager
from .RendererAPI   import RendererAPI
from .RenderCommand import RenderCommand

import pyrr

class Renderer:
    class SceneData:
        Scene                = None
        ViewProjectionMatrix : pyrr.Matrix44
        CameraPos            : pyrr.Vector3

    __slots__ = "__CurrentSceneData", "LineShader", "CAM_COMP"

    @staticmethod
    def Init() -> None:
        RendererAPI.Init()
        RenderCommand.Init()

        from .VertexArray import VertexArray
        VertexArray.Init()

        from .Buffer import VertexBuffer, IndexBuffer
        VertexBuffer.Init()
        IndexBuffer.Init()

        from .Shader import Shader
        Shader.Init()

        from .Texture import Texture
        Texture.Init()

        from .Framebuffer import Framebuffer
        Framebuffer.Init()

        RendererAPI.EnableCulling()

        from ..Scene.Components import CameraComponent
        Renderer.CAM_COMP = CameraComponent

        return Renderer

    @staticmethod
    def BeginScene(scene, camera=None):
        Renderer.__CurrentSceneData = Renderer.SceneData()
        if PI_DEBUG: StateManager.Stats.Reset()

        if camera is None:
            camera = scene.PrimaryCameraEntity
            if camera is None: PI_CORE_ASSERT(False, "There is no camera to render.")
            
            camera = camera.GetComponent(Renderer.CAM_COMP).Camera.CameraObject

        Renderer.__CurrentSceneData.ViewProjectionMatrix = camera.ViewProjectionMatrix
        Renderer.__CurrentSceneData.CameraPos            = camera.Position
        Renderer.__CurrentSceneData.Scene                = scene

        Renderer.LineShader.Bind()
        Renderer.LineShader.SetMat4("u_ViewProjection", Renderer.__CurrentSceneData.ViewProjectionMatrix)

        return _BeginEndRenderer.__new__(_BeginEndRenderer)

    @staticmethod
    def EndScene():
        return Renderer

    @staticmethod
    def Submit(shader, vertexArray, transform=pyrr.matrix44.create_identity()):
        shader.Bind()
        shader.SetMat4("u_ViewProjection", Renderer.__CurrentSceneData.ViewProjectionMatrix)
        shader.SetMat4("u_Transform", transform)

        vertexArray.Bind()
        RenderCommand.DrawIndexed(vertexArray)
        
        return Renderer

    @staticmethod
    def DrawLines(p0: pyrr.Vector3, p1: pyrr.Vector3,
        color: pyrr.Vector4=pyrr.Vector4([1, 1, 1, 1])) -> None:
        Renderer.LineShader.Bind()

        from . import VertexArray, VertexBuffer, BufferLayout, ShaderDataType

        vertexArray  : VertexArray  = VertexArray.Create()
        vertexArray.Bind()

        vertexBuffer : VertexBuffer = VertexBuffer.Create([ *p0, *p1 ])

        vertexBuffer.SetLayout(BufferLayout(
            ( ShaderDataType.Float3, "a_Position" )
        ))

        vertexArray.AddVertexBuffer(vertexBuffer)

        Renderer.LineShader.SetFloat4("u_Color", color)

        RenderCommand.DrawLines(vertexArray, 2)

        return Renderer

    @staticmethod
    def DrawRect(transform: pyrr.Matrix44, color: pyrr.Vector4=pyrr.Vector4([1, 1, 1, 1])) -> None:
        quad = [
            pyrr.Vector4([ -0.5, -0.5, 0.0, 1.0 ]),
            pyrr.Vector4([  0.5, -0.5, 0.0, 1.0 ]),
            pyrr.Vector4([  0.5,  0.5, 0.0, 1.0 ]),
            pyrr.Vector4([ -0.5,  0.5, 0.0, 1.0 ]),
        ]

        rect = [vertex @ transform for vertex in quad]

        Renderer.DrawLines(rect[0], rect[1], color=color)
        Renderer.DrawLines(rect[1], rect[2], color=color)
        Renderer.DrawLines(rect[2], rect[3], color=color)
        Renderer.DrawLines(rect[3], rect[0], color=color)

    @staticmethod
    def DrawScene():
        if Renderer.__CurrentSceneData.Scene is None: return Renderer
        Renderer.__CurrentSceneData.Scene.Draw()
        return Renderer

    @staticmethod
    def OnResize(width: int, height: int):
        RenderCommand.Resize(0, 0, width, height)
        return Renderer

    @staticmethod
    def GetAPI() -> int:
        return RendererAPI.GetAPI()

class _BeginEndRenderer:
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_value, traceback): Renderer.EndScene()
