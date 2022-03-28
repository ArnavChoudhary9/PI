from .ImGuiLayer import *

from contextlib import contextmanager
@contextmanager
def BeginImGui(windowName: str):
    try:
        imgui.begin(windowName)
        yield imgui

    finally:
        imgui.end()

PI_IGL_VERSION: str = "1.2.0"
