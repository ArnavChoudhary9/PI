from .RenderCommand import *
from .Camera import OrthographicCamera

from .VertexArray import VertexArray
from .Buffer  import *
from .Shader  import *
from .Texture import *

from ..Core import PI_TIMER
from ..Logging.logger import PI_CORE_TRACE

import pyrr
import numpy as np

from math import radians

from contextlib import contextmanager
@contextmanager
def BeginRenderer2D(camera: OrthographicCamera):
    try:
        Renderer2D.BeginScene(camera)
        yield Renderer2D
    finally:
        Renderer2D.EndScene()

class Renderer2D:
    class _Data:
        _QuadVertexArray  : VertexArray
        _QuadVertexBuffer : VertexBuffer
        _TextureShader    : Shader
        _WhiteTexture     : Texture2D

    __slots__ = ("__RendererData",)
    # __RendererData: _Data

    @staticmethod
    def Init() -> None:
        Renderer2D.__RendererData = Renderer2D._Data()

        Renderer2D.__RendererData._QuadVertexArray = VertexArray.Create()
        
        QuadVB: VertexBuffer = VertexBuffer.Create([
        #      Locations        Texture Coord
            -0.5, -0.5, 0.0,      0.0, 0.0,
             0.5, -0.5, 0.0,      1.0, 0.0,
             0.5,  0.5, 0.0,      1.0, 1.0,
            -0.5,  0.5, 0.0,      0.0, 1.0
        ])

        QuadVB.SetLayout(BufferLayout(
            ( ShaderDataType.Float3, "a_Position" ),
            ( ShaderDataType.Float2, "a_TexCoord" )
        ))
        Renderer2D.__RendererData._QuadVertexBuffer = QuadVB

        Renderer2D.__RendererData._QuadVertexArray.AddVertexBuffer(QuadVB)
        Renderer2D.__RendererData._QuadVertexArray.SetIndexBuffer(IndexBuffer.Create([0, 1, 2, 2, 3, 0]))

        Renderer2D.__RendererData._TextureShader = Shader.Create(".\\Assets\\Shaders\\CombinedRenderer2DShader.glsl")

        Renderer2D.__RendererData._WhiteTexture = Texture2D.Create(1, 1)
        Renderer2D.__RendererData._WhiteTexture.SetData(b'\xff\xff\xff\xff', 32)

        RenderCommand.EnableDepth()

    @staticmethod
    def BeginScene(camera: OrthographicCamera) -> None:        
        Renderer2D.__RendererData._TextureShader.Bind()
        Renderer2D.__RendererData._TextureShader.SetMat4("u_ViewProjection", camera.ViewProjectionMatrix)

    @staticmethod
    def EndScene() -> None:
        pass

    # Primitives
    @staticmethod
    def DrawQuad(pos: tuple, size: tuple, rotation: float=0.0,\
        color: tuple=None, texture: Texture=None, tilingFactor: float=1):
        timer = PI_TIMER("Renderer2D::DrawQuad")

        if len(pos) == 2:
            pos = ( *pos, 0.0 )
        pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([ *pos ]))
        size = pyrr.matrix44.create_from_scale(pyrr.Vector3([ *size, 1 ]))

        transform = None
        if rotation != 0.0:
            rotation = pyrr.matrix44.create_from_z_rotation(radians(rotation))
            transform = size @ rotation @ pos
        else:
            transform = size @ pos

        # Renderer2D.__RendererData._TextureShader.Bind()
        Renderer2D.__RendererData._TextureShader.SetMat4("u_Transform", transform)

        Renderer2D.__RendererData._TextureShader.SetFloat("u_TilingFactor", tilingFactor)

        if color is None:
            color = ( 1.0, 1.0, 1.0, 1.0 )
        elif len(color) == 3:
            color = ( *color, 1.0 )
        Renderer2D.__RendererData._TextureShader.SetFloat4("u_Color", pyrr.Vector4([ *color ]))

        if texture is None:
            Renderer2D.__RendererData._WhiteTexture.Bind(0)
        elif texture is not None:
            texture.Bind(0)
        Renderer2D.__RendererData._TextureShader.SetInt("u_Texture", 0)

        Renderer2D.__RendererData._QuadVertexArray.Bind()
        RenderCommand.DrawIndexed(Renderer2D.__RendererData._QuadVertexArray)

        return Renderer2D
