from PI import *
from PI.Scripting import *

class Script1(Behaviour):
    def OnAttach(self) -> None: DebugConsole.Warn("This is a warning test.")
    def OnDetach(self) -> None: DebugConsole.Log("Detaching Script1.")

# One file can have multiple scripts
class Script2(Behaviour):
    def OnAttach(self) -> None: DebugConsole.Error("This Error should stop the Editor Preview.")
    def OnDetach(self) -> None: DebugConsole.Log("Detaching Script2.")
