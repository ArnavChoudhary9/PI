class PI:
    class State:
        __slots__ = "__CurrentApplication", \
            "__CurrentWindow", "__CurrentNativeWindow"

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
