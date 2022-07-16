class PI:
    class State:
        __slots__ = "__CurrentApplication", \
            "__CurrentWindow", "__CurrentNativeWindow"

        class Stats:
            DrawCalls: int = 0

            class Shaders:
                ShadersBinded: int = 0

                class Uniforms:
                    TotalUniforms: int = 0

                    Ints: int = 0
                    Floats: int = 0
                    Vector3: int = 0
                    Vector4: int = 0
                    Matrix_3x3: int = 0
                    Matrix_4x4: int = 0

            @staticmethod
            def Reset() -> None:
                PI.State.Stats.DrawCalls = 0
                PI.State.Stats.Shaders.ShadersBinded = 0

                PI.State.Stats.Shaders.Uniforms.TotalUniforms = 0
                PI.State.Stats.Shaders.Uniforms.Ints = 0
                PI.State.Stats.Shaders.Uniforms.Floats = 0
                PI.State.Stats.Shaders.Uniforms.Vector3 = 0
                PI.State.Stats.Shaders.Uniforms.Vector4 = 0
                PI.State.Stats.Shaders.Uniforms.Matrix_3x3 = 0
                PI.State.Stats.Shaders.Uniforms.Matrix_4x4 = 0

        @staticmethod
        def SetContext(app):
            return (
                PI.State
                    .SetApplication(app)
                    .SetWindow(app.Window)
            ) 

        @staticmethod
        def SetApplication(app):
            PI.State.__CurrentApplication = app
            return PI.State

        @staticmethod
        def GetCurrentApplication():
            return PI.State.__CurrentApplication

        @staticmethod
        def SetWindow(window):
            PI.State.__CurrentWindow = window
            PI.State.__CurrentNativeWindow = window.NativeWindow
            return PI.State

        @staticmethod
        def GetCurrentWindow():
            return PI.State.__CurrentWindow

        @staticmethod
        def GetCurrentNativeWindow():
            return PI.State.__CurrentNativeWindow

StateManager: PI.State = PI.State
