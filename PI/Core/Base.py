from ..Instrumentation import Instrumentor, InstrumentationTimer

from typing import Tuple as _Tuple

PI_VERSION_TUPLE : _Tuple[int] = (1,1,5)
PI_VERSION       : str         = f"{'.'.join([str(_) for _ in PI_VERSION_TUPLE])}.dev"

PI_LATEST_UPDATE: str = """
    1.1.5.dev - Component Copying
"""

#-------------------------------------------------------------------
# Platforms
SUPPORTED_PLATFORMS = ["Windows"]           # Currently only supports Windows
CURRENT_PLATFORM    = SUPPORTED_PLATFORMS[0]
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# To turn on and off certain features
PI_CONFIGS : tuple = ("DEBUG", "NO_INSTRUMENTATION", "RELEASE", "RELEASE_NO_IMGUI")
PI_CONFIG  : str   = PI_CONFIGS[0]

PI_DEBUG           : bool
PI_LOGGING         : bool
PI_INSTRUMENTATION : bool
PI_IMGUI           : bool

PI_DEBUG_SCRIPTS: bool = False

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
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# Checks the imports
try:
    # if Python is able to import this it means the docking branch is enabled
    from imgui import CONFIG_DOCKING_ENABLE as __IMPORT_TEST
except ImportError:
    from ..Logging.logger import PI_CORE_ASSERT
    PI_CORE_ASSERT(False, "ImGui-Docking branch is not present.")
# -------------------------------------------------------------------

#-------------------------------------------------------------------
# Instrumentation
def _Ins_EmptyFunc(name: str=""): pass

PI_INSTRUMENTATION_BEGIN_SESSION = _Ins_EmptyFunc
PI_INSTRUMENTATION_END_SESSION   = _Ins_EmptyFunc
PI_TIMER = _Ins_EmptyFunc

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

from functools import wraps
from typing    import Callable
def Timer(func: Callable, name: str=None) -> Callable:
    @wraps(func)
    def TimerWarpper(*args, **kwargs):
        _name = name if name is not None else func.__name__
        timer =  PI_TIMER(_name)
        func(*args, **kwargs)

    return TimerWarpper
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# Other basic utility functions and classes
# Base PI class

# Built-in Math Library
class Math:
    @staticmethod
    def PythonInt32ToBytes( value: int   , byteorder='big' ) -> bytes: return value.to_bytes(4, byteorder)
    @staticmethod
    def BytesToPythonInt32( value: bytes , byteorder='big' ) -> bytes: return int.from_bytes(value, byteorder)

# In-Built Random module
import numpy as _np

class Random:
    __BaseAPI = _np.random

    @staticmethod
    def Random(size=None) -> float:
        return Random.__BaseAPI.random(size)

    @staticmethod
    def RandomInt(begin: int, end: int) -> int:
        return Random.__BaseAPI.randint(begin, end)

    @staticmethod
    def GenerateName(base: str) -> str:
        return "{}{}".format(base, Random.RandomInt(0, 100000))
#-------------------------------------------------------------------
