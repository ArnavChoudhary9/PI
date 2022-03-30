from ..Core   import PI_IMGUI_DOCKING
from ..Layers import Layer
from ..Input  import Input

# from ..
from  imgui.integrations.glfw   import *
import imgui

class ImGuiLayer(Layer):
    __Time: float
    __Renderer = None

    def __init__(self, name: str="ImGuiLayer") -> None:
        super().__init__(name=name)
        self.__Time = 0.0

    def OnAttach(self) -> None:
        imgui.create_context()
        io = imgui.get_io()

        io.config_flags |= imgui.CONFIG_NAV_ENABLE_KEYBOARD

        if PI_IMGUI_DOCKING:
            io.config_flags |= imgui.CONFIG_DOCKING_ENABLE
            io.config_flags |= imgui.CONFIG_VIEWEPORTS_ENABLE

        imgui.style_colors_dark()

        if PI_IMGUI_DOCKING:
            style = imgui.get_style()
            if io.config_flags & imgui.CONFIG_VIEWEPORTS_ENABLE:
                style.window_rounding = 0.0
                # style.colors[imgui.COLOR_WINDOW_BACKGROUND].w = 1.0

        window = Input.GetNativeWindow()
        self.__Renderer = GlfwRenderer(window)        

    def OnDetach(self) -> None:
        self.__Renderer.shutdown()

    def OnImGuiRender(self) -> None:
        imgui.show_demo_window(True)

    def Begin(self) -> None:
        self.__Renderer.process_inputs()
        imgui.new_frame()

    def End(self) -> None:
        imgui.render()
        self.__Renderer.render(imgui.get_draw_data())

        if PI_IMGUI_DOCKING:
            io = imgui.get_io()
            if io.config_flags & imgui.CONFIG_VIEWEPORTS_ENABLE:
                backupCurrentContext = glfw.get_current_context()
                imgui.update_platform_windows()
                imgui.render_platform_windows_default()
                glfw.make_context_current(backupCurrentContext)
