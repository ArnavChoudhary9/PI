from PI import *
from PI.Scripting import *

class InstanciationTest(Behaviour):
    __Timer: float

    def OnAttach(self) -> None:
        self.__Timer = 0.0

    def OnUpdate(self, dt: float) -> None:
        if self.__Timer > 1:
            self.__Timer = 0.0
            entity = self.InstanciateEntity("TestEntity")
            entity.AddComponent(ScriptComponent, "InstanciationTest", "InstanciationTest")

        self.__Timer += dt
