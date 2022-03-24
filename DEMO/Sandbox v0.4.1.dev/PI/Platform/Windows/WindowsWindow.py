from ...Core     import PI_VERSION, PI_V_SYNC, PI_CONFIG, PI_DEBUG
from ...Window   import Window, WindowProperties
from ...logger   import PI_CORE_ASSERT, PI_CORE_INFO
from ...Renderer import GraphicsContext
from ...Events   import *

from OpenGL.GL import glEnable, GL_DEPTH_TEST
import glfw

class WindowData:
    Title: str

    Width: int
    Height: int
    VSync: bool

    EventCallback = None

class WindowsWindow(Window):
    GLFWInitialized = False

    __Window = None
    __Data: WindowData

    __Context: GraphicsContext

    def __init__(self, props: WindowProperties) -> None:
        self.__Data = WindowData()
        self.__Init(props)

    def __del__(self) -> None:
        self.__Shutdown()

    def OnUpdate(self) -> None:
        glfw.poll_events()
        self.__Context.SwapBuffers()

    def __Init(self, props: WindowProperties) -> None:
        self.__Data.Title = props.Title
        self.__Data.Width = props.Width
        self.__Data.Height = props.Height

        PI_CORE_INFO("Creating Window: {} ({}, {})".format(self.__Data.Title, self.__Data.Width, self.__Data.Height))

        if (not WindowsWindow.GLFWInitialized):
            success: int = glfw.init()
            PI_CORE_ASSERT(success, "Could not intialize GLFW!")

            glfw.set_error_callback(WindowsWindow.GLFWErrorEventHandler)

            WindowsWindow.GLFWInitialized = True

        if (PI_DEBUG):
            self.__Window = glfw.create_window(props.Width, props.Height, 
                "{} - PI v{} - Config: {}".format(self.__Data.Title, PI_VERSION, PI_CONFIG),
                None, None
            )

        else:
            self.__Window = glfw.create_window(props.Width, props.Height, 
                "{} - PI v{}".format(self.__Data.Title, PI_VERSION),
                None, None
            )

        self.__Context = GraphicsContext.Create(self.__Window)
        self.__Context.Init()

        glfw.set_window_user_pointer(self.__Window, self.__Data)
        self.SetVSync(PI_V_SYNC)

        # Sets GLFW callbacks
        glfw.set_window_size_callback  ( self.__Window, WindowsWindow.WindowResizeEventHandler )
        glfw.set_window_close_callback ( self.__Window, WindowsWindow.WindowCloseEventHandler  )
        glfw.set_key_callback          ( self.__Window, WindowsWindow.KeyEventHandler          )
        glfw.set_mouse_button_callback ( self.__Window, WindowsWindow.MouseButtonEventHandler  )
        glfw.set_scroll_callback       ( self.__Window, WindowsWindow.MouseScrollEventHandler  )
        glfw.set_cursor_pos_callback   ( self.__Window, WindowsWindow.MouseMovedEventHandler   )

    def __Shutdown(self) -> None:
        glfw.destroy_window(self.__Window)

    @staticmethod
    def GLFWErrorEventHandler(error, description):
        print("GLFW Error ({}): {}".format(error, description))

    @staticmethod
    def WindowResizeEventHandler(window, width, height):
        data = glfw.get_window_user_pointer(window)

        data.Width = width
        data.Height = height

        event = WindowResizeEvent(width, height)
        data.EventCallback(event)

    @staticmethod
    def WindowCloseEventHandler(window):
        data = glfw.get_window_user_pointer(window)
        event = WindowCloseEvent()
        data.EventCallback(event)

    @staticmethod
    def KeyEventHandler(window, key, scancode, action, mods):
        data = glfw.get_window_user_pointer(window)

        if (action == glfw.PRESS):
            event = KeyPressedEvent(key, 0)
            data.EventCallback(event)

        elif (action == glfw.RELEASE):
            event = KeyReleasedEvent(key)
            data.EventCallback(event)

        elif (action == glfw.REPEAT):
            event = KeyPressedEvent(key, 1)
            data.EventCallback(event)

    @staticmethod
    def MouseButtonEventHandler(window, button, action, mods):
        data = glfw.get_window_user_pointer(window)

        if (action == glfw.PRESS):
            event = MouseButtonPressedEvent(button)
            data.EventCallback(event)

        elif (action == glfw.RELEASE):
            event = MouseButtonReleasedEvent(button)
            data.EventCallback(event)

    @staticmethod
    def MouseScrollEventHandler(window, xoffset, yoffset):
        data = glfw.get_window_user_pointer(window)
        event = MouseScrolledEvent(yoffset, xoffset)
        data.EventCallback(event)

    @staticmethod
    def MouseMovedEventHandler(window, xoffset, yoffset):
        data = glfw.get_window_user_pointer(window)
        event = MouseMovedEvent(xoffset, yoffset)
        data.EventCallback(event)

    @property
    def Width(self) -> int:
        return self.__Data.Width

    @property
    def Height(self) -> int:
        return self.__Data.Height

    def SetEventCallback(self, callback) -> None:
        self.__Data.EventCallback = callback

    def SetVSync(self, enable: bool) -> None:
        if (enable):
            glfw.swap_interval(1)
        else:
            glfw.swap_interval(0)

        self.__Data.VSync = enable

    @property
    def NativeWindow(self):
        return self.__Window

    @property
    def IsVsync(self) -> None:
        return self.__Data.VSync

    @staticmethod
    def Create(props: WindowProperties=WindowProperties()):
        return WindowsWindow(props)
