from .core      import PI_INSTRUMENTATION_BEGIN_SESSION, PI_INSTRUMENTATION_END_SESSION, PI_IMGUI
from ..Events   import *
from ..Input    import Input
from ..ImGui    import ImGuiLayer
from ..Layers   import *
from ..Platform import *
from ..Renderer import RenderCommand, Camera
from .Timestep  import Timestep
from ..Window   import Window, WindowProperties

from .. import logger

from OpenGL.GL import glViewport    # Temp
from abc import ABC
import glfw

class PI_Application(ABC):
    '''
    This is the Root for all classes used to make Application using PI Engine.
    '''

    _Name   : str           # Name of the Application
    _Window : Window        # Window that it creates

    _Running: bool          # Is this application Running
    _LayerStack: LayerStack
    __ImGuiLayer: ImGuiLayer

    _EventDispacher: EventDispatcher
    _Camera: Camera

    _LastFrameTime: float = 0.0

    def __init__(self, name: str, props: WindowProperties=WindowProperties()) -> None:
        '''
        This initialize the super() class

        ``name``-
            type: str\n
            It is the name of the application.\n
            NOTE: This is note the name of the Window it creates.
        '''

        self._Name = name
        self._Running = True

        self._Window = Window.Create(props)
        self._Window.SetEventCallback(self.OnEvent)
        Input.SetWindow(self._Window)

        self._EventDispacher = EventDispatcher()
        self._LayerStack = LayerStack()

        self.__ImGuiLayer = ImGuiLayer()
        self._LayerStack.PushOverlay(self.__ImGuiLayer)

    def __del__(self) -> None:
        pass

    @property
    def Name(self) -> str:
        '''Name of the Application'''
        return self._Name

    @property
    def Window(self) -> Window:
        '''The Window it created'''
        return self._Window

    def OnWindowClose(self, event: WindowCloseEvent):
        '''This will be called to to terminate the application.'''
        self._Running = False
        event.Handled = True
        return True

    def OnWindowResize(self, event: WindowResizeEvent):
        '''Resizes the window'''
        glViewport(0, 0, event.Width, event.Height)
        self._Camera.SetAspectRatio(self._Window.AspectRatio)
        event.Handled = True
        return True

    def OnEvent(self, event: Event):
        '''Called when an event occures on the Window'''
        self._EventDispacher.ChangeEvent(event)

        self._EventDispacher.Dispach( self.OnWindowResize , EventType.WindowResize )
        self._EventDispacher.Dispach( self.OnWindowClose  , EventType.WindowClose  )

        self._LayerStack.OnEvent(event)

    def Run(self) -> None:
        '''you should call this function within the run loop of the derived class.'''
        _time = glfw.get_time()
        timestep = Timestep(_time - self._LastFrameTime)
        self._LastFrameTime = _time

        Input.SetWindow(self._Window)
        
        RenderCommand.SetClearColor(0.1, 0.1, 0.1, 1)
        RenderCommand.Clear()

        self._LayerStack.OnUpdate(timestep)

        if PI_IMGUI:
            self.__ImGuiLayer.Begin()
            self._LayerStack.OnImGuiRender()
            self.__ImGuiLayer.End()

            self._Window.OnUpdate()
    
CreateApplication = None

def main():
    '''The Entry point fore the code'''
    PI_INSTRUMENTATION_BEGIN_SESSION("PI_Init")
    app = CreateApplication()
    PI_INSTRUMENTATION_END_SESSION()

    PI_INSTRUMENTATION_BEGIN_SESSION("PI_Runtime")
    app.Run()
    PI_INSTRUMENTATION_END_SESSION()

    PI_INSTRUMENTATION_BEGIN_SESSION("PI_Shutdown")
    del app
    PI_INSTRUMENTATION_END_SESSION()
