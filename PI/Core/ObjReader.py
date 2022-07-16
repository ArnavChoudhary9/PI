import pywavefront
from ..Logging import PI_CORE_WARN

class OBJReader:
    class __CustomLoggerForPyWavefront:
        @staticmethod
        def warning(msg: str) -> None:
            PI_CORE_WARN(msg)

    @staticmethod
    def Read(path: str):
        pywavefront.parser.logger = OBJReader.__CustomLoggerForPyWavefront
        pywavefront.logger        = OBJReader.__CustomLoggerForPyWavefront
        scene = pywavefront.Wavefront(path, strict=True, collect_faces=True, create_materials=True, cache=False)
        return scene
