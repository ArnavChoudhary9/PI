# Texture and image formats
from OpenGL.GL import \
    GL_RGB, GL_RGB8, GL_RGBA, GL_RGBA8, \
    GL_DEPTH24_STENCIL8, GL_DEPTH_STENCIL, GL_UNSIGNED_INT_24_8

class PIConstants:
    @staticmethod
    def ToOpenGLConstant(constant: int) -> int:
        return constant

    RGB, RGB8, RGBA, RGBA8 = GL_RGB, GL_RGB8, GL_RGBA, GL_RGBA8
    
    DEPTH24_STENCIL8, DEPTH_STENCIL, UNSIGNED_INT_24_8 = \
        GL_DEPTH24_STENCIL8, GL_DEPTH_STENCIL, GL_UNSIGNED_INT_24_8 
