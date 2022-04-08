# Hackey Fix for relative path problem
# TODO: Try to remove it later
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Main Code starts from here
from PI import *
from ExampleLayer import ExampleLayer
from Sandbox2D    import Sandbox2D

class Sandbox(PI_Application):
    def __init__(self, name: str, props: WindowProperties=WindowProperties()) -> None:
        timer = PI_TIMER("Application::Init")
        super().__init__(name, props)
        self._Camera = OrthographicCamera(self._Window.AspectRatio, 1)

        self._LayerStack.PushLayer(ExampleLayer(self._Camera))
        # self._LayerStack.PushLayer(Sandbox2D(self._Camera))

    def Run(self) -> None:
        runTimer = PI_TIMER("Application::Run")
        
        while (self._Running):
            updateTimer = PI_TIMER("Application::Update")
            super().Run()

def CreateApp() -> Sandbox:
    timer = PI_TIMER("Application::Create")
    return Sandbox("Sandbox", WindowProperties("Sandbox", 1200, 600))
    
App.CreateApplication = CreateApp
main()

# Only for Detailed Profiling
# import cProfile
# import pstats

# with cProfile.Profile() as pr:
#     main()

# stats = pstats.Stats(pr)
# stats.sort_stats(pstats.SortKey.TIME)
# stats.dump_stats(filename="profile.prof")
