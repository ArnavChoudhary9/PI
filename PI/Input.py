from .logger import PI_CORE_ASSERT
from .Window import OS, Window
from typing  import Tuple

class Input:
    __slots__ = "__NativeClass", "__CurrentWindow", "__CurrentNativeWindow"
    
    @staticmethod
    def Init():
        if Window.GetOS() == OS.Null:
            PI_CORE_ASSERT(False, "OS.Null is yet not supported!")
            Input.__NativeClass = None

        elif Window.GetOS() == OS.Windows:
            from .Platform.Windows import WindowsInput
            Input.__NativeClass = WindowsInput

    @staticmethod
    def SetWindow(window) -> None:
        Input.__CurrentWindow = window
        Input.__CurrentNativeWindow = window.NativeWindow

    @staticmethod
    def GetWindow() -> Window:
        return Input.__CurrentWindow

    @staticmethod
    def GetNativeWindow() -> Window:
        return Input.__CurrentNativeWindow

    @staticmethod
    def IsKeyPressed(keyCode: int) -> bool:
        return Input.__NativeClass.IsKeyPressed(keyCode)
    
    @staticmethod
    def IsMouseButtonPressed(button: int) -> bool:
        return Input.__NativeClass.IsMouseButtonPressed(button)

    @staticmethod
    def GetMouseX() -> float:
        return Input.__NativeClass.GetMouseX()

    @staticmethod
    def GetMouseY() -> float:
        return Input.__NativeClass.GetMouseY()

    @staticmethod
    def GetMousePos() -> Tuple[float, float]:
        return Input.__NativeClass.GetMousePos()
