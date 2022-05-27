from PI import *
from PI.Scripting import *

class TestScript(Behaviour):
    def OnAttach(self) -> None:
        self.TestStr    = "Test Str"
        self.TestFloat  = 0.0
        self.TestInt    = 5
        self.TestBool   = False
        self.TestVector = pyrr.Vector3([ 1, 0, 3 ])
        self.TestColor  = Color4([ 1, 1, 1, 1 ])
