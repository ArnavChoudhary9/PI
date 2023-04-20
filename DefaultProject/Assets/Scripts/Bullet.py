from PI import *
from PI.Scripting import *

class Bullet(Behaviour):
    Time: float = 1
    def OnUpdate(self, dt: float) -> None:
        self.Time -= dt
        if self.Time < 0.0: self.Destroy()
