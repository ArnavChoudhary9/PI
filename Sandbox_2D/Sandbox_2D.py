# Hackey Fix for relative path problem
# TODO: Try to remove it later
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Main Code starts from here
from PI import *
from Sandbox2DLayer import Sandbox2D

class Sandbox2DApp(PI_Application):
    def __init__(self, name: str, props: WindowProperties=WindowProperties()) -> None:
        timer = PI_TIMER("Sandbox2DApp::Init")
        super().__init__(name, props)

        self._LayerStack.PushLayer(Sandbox2D())

    def Run(self) -> None:
        runTimer = PI_TIMER("Sandbox2DApp::Run")
        
        while (self._Running):
            updateTimer = PI_TIMER("Sandbox2DApp::Update")
            super().Run()

def CreateApp() -> Sandbox2DApp:
    timer = PI_TIMER("Sandbox2DApp::Create")
    return Sandbox2DApp("Sandbox2DApp", WindowProperties("Sandbox2DApp", 1200, 600))
    
App.CreateApplication = CreateApp
main()
