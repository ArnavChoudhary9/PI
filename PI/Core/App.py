from .Base      import PI_INSTRUMENTATION_BEGIN_SESSION, PI_INSTRUMENTATION_END_SESSION, PI_IMGUI, PI_DEBUG
from ..Events   import *
from .Input     import Input
from ..ImGui    import ImGuiLayer
from ..Layers   import *
from ..Platform import *
from ..Renderer import RenderCommand, Renderer, Renderer2D, Shader
from .Timestep  import Timestep
from .Window   import Window, WindowProperties
from .StateManager import StateManager

from ..Logging import logger

from abc import ABC
import glfw

class PI_Application(ABC):
    '''
    This is the Root for all classes used to make Application using PI Engine.
    '''

    # _Name   : str           # Name of the Application
    # _Window : Window        # Window that it creates

    # _Running: bool          # Is this application Running
    # _LayerStack: LayerStack
    # __ImGuiLayer: ImGuiLayer

    # _Camera: Camera

    # _LastFrameTime: float = 0.0

    __slots__ = "_Name", "_Window", "_Running", "_IsMinimised", \
        "_LayerStack", "__ImGuiLayer", \
        "_LastFrameTime", "timestep"

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

        Renderer.Init()
        Input.Init()

        self._Window = Window.Create(props)
        self._Window.SetEventCallback(self.OnEvent)

        StateManager.SetContext(self)

        # Renderer 2D can only be initialized after Rendering API is Initializd
        # i.e. After window is created
        Renderer2D.Init()
        Renderer.LineShader: Shader = Shader.Create(".\\Assets\\Internal\\Shaders\\Line3D.glsl")
  
        from ..Scripting.ScriptingEngine import ScriptingEngine
        ScriptingEngine.Init()

        from .CacheManager import LocalCache
        LocalCache.Init()
        LocalCache.LoadFields()

        self._IsMinimised = False

        self._LayerStack = LayerStack()

        self.__ImGuiLayer = ImGuiLayer()
        self._LayerStack.PushOverlay(self.__ImGuiLayer)

        self._LastFrameTime = 0.0
        self.timestep = Timestep(0)

    def __del__(self) -> None: pass

    @property
    def Name(self) -> str:
        '''Name of the Application'''
        return self._Name

    @property
    def Window(self) -> Window:
        '''The Window it created'''
        return self._Window

    @property
    def ImGuiLayer(self) -> ImGuiLayer:
        '''Returns the ImGui Layer of the current application'''
        return self.__ImGuiLayer

    def OnWindowClose(self, event: WindowCloseEvent):
        '''This will be called to to terminate the application.'''
        self.Close()
        return True

    def OnWindowResize(self, event: WindowResizeEvent):
        '''Resizes the window'''

        if event.Width == 0 or event.Height == 0:
            self._IsMinimised = True
            return False

        self._IsMinimised = False

        # glViewport(0, 0, event.Width, event.Height)
        Renderer.OnResize(event.Width, event.Height)

        return False

    def OnEvent(self, event: Event):
        '''Called when an event occures on the Window'''
        dispatcher = EventDispatcher(event)

        dispatcher.Dispach( self.OnWindowResize , EventType.WindowResize )
        dispatcher.Dispach( self.OnWindowClose  , EventType.WindowClose  )

        self._LayerStack.OnEvent(event)

    def Run(self) -> None:
        '''you should call this function within the run loop of the derived class.'''
        _time = glfw.get_time()
        self.timestep = Timestep(_time - self._LastFrameTime)
        self._LastFrameTime = _time

        if not self._IsMinimised:
            StateManager.SetContext(self)

            RenderCommand.SetClearColor(0.1, 0.1, 0.1, 1)
            RenderCommand.Clear()

            self._LayerStack.OnUpdate(self.timestep)

        if PI_IMGUI:
            self.__ImGuiLayer.Begin()
            self._LayerStack.OnImGuiRender()
            self.__ImGuiLayer.End()

        self._Window.OnUpdate()

        # if PI_DEBUG: gc.collect()     # Safer but costs ~40 FPS

    def Close(self) -> None:
        if not self._Running: return

        from ..Scripting.ScriptingEngine import ScriptingEngine
        ScriptingEngine.Shutdown()

        from .CacheManager import LocalCache
        LocalCache.Shutdown()

        self._Running = False
    
CreateApplication = None

def _main():
    '''The Entry point fore the code'''
    PI_INSTRUMENTATION_BEGIN_SESSION("PI_Init")
    app: PI_Application = CreateApplication()
    PI_INSTRUMENTATION_END_SESSION()

    PI_INSTRUMENTATION_BEGIN_SESSION("PI_Runtime")
    app.Run()
    PI_INSTRUMENTATION_END_SESSION()

    PI_INSTRUMENTATION_BEGIN_SESSION("PI_Shutdown")
    app.Close()
    del app
    PI_INSTRUMENTATION_END_SESSION()

def main():
    if PI_DEBUG:
        # Only for Detailed Profiling
        import cProfile
        import pstats

        with cProfile.Profile() as pr:
            _main()

        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.dump_stats(filename="profile.prof")

    else:
        _main()
