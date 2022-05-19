from ...Core.Input import Input
from ...Core.StateManager import PI
from typing import Tuple
import glfw

class WindowsInput(Input):
    @staticmethod
    def IsKeyPressed(keyCode: int) -> bool:
        state = glfw.get_key(PI.State.GetCurrentNativeWindow(), WindowsInput.PI_KC_To_GLFW_KC(keyCode))
        return (state == glfw.PRESS or state == glfw.REPEAT)
        
    @staticmethod
    def IsMouseButtonPressed(button: int) -> bool:
        state = glfw.get_mouse_button(PI.State.GetCurrentNativeWindow(), WindowsInput.PI_MBC_To_GLFW_MBC(button))
        return (state == glfw.PRESS)

    @staticmethod
    def GetMouseX() -> float:
        return glfw.get_cursor_pos(PI.State.GetCurrentNativeWindow())[0]

    @staticmethod
    def GetMouseY() -> float:
        return glfw.get_cursor_pos(PI.State.GetCurrentNativeWindow())[1]

    @staticmethod
    def GetMousePos() -> Tuple[float, float]:
        return glfw.get_cursor_pos(PI.State.GetCurrentNativeWindow())

    @staticmethod
    def PI_KC_To_GLFW_KC(keyCode: int) -> int:
        return keyCode

    @staticmethod
    def PI_MBC_To_GLFW_MBC(button: int) -> int:
        return button
