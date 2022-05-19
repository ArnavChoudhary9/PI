from ..Core import *
import spdlog

class Log:
    __slots__ = "__CoreLogger", "__ClientLogger"

    @staticmethod
    def Init() -> None:
        logSinks = [
            spdlog.stdout_color_sink_mt(),
            spdlog.basic_file_sink_mt("PI.log", True)
        ]
        
	    # TODO: Set File logger pattern to -> "[%T] [%l] %n: %v"

        Log.__CoreLogger = spdlog.SinkLogger("PI", logSinks)
        Log.__CoreLogger.set_pattern("%^[%T] %n: %v%$")
        Log.__CoreLogger.set_level(spdlog.LogLevel.TRACE)
        Log.__CoreLogger.flush_on(spdlog.LogLevel.TRACE)

        Log.__ClientLogger = spdlog.SinkLogger("Client", logSinks)
        Log.__ClientLogger.set_pattern("%^[%T] %n: %v%$")
        Log.__ClientLogger.set_level(spdlog.LogLevel.TRACE)
        Log.__ClientLogger.flush_on(spdlog.LogLevel.TRACE)

    @staticmethod
    def GetCoreLogger() -> spdlog.Logger:
        return Log.__CoreLogger

    @staticmethod
    def GetClientLogger() -> spdlog.Logger:
        return Log.__ClientLogger
