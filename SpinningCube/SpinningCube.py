# Hackey Fix for relative path problem
# TODO: Try to remove it later
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Main Code starts from here
from PI import *
from SpinningCubeLayer import CubeLayer

class SpinningCube(PI_Application):
    def __init__(self, name: str, props: WindowProperties=WindowProperties()) -> None:
        super().__init__(name, props=props)
        self._Camera = PerspectiveCamera(45, self._Window.AspectRatio)
        self._LayerStack.PushLayer(CubeLayer(self._Camera))

    def Run(self) -> None:
        runTimer = PI_TIMER("Application::Run")

        while (self._Running):
            updateTimer = PI_TIMER("Application::Update")
            super().Run()

def CreateApp() -> PI_Application:
    return SpinningCube("Spinning Cube", WindowProperties(
        title="Spinning Cube", width=1280, height=720
    ))

App.CreateApplication = CreateApp

if PI_DEBUG:
    # Only for Detailed Profiling
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename="profile.prof")

else:
    main()
