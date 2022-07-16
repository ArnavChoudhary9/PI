from PI import *
from PI.Scripting import *

class FallDown(Behaviour):
    TestVariable : pyrr.Vector3 = pyrr.Vector3([ 0, -0.1, 0 ])

    def OnUpdate(self, dt: float) -> None:
        self._Transform.Translate(self.TestVariable * dt)
