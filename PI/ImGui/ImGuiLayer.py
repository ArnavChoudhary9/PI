from ..Events import Event, EventDispatcher, EventCategory, EventType
from ..Layers import Layer
from ..Core.Input import Input
from ..ButtonCodes.KeyCodes import *

from ..Core.StateManager import StateManager

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
        io.config_flags |= imgui.CONFIG_DOCKING_ENABLE
        io.config_flags |= imgui.CONFIG_VIEWEPORTS_ENABLE

        io.fonts.add_font_from_file_ttf(".\\Assets\\Internal\\Fonts\\opensans\\OpenSans-Regular.ttf", 18.0)

        imgui.style_colors_dark()
        
        style = imgui.get_style()
        if io.config_flags & imgui.CONFIG_VIEWEPORTS_ENABLE:
            style.window_rounding = 0.0
            bgColor = style.colors[imgui.COLOR_WINDOW_BACKGROUND]
            style.colors[imgui.COLOR_WINDOW_BACKGROUND] = imgui.Vec4( bgColor.x, bgColor.y, bgColor.z, 1.0 )

        self.SetDarkThemeColors()

        window = StateManager.GetCurrentNativeWindow()
        self.__Renderer = GlfwRenderer(window, False)    

    def OnDetach(self) -> None:
        self.__Renderer.shutdown()

    def BlockEvents(self, block: bool) -> None:
        self.__BlockEvents = block

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

    def Begin(self) -> None:
        self.__Renderer.process_inputs()
        imgui.new_frame()

    def End(self) -> None:
        imgui.render()
        self.__Renderer.render(imgui.get_draw_data())

        io = imgui.get_io()
        if io.config_flags & imgui.CONFIG_VIEWEPORTS_ENABLE:
            backupCurrentContext = glfw.get_current_context()
            imgui.update_platform_windows()
            imgui.render_platform_windows_default()
            glfw.make_context_current(backupCurrentContext)

    def SetDarkThemeColors(self) -> None:
        colors = imgui.get_style().colors
        colors[imgui.COLOR_WINDOW_BACKGROUND] = imgui.Vec4( 0.1, 0.105, 0.11, 1.0 )

        # Hederes
        colors[imgui.COLOR_HEADER]         = imgui.Vec4( 0.2  , 0.205  , 0.21  , 1.0 )
        colors[imgui.COLOR_HEADER_HOVERED] = imgui.Vec4( 0.3  , 0.305  , 0.31  , 1.0 )
        colors[imgui.COLOR_HEADER_ACTIVE]  = imgui.Vec4( 0.15 , 0.1505 , 0.151 , 1.0 )

        # Buttons
        colors[imgui.COLOR_BUTTON]         = imgui.Vec4( 0.2  , 0.205  , 0.21  , 1.0 )
        colors[imgui.COLOR_BUTTON_HOVERED] = imgui.Vec4( 0.3  , 0.305  , 0.31  , 1.0 )
        colors[imgui.COLOR_BUTTON_ACTIVE]  = imgui.Vec4( 0.15 , 0.1505 , 0.151 , 1.0 )

        # Frame BG
        colors[imgui.COLOR_FRAME_BACKGROUND]         = imgui.Vec4( 0.2  , 0.205  , 0.21  , 1.0 )
        colors[imgui.COLOR_FRAME_BACKGROUND_HOVERED] = imgui.Vec4( 0.3  , 0.305  , 0.31  , 1.0 )
        colors[imgui.COLOR_FRAME_BACKGROUND_ACTIVE]  = imgui.Vec4( 0.15 , 0.1505 , 0.151 , 1.0 )

        # Tabs
        colors[imgui.COLOR_TAB]         = imgui.Vec4( 0.15 , 0.1505 , 0.151 , 1.0 )
        colors[imgui.COLOR_TAB_HOVERED] = imgui.Vec4( 0.38 , 0.3805 , 0.381 , 1.0 )
        colors[imgui.COLOR_TAB_ACTIVE]  = imgui.Vec4( 0.28 , 0.2805 , 0.281 , 1.0 )

        colors[imgui.COLOR_TAB_UNFOCUSED]         = imgui.Vec4( 0.15 , 0.1505 , 0.151 , 1.0 )
        colors[imgui.COLOR_TAB_UNFOCUSED_ACTIVE]  = imgui.Vec4( 0.2  , 0.205  , 0.21  , 1.0 )

        # Title
        colors[imgui.COLOR_TITLE_BACKGROUND]           = imgui.Vec4( 0.15 , 0.1505 , 0.151 , 1.0 )
        colors[imgui.COLOR_TITLE_BACKGROUND_ACTIVE]    = imgui.Vec4( 0.15 , 0.1505 , 0.151 , 1.0 )
        colors[imgui.COLOR_TITLE_BACKGROUND_COLLAPSED] = imgui.Vec4( 0.15 , 0.1505 , 0.151 , 1.0 )
