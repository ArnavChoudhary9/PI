from ..Instrumentation import Instrumentor, InstrumentationTimer

PI_VERSION: str = "0.7.1.dev"

PI_LATEST_UPDATE: str = """
    x.x.0
    Added Phong Shading

    x.x.1
    Added Specular controll
"""

#-------------------------------------------------------------------
# Platforms
SUPPORTED_PLATFORMS = ["Windows"]           # Currently only supports Windows
CURRENT_PLATFORM = SUPPORTED_PLATFORMS[0]
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# To turn on and off certain features
PI_CONFIGS : tuple = ("DEBUG", "NO_INSTRUMENTATION", "RELEASE", "RELEASE_NO_IMGUI")
PI_CONFIG  : str   = PI_CONFIGS[0]

PI_DEBUG           : bool
PI_LOGGING         : bool
PI_INSTRUMENTATION : bool
PI_IMGUI           : bool
PI_IMGUI_DOCKING   : bool

PI_V_SYNC: bool = True

# Full DEBUG Configuration
if PI_CONFIG == "DEBUG":
    PI_DEBUG   : bool = True
    PI_LOGGING : bool = True
    PI_IMGUI   : bool = True
    PI_INSTRUMENTATION: bool = True

# NO_INSTRUMENTATION Configuration
if PI_CONFIG == "NO_INSTRUMENTATION":
    PI_DEBUG   : bool = True
    PI_LOGGING : bool = True
    PI_IMGUI   : bool = True
    PI_INSTRUMENTATION: bool = False

# Strips all debugging features
if PI_CONFIG == "RELEASE":
    PI_DEBUG   : bool = False
    PI_LOGGING : bool = False
    PI_IMGUI   : bool = True
    PI_INSTRUMENTATION: bool = False

# Strips all debugging features and ImGui
if PI_CONFIG == "RELEASE_NO_IMGUI":
    PI_DEBUG   : bool = False
    PI_LOGGING : bool = False
    PI_IMGUI   : bool = False
    PI_INSTRUMENTATION: bool = False

try:
    # if Python is able to import this it means the docking branch is enabled
    from imgui import CONFIG_DOCKING_ENABLE
    PI_IMGUI_DOCKING = True
except:
    PI_IMGUI_DOCKING = False
# -------------------------------------------------------------------

#-------------------------------------------------------------------
# Instrumentation
def EmptyFunc(name: str=""):
    pass

PI_INSTRUMENTATION_BEGIN_SESSION = EmptyFunc
PI_INSTRUMENTATION_END_SESSION   = EmptyFunc
PI_TIMER = EmptyFunc

if PI_INSTRUMENTATION:
    def _BeginSession(name: str) -> None:
        Instrumentor.Get().BeginSession(name)
        
    def _EndSession() -> None:
        Instrumentor.Get().EndSession()

    def _Timer(name: str) -> InstrumentationTimer:
        return InstrumentationTimer(name)

    PI_INSTRUMENTATION_BEGIN_SESSION = _BeginSession
    PI_INSTRUMENTATION_END_SESSION   = _EndSession
    PI_TIMER = _Timer
#-------------------------------------------------------------------
