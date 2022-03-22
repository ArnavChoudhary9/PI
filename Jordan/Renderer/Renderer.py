from ..Core         import JD_TIMER
from .RendererAPI   import RendererAPI
from .RenderCommand import RenderCommand

import pyrr

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
    def BeginScene(camera) -> None:
        Renderer.__CurrentSceneData = Renderer.SceneData()
        Renderer.__CurrentSceneData.ViewProjectionMatrix = camera.ViewProjectionMatrix

    @staticmethod
    def EndScene() -> None:
        # endSceneTimer = JD_TIMER("Renderer::EndScene")
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
