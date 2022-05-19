# Hackey Fix for relative path problem
# TODO: Try to remove it later
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Main Code starts from here
from PI import *
from EditorLayer import EditorLayer

class Theta(PI_Application):
    def __init__(self, name: str, props: WindowProperties=WindowProperties()) -> None:
        super().__init__(name, props=props)
        self._LayerStack.PushLayer(EditorLayer())

    def Run(self) -> None:
        runTimer = PI_TIMER("Theta::Run")

        while (self._Running):
            updateTimer = PI_TIMER("Theta::Update")
            super().Run()

def CreateApp() -> PI_Application:
    return Theta("Theta", WindowProperties(
        title="Theta: PI Editor", width=1280, height=720
    ))

App.CreateApplication = CreateApp
main()
