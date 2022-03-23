# Hackey Fix for relative path problem
# TODO: Try to remove it later
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Main Code starts from here
from Jordan import *
from EditorLayer import EditorLayer

from time import time

frames = 0

class Sandbox(JD_Application):
    def __init__(self, name: str, props: WindowProperties=WindowProperties()) -> None:
        timer = JD_TIMER("Application::Init")
        super().__init__(name, props)
        self._Camera = OrthographicCamera(self._Window.AspectRatio, 1)
        self._LayerStack.PushOverlay(EditorLayer(self._Camera))

    def __del__(self) -> None:
        timer = JD_TIMER("Application::Destroy")
        
        self._Running = False

        del self._LayerStack
        del self._EventDispacher
        del self._Window

    def Run(self) -> None:
        global frames
        runTimer = JD_TIMER("Application::Run")
        
        while (self._Running):
            updateTimer = JD_TIMER("Application::Update")
            super().Run()

            frames += 1
            

def CreateApp() -> Sandbox:
    timer = JD_TIMER("Application::Create")
    return Sandbox("Sandbox", WindowProperties("Sandbox", 1200, 600))
    
App.CreateApplication = CreateApp

start = time()
main()
print("Average FPS: {}".format( frames / (time() - start) ))
