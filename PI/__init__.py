from .Core       import *
from .Core.App   import *
from .Core.Input import *
from .Core.Window import *

from .Events import *
from .Layers import *

from .ImGui import *

from .Platform import *
from .Renderer import *

from .Logging import *

from .ButtonCodes import *

import pyrr
import imgui

from numpy import degrees, radians

if PI_LOGGING:
    Log.Init()

# Currently We only support Windows with OpenGL
# Cause this is all what The Cherno taught me.
if (CURRENT_PLATFORM == "Windows"):
    Window.SetOS(OS.Windows)
