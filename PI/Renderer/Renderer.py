from ..Core         import PI_TIMER
from .RendererAPI   import RendererAPI
from .RenderCommand import RenderCommand

import pyrr
from contextlib import contextmanager
from multipledispatch import dispatch

@contextmanager
def BeginRenderer(camera):
    try:
        Renderer.BeginScene(camera)
        yield Renderer

    finally:
        Renderer.EndScene()

class Renderer:
    class SceneData:
        ViewProjectionMatrix: pyrr.Matrix44
        RenderQueue: dict = {}

        def Enqueue(self, shader, vertexArray, transform) -> None:
            if (self.RenderQueue.get(shader, False)):
                self.RenderQueue[shader].append( (vertexArray, transform) )
            else:
                self.RenderQueue[shader] = [ (vertexArray, transform) ]

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
    def BeginScene(camera) -> None:
        Renderer.__CurrentSceneData = Renderer.SceneData()
        Renderer.__CurrentSceneData.ViewProjectionMatrix = camera.ViewProjectionMatrix

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
        mesh.Bind()
        mesh.Material.SetViewProjection(Renderer.__CurrentSceneData.ViewProjectionMatrix)
        RenderCommand.DrawIndexed(mesh.VertexArray)

    @staticmethod
    def OnResize(width: int, height: int) -> None:
        RenderCommand.Resize(0, 0, width, height)

    @staticmethod
    def GetAPI() -> int:
        return RendererAPI.GetAPI()
