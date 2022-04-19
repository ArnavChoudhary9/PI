from ..Core         import PI_TIMER
from .RendererAPI   import RendererAPI
from .RenderCommand import RenderCommand

import pyrr
from contextlib import contextmanager

@contextmanager
def BeginRenderer(camera):
    try:
        yield Renderer.BeginScene(camera)

    finally:
        Renderer.EndScene()

class Renderer:
    class SceneData:
        ViewProjectionMatrix : pyrr.Matrix44
        CameraPos            : pyrr.Vector3

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

        from .Framebuffer import Framebuffer
        Framebuffer.Init()

        RendererAPI.EnableCulling()

        return Renderer

    @staticmethod
    def BeginScene(camera) -> None:
        Renderer.__CurrentSceneData = Renderer.SceneData()

        Renderer.__CurrentSceneData.ViewProjectionMatrix = camera.ViewProjectionMatrix
        Renderer.__CurrentSceneData.CameraPos            = camera.Position

        return Renderer

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
    def SubmitScene(scene):
        for mesh in scene.Meshes:
            mesh.Bind(
                scene.DirectionalLight,
                scene.PointLights, scene.PointLightLen,
                scene.SpotLights, scene.SpotLightLen,
                Renderer.__CurrentSceneData.CameraPos
            )

            mesh.Material.SetViewProjection(Renderer.__CurrentSceneData.ViewProjectionMatrix)
            RenderCommand.DrawIndexed(mesh.VertexArray)

        return Renderer

    @staticmethod
    def OnResize(width: int, height: int):
        RenderCommand.Resize(0, 0, width, height)
        return Renderer

    @staticmethod
    def GetAPI() -> int:
        return RendererAPI.GetAPI()
