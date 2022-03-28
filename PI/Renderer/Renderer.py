from ..Core         import PI_TIMER
from .RendererAPI   import RendererAPI
from .RenderCommand import RenderCommand

import pyrr
from contextlib import contextmanager

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

    __CurrentSceneData: SceneData

    @staticmethod
    def Init() -> None:
        # RendererAPI.Init()
        # RenderCommand.Init()

        # VertexArray.Init()
        # VertexBuffer.Init()
        # IndexBuffer.Init()
        # Shader.Init()
        # Texture.Init()

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
        # endSceneTimer = PI_TIMER("Renderer::EndScene")
        # for shader, objects in Renderer.__CurrentSceneData.RenderQueue.items():
        #     shader.Bind()
        #     shader.UploadUniformMat4("u_ViewProjection", Renderer.__CurrentSceneData.ViewProjectionMatrix)

        #     for vertexArray, transform in objects:
        #         shader.UploadUniformMat4("u_Transform", transform)
        #         vertexArray.Bind()
        #         RenderCommand.DrawIndexed(vertexArray)

        pass


    @staticmethod
    def Submit(shader, vertexArray, transform=pyrr.matrix44.create_identity()) -> None:
        shader.Bind()
        shader.UploadUniformMat4("u_ViewProjection", Renderer.__CurrentSceneData.ViewProjectionMatrix)
        shader.UploadUniformMat4("u_Transform", transform)

        vertexArray.Bind()
        RenderCommand.DrawIndexed(vertexArray)

        # Renderer.__CurrentSceneData.Enqueue(shader, vertexArray, transform)

    @staticmethod
    def GetAPI() -> int:
        return RendererAPI.GetAPI()
