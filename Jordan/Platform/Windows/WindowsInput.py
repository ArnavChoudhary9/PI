from ...Input import Input
from typing import Tuple
import glfw

class WindowsInput(Input):
    @staticmethod
    def IsKeyPressed(keyCode: int) -> bool:
        state = glfw.get_key(Input.GetWindow(), WindowsInput.JD_KC_To_GLFW_KC(keyCode))
        return (state == glfw.PRESS or state == glfw.REPEAT)
        
    @staticmethod
    def IsMouseButtonPressed(button: int) -> bool:
        state = glfw.get_mouse_button(Input.GetWindow(), WindowsInput.JD_MBC_To_GLFW_MBC(button))
        return (state == glfw.PRESS)

    @staticmethod
    def GetMouseX() -> float:
        return glfw.get_cursor_pos(Input.GetWindow())[0]

    @staticmethod
    def GetMouseY() -> float:
        return glfw.get_cursor_pos(Input.GetWindow())[1]

    @staticmethod
    def GetMousePos() -> Tuple[float, float]:
        return glfw.get_cursor_pos(Input.GetWindow())

    @staticmethod
    def JD_KC_To_GLFW_KC(keyCode: int) -> int:
        return keyCode

    @staticmethod
    def JD_MBC_To_GLFW_MBC(button: int) -> int:
        return button
