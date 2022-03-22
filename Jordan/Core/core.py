from ..Instrumentation import Instrumentor, InstrumentationTimer

JD_VERSION: str = "0.3.5.dev"

JD_LATEST_UPDATE: str = """
    
"""

#-------------------------------------------------------------------
# To turn on and off certain features
JD_CONFIGS : tuple = ("DEBUG", "NO_INSTRUMENTATION", "RELEASE")
JD_CONFIG  : str   = JD_CONFIGS[0]

JD_DEBUG           : bool
JD_LOGGING         : bool
JD_INSTRUMENTATION : bool

JD_V_SYNC: bool = True

# Full DEBUG Configuration
if JD_CONFIG == "DEBUG":
    JD_DEBUG   : bool = True
    JD_LOGGING : bool = True
    JD_INSTRUMENTATION: bool = True

# NO_INSTRUMENTATION Configuration
if JD_CONFIG == "NO_INSTRUMENTATION":
    JD_DEBUG   : bool = True
    JD_LOGGING : bool = True
    JD_INSTRUMENTATION: bool = False

# Strips all debugging features
if JD_CONFIG == "RELEASE":
    JD_DEBUG   : bool = False
    JD_LOGGING : bool = False
    JD_INSTRUMENTATION: bool = False
# -------------------------------------------------------------------

#-------------------------------------------------------------------
# Platforms
SUPPORTED_PLATFORMS = ["Windows"]           # Currently only supports Windows
CURRENT_PLATFORM = SUPPORTED_PLATFORMS[0]
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# Instrumentation
def EmptyFunc(name: str=""):
    pass

JD_INSTRUMENTATION_BEGIN_SESSION = EmptyFunc
JD_INSTRUMENTATION_END_SESSION   = EmptyFunc
JD_TIMER = EmptyFunc

if JD_INSTRUMENTATION:
    def _BeginSession(name: str) -> None:
        Instrumentor.Get().BeginSession(name)
        
    def _EndSession() -> None:
        Instrumentor.Get().EndSession()

    def _Timer(name: str) -> InstrumentationTimer:
        return InstrumentationTimer(name)

    JD_INSTRUMENTATION_BEGIN_SESSION = _BeginSession
    JD_INSTRUMENTATION_END_SESSION   = _EndSession
    JD_TIMER = _Timer
#-------------------------------------------------------------------
