from .Core     import *
from .Core.App import *

from .Events import *
from .Layers import *

from .Input import *
from .ImGui import *

from .Platform import *
from .Renderer import *

from .Log      import *
from .logger   import *

from .KeyCodes         import *
from .MouseButtonCodes import *

from .Window import *

import pyrr
import imgui

from math import radians, degrees

if PI_LOGGING:
    Log.Init()

# Currently We only support Windows with OpenGL
# Cause this is all what The Cherno taught me.
if (CURRENT_PLATFORM == "Windows"):
    Window.SetOS(OS.Windows)

Renderer.Init()
Input.Init()
