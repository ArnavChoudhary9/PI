from ..Core         import PI_TIMER
from .RendererAPI   import RendererAPI
from .RenderCommand import RenderCommand

import pyrr
from contextlib import contextmanager

@contextmanager
def BeginRenderer(camera, light):
    try:
        Renderer.BeginScene(camera, light)
        yield Renderer

    finally:
        Renderer.EndScene()

class Renderer:
    class SceneData:
        ViewProjectionMatrix : pyrr.Matrix44
        CameraPos            : pyrr.Vector3

        Light = None

    __slots__ = ("__CurrentSceneData",)

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

    @staticmethod
    def BeginScene(camera, light) -> None:
        Renderer.__CurrentSceneData = Renderer.SceneData()

        Renderer.__CurrentSceneData.ViewProjectionMatrix = camera.ViewProjectionMatrix
        Renderer.__CurrentSceneData.CameraPos            = camera.Position

        Renderer.__CurrentSceneData.Light = light

    @staticmethod
    def EndScene() -> None:
        pass

    @staticmethod
    def Submit(shader, vertexArray, transform=pyrr.matrix44.create_identity()) -> None:
        shader.Bind()
        shader.SetMat4("u_ViewProjection", Renderer.__CurrentSceneData.ViewProjectionMatrix)
        shader.SetMat4("u_Transform", transform)

        vertexArray.Bind()
        RenderCommand.DrawIndexed(vertexArray)

    @staticmethod
    def SubmitMesh(mesh) -> None:
        mesh.Bind(
            Renderer.__CurrentSceneData.Light,
            Renderer.__CurrentSceneData.CameraPos
        )
        
        mesh.Material.SetViewProjection(Renderer.__CurrentSceneData.ViewProjectionMatrix)
        
        RenderCommand.DrawIndexed(mesh.VertexArray)

    @staticmethod
    def OnResize(width: int, height: int) -> None:
        RenderCommand.Resize(0, 0, width, height)

    @staticmethod
    def GetAPI() -> int:
        return RendererAPI.GetAPI()
