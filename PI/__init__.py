from .Core        import *
from .Core.App    import *
from .Core.Input  import *
from .Core.Window import *

from .Events import *
from .Layers import *

from .ImGui import *

from .Platform import *
from .Renderer import *

from .Scene     import *
from .Scripting import *
from .Projects  import *

from .AssetManager import *

from .Logging import *

from .ButtonCodes import *

from .Utility import *

import pyrr

import imgui
from imgui import Vec2 as ImVec2
from imgui import Vec4 as ImVec4

from typing import Tuple, List, Any, Callable, Iterable

from numpy import degrees as ArrayToDegrees
from numpy import radians as ArrayToRadians

import pathlib

def Vector3ToRadians(vector3Like) -> pyrr.Vector3:
    if not isinstance(vector3Like, pyrr.Vector3): vector3Like = pyrr.Vector3(vector3Like)
    return pyrr.Vector3(ArrayToRadians(vector3Like))

if PI_LOGGING:
    Log.Init()

# Currently We only support Windows with OpenGL
# Cause this is all what The Cherno taught me.
if (CURRENT_PLATFORM == "Windows"):
    Window.SetOS(OS.Windows)
