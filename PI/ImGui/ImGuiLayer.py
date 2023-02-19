from ..Events import Event, KeyEvent, MouseScrolledEvent, WindowResizeEvent, EventDispatcher, EventCategory, EventType
from ..Layers import Layer
from ..Core.Input import Input
from ..ButtonCodes.KeyCodes import *

from ..Core.StateManager import StateManager

from typing import Any, Dict
from imgui.integrations.glfw import *
import imgui

# Currently only supports Colors
class ImGuiTheme:
    __slots__ = "__Fields", "CurrentTheme", \
        "Default", "DefaultDark", "DefaultLight", "DefaultInactive", "DefaultActive", "Ruth", "LightActive"

    def __init__ (self) -> None: self.__Fields: Dict[int, Any] = {}
    def __eq__   (self, other) -> bool: return self.__Fields == other.__Fields

    def AddFields(self, fields: Dict[int, Any]) -> None:
        for field, value in fields.items(): self.__Fields[field] = value

    def Apply(self) -> None:
        for field, value in self.__Fields.items():
            colors = imgui.get_style().colors
            colors[field] = value

    @property
    def Fields(self) -> Dict[int, Any]: return self.__Fields

    def Copy(self):
        theme = ImGuiTheme()
        theme.AddFields(self.__Fields)
        return theme

# Light Theme
ImGuiTheme.DefaultLight = ImGuiTheme()
ImGuiTheme.DefaultLight.AddFields({
    # Text
    imgui.COLOR_TEXT          : imgui.Vec4( 0.00 , 0.00 , 0.00 , 1.0 ),
    imgui.COLOR_TEXT_DISABLED : imgui.Vec4( 0.60 , 0.60 , 0.60 , 1.0 ),

    imgui.COLOR_TEXT_SELECTED_BACKGROUND : imgui.Vec4( 0.26 , 0.59 , 0.98 , 0.35 ),

    # Window
    imgui.COLOR_WINDOW_BACKGROUND : imgui.Vec4( 0.94 , 0.94 , 0.94 , 0.94 ),
    imgui.COLOR_CHILD_BACKGROUND  : imgui.Vec4( 0.00 , 0.00 , 0.00 , 0.00 ),

    # Border
    imgui.COLOR_BORDER        : imgui.Vec4( 0.00 , 0.00 , 0.00 , 0.39 ),
    imgui.COLOR_BORDER_SHADOW : imgui.Vec4( 1.00 , 1.00 , 1.00 , 0.10 ),

    # Frame
    imgui.COLOR_FRAME_BACKGROUND         : imgui.Vec4( 1.00 , 1.00 , 1.00 , 0.94 ),
    imgui.COLOR_FRAME_BACKGROUND_HOVERED : imgui.Vec4( 0.26 , 0.59 , 0.98 , 0.40 ),
    imgui.COLOR_FRAME_BACKGROUND_ACTIVE  : imgui.Vec4( 0.26 , 0.59 , 0.98 , 0.67 ),

    # Tabs
    imgui.COLOR_TAB         : imgui.Vec4( 0.75 , 0.80 , 0.92 , 1.00 ),
    imgui.COLOR_TAB_HOVERED : imgui.Vec4( 0.80 , 0.87 , 0.98 , 1.00 ),
    imgui.COLOR_TAB_ACTIVE  : imgui.Vec4( 0.75 , 0.81 , 0.93 , 1.00 ),

    imgui.COLOR_TAB_UNFOCUSED         : imgui.Vec4( 0.81 , 0.87 , 0.98 , 1.0 ),
    imgui.COLOR_TAB_UNFOCUSED_ACTIVE  : imgui.Vec4( 0.75 , 0.81 , 0.93 , 1.0 ),

    # Title
    imgui.COLOR_TITLE_BACKGROUND           : imgui.Vec4( 0.96 , 0.96 , 0.96 , 1.00 ),
    imgui.COLOR_TITLE_BACKGROUND_COLLAPSED : imgui.Vec4( 1.00 , 1.00 , 1.00 , 0.51 ),
    imgui.COLOR_TITLE_BACKGROUND_ACTIVE    : imgui.Vec4( 0.82 , 0.82 , 0.82 , 1.00 ),

    # Scrollbar
    imgui.COLOR_SCROLLBAR_BACKGROUND   : imgui.Vec4( 0.98 , 0.98 , 0.98 , 0.53 ),
    imgui.COLOR_SCROLLBAR_GRAB         : imgui.Vec4( 0.69 , 0.69 , 0.69 , 1.00 ),
    imgui.COLOR_SCROLLBAR_GRAB_HOVERED : imgui.Vec4( 0.49 , 0.49 , 0.49 , 1.00 ),
    imgui.COLOR_SCROLLBAR_GRAB_ACTIVE  : imgui.Vec4( 0.49 , 0.49 , 0.49 , 1.00 ),

    # Button
    imgui.COLOR_BUTTON         : imgui.Vec4( 0.26 , 0.59 , 0.98 , 0.40 ),
    imgui.COLOR_BUTTON_HOVERED : imgui.Vec4( 0.26 , 0.59 , 0.98 , 1.00 ),
    imgui.COLOR_BUTTON_ACTIVE  : imgui.Vec4( 0.06 , 0.53 , 0.98 , 1.00 ),

    # Header
    imgui.COLOR_HEADER         : imgui.Vec4( 0.26 , 0.59 , 0.98 , 0.31 ),
    imgui.COLOR_HEADER_HOVERED : imgui.Vec4( 0.26 , 0.59 , 0.98 , 0.80 ),
    imgui.COLOR_HEADER_ACTIVE  : imgui.Vec4( 0.26 , 0.59 , 0.98 , 1.00 ),

    # Resize Grip
    imgui.COLOR_RESIZE_GRIP         : imgui.Vec4( 1.00 , 1.00 , 1.00 , 0.50 ),
    imgui.COLOR_RESIZE_GRIP_HOVERED : imgui.Vec4( 0.26 , 0.59 , 0.98 , 0.67 ),
    imgui.COLOR_RESIZE_GRIP_ACTIVE  : imgui.Vec4( 0.26 , 0.59 , 0.98 , 0.95 ),

    # Miscellaneous
    imgui.COLOR_POPUP_BACKGROUND   : imgui.Vec4( 1.00 , 1.00 , 1.00 , 0.94 ),
    imgui.COLOR_MENUBAR_BACKGROUND : imgui.Vec4( 0.86 , 0.86 , 0.86 , 1.00 ),
    imgui.COLOR_CHECK_MARK         : imgui.Vec4( 0.26 , 0.59 , 0.98 , 1.00 ),

    imgui.COLOR_SLIDER_GRAB        : imgui.Vec4( 0.24 , 0.52 , 0.88 , 1.00 ),
    imgui.COLOR_SLIDER_GRAB_ACTIVE : imgui.Vec4( 0.26 , 0.59 , 0.98 , 1.00 ),

    imgui.COLOR_MODAL_WINDOW_DIM_BACKGROUND : imgui.Vec4( 0.20 , 0.20 , 0.20 , 0.35 )

})

# Ruth Theme
ImGuiTheme.Ruth = ImGuiTheme()
ImGuiTheme.Ruth.AddFields({
    # Text
    imgui.COLOR_TEXT          : imgui.Vec4( 0.80 , 0.80 , 0.83 , 1.0 ),
    imgui.COLOR_TEXT_DISABLED : imgui.Vec4( 0.24 , 0.23 , 0.29 , 1.0 ),

    imgui.COLOR_TEXT_SELECTED_BACKGROUND : imgui.Vec4( 0.26 , 0.59 , 0.98 , 0.35 ),

    # Window
    imgui.COLOR_WINDOW_BACKGROUND : imgui.Vec4( 0.06 , 0.05 , 0.07 , 1.00 ),
    imgui.COLOR_CHILD_BACKGROUND  : imgui.Vec4( 0.07 , 0.07 , 0.09 , 1.00 ),

    # Border
    imgui.COLOR_BORDER        : imgui.Vec4( 0.80 , 0.80 , 0.83 , 0.88 ),
    imgui.COLOR_BORDER_SHADOW : imgui.Vec4( 0.92 , 0.91 , 0.88 , 0.00 ),

    # Frame
    imgui.COLOR_FRAME_BACKGROUND         : imgui.Vec4( 0.10 , 0.09 , 0.12 , 1.00 ),
    imgui.COLOR_FRAME_BACKGROUND_HOVERED : imgui.Vec4( 0.23 , 0.24 , 0.29 , 1.00 ),
    imgui.COLOR_FRAME_BACKGROUND_ACTIVE  : imgui.Vec4( 0.56 , 0.56 , 0.58 , 1.00 ),

    # Tabs
    imgui.COLOR_TAB         : imgui.Vec4( 0.15 , 0.1505 , 0.151 , 1.0 ),
    imgui.COLOR_TAB_HOVERED : imgui.Vec4( 0.38 , 0.3805 , 0.381 , 1.0 ),
    imgui.COLOR_TAB_ACTIVE  : imgui.Vec4( 0.28 , 0.2805 , 0.281 , 1.0 ),

    imgui.COLOR_TAB_UNFOCUSED         : imgui.Vec4( 0.15 , 0.1505 , 0.151 , 1.0 ),
    imgui.COLOR_TAB_UNFOCUSED_ACTIVE  : imgui.Vec4( 0.2  , 0.205  , 0.21  , 1.0 ),

    # Title
    imgui.COLOR_TITLE_BACKGROUND           : imgui.Vec4( 0.10 , 0.09 , 0.12 , 1.00 ),
    imgui.COLOR_TITLE_BACKGROUND_COLLAPSED : imgui.Vec4( 1.00 , 0.98 , 0.95 , 0.75 ),
    imgui.COLOR_TITLE_BACKGROUND_ACTIVE    : imgui.Vec4( 0.07 , 0.07 , 0.09 , 1.00 ),

    # Scrollbar
    imgui.COLOR_SCROLLBAR_BACKGROUND   : imgui.Vec4( 0.10 , 0.09 , 0.12 , 1.00 ),
    imgui.COLOR_SCROLLBAR_GRAB         : imgui.Vec4( 0.80 , 0.80 , 0.83 , 0.31 ),
    imgui.COLOR_SCROLLBAR_GRAB_HOVERED : imgui.Vec4( 0.56 , 0.56 , 0.58 , 1.00 ),
    imgui.COLOR_SCROLLBAR_GRAB_ACTIVE  : imgui.Vec4( 0.06 , 0.05 , 0.07 , 1.00 ),

    # Button
    imgui.COLOR_BUTTON         : imgui.Vec4( 0.10 , 0.09 , 0.12 , 1.00 ),
    imgui.COLOR_BUTTON_HOVERED : imgui.Vec4( 0.23 , 0.24 , 0.29 , 1.00 ),
    imgui.COLOR_BUTTON_ACTIVE  : imgui.Vec4( 0.56 , 0.56 , 0.58 , 1.00 ),

    # Header
    imgui.COLOR_HEADER         : imgui.Vec4( 0.10 , 0.09 , 0.12 , 1.00 ),
    imgui.COLOR_HEADER_HOVERED : imgui.Vec4( 0.56 , 0.56 , 0.58 , 1.00 ),
    imgui.COLOR_HEADER_ACTIVE  : imgui.Vec4( 0.06 , 0.05 , 0.07 , 1.00 ),

    # Resize Grip
    imgui.COLOR_RESIZE_GRIP         : imgui.Vec4( 0.00 , 0.00 , 0.00 , 0.00 ),
    imgui.COLOR_RESIZE_GRIP_HOVERED : imgui.Vec4( 0.56 , 0.56 , 0.58 , 1.00 ),
    imgui.COLOR_RESIZE_GRIP_ACTIVE  : imgui.Vec4( 0.06 , 0.05 , 0.07 , 1.00 ),

    # Miscellaneous
    imgui.COLOR_POPUP_BACKGROUND   : imgui.Vec4( 0.07 , 0.07 , 0.09 , 1.00 ),
    imgui.COLOR_MENUBAR_BACKGROUND : imgui.Vec4( 0.10 , 0.09 , 0.12 , 1.00 ),
    imgui.COLOR_CHECK_MARK         : imgui.Vec4( 0.80 , 0.80 , 0.83 , 0.31 ),

    imgui.COLOR_SLIDER_GRAB        : imgui.Vec4( 0.80 , 0.80 , 0.83 , 0.31 ),
    imgui.COLOR_SLIDER_GRAB_ACTIVE : imgui.Vec4( 0.06 , 0.05 , 0.07 , 1.00 ),

    imgui.COLOR_MODAL_WINDOW_DIM_BACKGROUND : imgui.Vec4( 1.00 , 0.98 , 0.95 , 0.73 )

})

# Dark Theme
# Auto generate DefaultDark
ImGuiTheme.DefaultDark = ImGuiTheme()
__fields = {}

for field, value in ImGuiTheme.DefaultLight.Fields.items():
    h, s, v = imgui.color_convert_rgb_to_hsv(value[0], value[1], value[2])
    if s < 0.1: v = 1.0 - v
    r, g, b = imgui.color_convert_hsv_to_rgb(h, s, v)
    __fields[field] = imgui.Vec4(r, g, b, value[3])

ImGuiTheme.DefaultDark.AddFields(__fields)

# These are some values I like
# so, they will override the default
ImGuiTheme.DefaultDark.AddFields({
    imgui.COLOR_WINDOW_BACKGROUND: imgui.Vec4( 0.1, 0.105, 0.11, 1.0 ),

    # Hederes
    imgui.COLOR_HEADER         : imgui.Vec4( 0.2  , 0.205  , 0.21  , 1.0 ),
    imgui.COLOR_HEADER_HOVERED : imgui.Vec4( 0.3  , 0.305  , 0.31  , 1.0 ),
    imgui.COLOR_HEADER_ACTIVE  : imgui.Vec4( 0.15 , 0.1505 , 0.151 , 1.0 ),

    
    # Buttons
    imgui.COLOR_BUTTON         : imgui.Vec4( 0.2  , 0.205  , 0.21  , 1.0 ),
    imgui.COLOR_BUTTON_HOVERED : imgui.Vec4( 0.3  , 0.305  , 0.31  , 1.0 ),
    imgui.COLOR_BUTTON_ACTIVE  : imgui.Vec4( 0.15 , 0.1505 , 0.151 , 1.0 ),

    # Frame BG
    imgui.COLOR_FRAME_BACKGROUND         : imgui.Vec4( 0.2  , 0.205  , 0.21  , 1.0 ),
    imgui.COLOR_FRAME_BACKGROUND_HOVERED : imgui.Vec4( 0.3  , 0.305  , 0.31  , 1.0 ),
    imgui.COLOR_FRAME_BACKGROUND_ACTIVE  : imgui.Vec4( 0.15 , 0.1505 , 0.151 , 1.0 ),

    # Tabs
    imgui.COLOR_TAB         : imgui.Vec4( 0.15 , 0.1505 , 0.151 , 1.0 ),
    imgui.COLOR_TAB_HOVERED : imgui.Vec4( 0.38 , 0.3805 , 0.381 , 1.0 ),
    imgui.COLOR_TAB_ACTIVE  : imgui.Vec4( 0.28 , 0.2805 , 0.281 , 1.0 ),

    imgui.COLOR_TAB_UNFOCUSED         : imgui.Vec4( 0.15 , 0.1505 , 0.151 , 1.0 ),
    imgui.COLOR_TAB_UNFOCUSED_ACTIVE  : imgui.Vec4( 0.2  , 0.205  , 0.21  , 1.0 ),

    # Title
    imgui.COLOR_TITLE_BACKGROUND           : imgui.Vec4( 0.15 , 0.1505 , 0.151 , 1.0 ),
    imgui.COLOR_TITLE_BACKGROUND_ACTIVE    : imgui.Vec4( 0.15 , 0.1505 , 0.151 , 1.0 ),
    imgui.COLOR_TITLE_BACKGROUND_COLLAPSED : imgui.Vec4( 0.15 , 0.1505 , 0.151 , 1.0 )
})

# It is good to copy as changing a theme will not affect rest
ImGuiTheme.Default = ImGuiTheme.DefaultDark.Copy()     # I love Dark theme

ImGuiTheme.DefaultInactive = ImGuiTheme.Default.Copy()
ImGuiTheme.DefaultActive   = ImGuiTheme.Ruth.Copy()

# Overrides Again
ImGuiTheme.DefaultActive.AddFields({
    imgui.COLOR_WINDOW_BACKGROUND : imgui.Vec4( 0.0 , 0.0 , 0.0 , 1.00 ),
})

ImGuiTheme.LightActive = ImGuiTheme.DefaultLight.Copy()
ImGuiTheme.LightActive.AddFields({
    imgui.COLOR_WINDOW_BACKGROUND: imgui.Vec4( 0.85, 0.87, 0.80, 1.0 ),

    imgui.COLOR_TITLE_BACKGROUND           : imgui.Vec4( 0.85 * 0.9, 0.87 * 0.9, 0.80 * 0.9, 1.0 ),
    imgui.COLOR_TITLE_BACKGROUND_COLLAPSED : imgui.Vec4( 1., 1.0, 1.0, 0.51 ),
    imgui.COLOR_TITLE_BACKGROUND_ACTIVE    : imgui.Vec4( 0.85 * 0.8, 0.87 * 0.8, 0.80 * 0.8, 1.0 ),

    imgui.COLOR_MENUBAR_BACKGROUND : imgui.Vec4( 0.85 * 0.7, 0.87 * 0.7, 0.80 * 0.7, 1.0 ),
})

class ImGuiLayer(Layer):
    __slots__ = "__Time", "__Renderer", "__io", "__BlockEvents"

    GlobalHeadingFont = None

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

        fontLoc = ".\\Assets\\Internal\\Fonts\\opensans\\OpenSans-Regular.ttf"
        io.fonts.add_font_from_file_ttf(fontLoc, 18.0)
        ImGuiLayer.GlobalHeadingFont = io.fonts.add_font_from_file_ttf(fontLoc, 24.0)

        imgui.style_colors_dark()
        
        style = imgui.get_style()
        if io.config_flags & imgui.CONFIG_VIEWEPORTS_ENABLE:
            style.window_rounding = 0.0
            bgColor = style.colors[imgui.COLOR_WINDOW_BACKGROUND]
            style.colors[imgui.COLOR_WINDOW_BACKGROUND] = imgui.Vec4( bgColor.x, bgColor.y, bgColor.z, 1.0 )

        ImGuiLayer.SetTheme(ImGuiTheme.Default)

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
    def __KeyboardPressCallback    ( self, e: KeyEvent           ) -> None:
        io = self.__io

        io.keys_down[e.KeyCode] = True

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
    def __KeyboardReleasedCallback ( self, e: KeyEvent           ) -> None:
        io = self.__io

        io.keys_down[e.KeyCode] = False

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
    def __CharInputCallback        ( self, e: KeyEvent           ) -> None:
        io = self.__io

        if 0 < e.Char < 0x10000:
            io.add_input_character(e.Char)
            if self.__BlockEvents: return True

        return False
    def __WindowResizeCallback     ( self, e: WindowResizeEvent  ) -> None:
        self.__io.display_size = e.Width, e.Height

        if self.__BlockEvents: return True
        return False
    def __MouseScrollCallback      ( self, e: MouseScrolledEvent ) -> None:
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

    @staticmethod
    def SetTheme(theme: ImGuiTheme) -> None: theme.Apply()
