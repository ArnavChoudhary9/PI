import pywavefront
from ..Logging import Log as _Log

class OBJReader:
    class __CustomLoggerForPyWavefront:
        @staticmethod
        def warning(msg: str) -> None:
            _Log.GetCoreLogger().warn(msg)

    @staticmethod
    def Read(path: str):
        pywavefront.parser.logger = OBJReader.__CustomLoggerForPyWavefront
        pywavefront.logger        = OBJReader.__CustomLoggerForPyWavefront
        scene = pywavefront.Wavefront(path, collect_faces=True, create_materials=True)
        return scene
