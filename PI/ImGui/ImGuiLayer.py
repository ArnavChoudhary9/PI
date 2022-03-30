from ..Core   import PI_IMGUI_DOCKING
from ..Events import Event, EventDispatcher, EventCategory, EventType
from ..Layers import Layer
from ..Input  import Input
from ..KeyCodes import *

from imgui.integrations.glfw import *
import imgui

class ImGuiLayer(Layer):
    __slots__ = "__Time", "__Renderer", "__io", "__BlockEvents"

    def __init__(self, name: str="ImGuiLayer") -> None:
        super().__init__(name=name)
        self.__Time = 0.0
        self.__BlockEvents = False

    def OnAttach(self) -> None:
        imgui.create_context()
        io = imgui.get_io()
        self.__io = io

        io.config_flags |= imgui.CONFIG_NAV_ENABLE_KEYBOARD

        if PI_IMGUI_DOCKING:
            io.config_flags |= imgui.CONFIG_DOCKING_ENABLE
            io.config_flags |= imgui.CONFIG_VIEWEPORTS_ENABLE

        io.fonts.add_font_from_file_ttf(".\\Assets\\Fonts\\opensans\\OpenSans-Regular.ttf", 18.0)
        # io.fonts_default = io.fonts.add_font_from_file_ttf(".\\Assets\\Fonts\\opensans\\OpenSans-Regular.ttf", 18.0)

        imgui.style_colors_dark()

        if PI_IMGUI_DOCKING:
            style = imgui.get_style()
            if io.config_flags & imgui.CONFIG_VIEWEPORTS_ENABLE:
                style.window_rounding = 0.0
                # style.colors[imgui.COLOR_WINDOW_BACKGROUND].w = 1.0

        window = Input.GetNativeWindow()
        self.__Renderer = GlfwRenderer(window, False)        

    def OnDetach(self) -> None:
        self.__Renderer.shutdown()

    #-----------------EVENTS-----------------
    def OnEvent(self, event: Event) -> None:
        dispatcher = EventDispatcher(event)

        dispatcher.Dispach ( self.__KeyboardPressCallback    , EventType.KeyPressed    )
        dispatcher.Dispach ( self.__KeyboardReleasedCallback , EventType.KeyReleased   )
        dispatcher.Dispach ( self.__CharInputCallback        , EventType.CharInput     )
        dispatcher.Dispach ( self.__WindowResizeCallback     , EventType.WindowResize  )
        dispatcher.Dispach ( self.__MouseScrollCallback      , EventType.MouseScrolled )

        if self.__BlockEvents:
            event.Handled |= bool( event.IsInCategory(EventCategory.Mouse) & self.__io.want_capture_mouse )
            event.Handled |= bool( event.IsInCategory(EventCategory.Keyboard) & self.__io.want_capture_keyboard )
            return

        event.Handled = False        

    def __KeyboardPressCallback(self, event: Event) -> None:
        io = self.__io

        io.keys_down[event.KeyCode] = True

        Input.IsKeyPressed(PI_KEY_LEFT_CONTROL)
        io.key_ctrl = (
            io.keys_down[ Input.IsKeyPressed(PI_KEY_LEFT_CONTROL) ] or
            io.keys_down[ Input.IsKeyPressed(PI_KEY_RIGHT_CONTROL) ]
        )

        io.key_alt = (
            io.keys_down[ Input.IsKeyPressed(PI_KEY_LEFT_ALT) ] or
            io.keys_down[ Input.IsKeyPressed(PI_KEY_RIGHT_ALT) ]
        )

        io.key_shift = (
            io.keys_down[ Input.IsKeyPressed(PI_KEY_LEFT_SHIFT) ] or
            io.keys_down[ Input.IsKeyPressed(PI_KEY_RIGHT_SHIFT) ]
        )

        io.key_super = (
            io.keys_down[ Input.IsKeyPressed(PI_KEY_LEFT_SUPER) ] or
            io.keys_down[ Input.IsKeyPressed(PI_KEY_RIGHT_SUPER) ]
        )

        if self.__BlockEvents: return True
        return False

    def __KeyboardReleasedCallback(self, event: Event) -> None:
        io = self.__io

        io.keys_down[event.KeyCode] = False

        Input.IsKeyPressed(PI_KEY_LEFT_CONTROL)
        io.key_ctrl = (
            io.keys_down[ Input.IsKeyPressed(PI_KEY_LEFT_CONTROL) ] or
            io.keys_down[ Input.IsKeyPressed(PI_KEY_RIGHT_CONTROL) ]
        )

        io.key_alt = (
            io.keys_down[ Input.IsKeyPressed(PI_KEY_LEFT_ALT) ] or
            io.keys_down[ Input.IsKeyPressed(PI_KEY_RIGHT_ALT) ]
        )

        io.key_shift = (
            io.keys_down[ Input.IsKeyPressed(PI_KEY_LEFT_SHIFT) ] or
            io.keys_down[ Input.IsKeyPressed(PI_KEY_RIGHT_SHIFT) ]
        )

        io.key_super = (
            io.keys_down[ Input.IsKeyPressed(PI_KEY_LEFT_SUPER) ] or
            io.keys_down[ Input.IsKeyPressed(PI_KEY_RIGHT_SUPER) ]
        )

        if self.__BlockEvents: return True
        return False

    def __CharInputCallback(self, e: Event) -> None:
        io = self.__io

        if 0 < e.Char < 0x10000:
            io.add_input_character(e.Char)
            if self.__BlockEvents: return True

        return False

    def __WindowResizeCallback(self, e: Event) -> None:
        self.__io.display_size = e.Width, e.Height

        if self.__BlockEvents: return True
        return False

    def __MouseScrollCallback(self, e: Event) -> None:
        self.__io.mouse_wheel_horizontal = e.OffsetX
        self.__io.mouse_wheel = e.OffsetY
        
        if self.__BlockEvents: return True
        return False
    #----------------------------------------

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
