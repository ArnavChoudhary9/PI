from .Core import *
import spdlog

class Log:
    __CoreLogger   : spdlog.ConsoleLogger
    __ClientLogger : spdlog.ConsoleLogger

    @staticmethod
    def Init() -> None:
        Log.__CoreLogger   = spdlog.ConsoleLogger("Core"   , multithreaded=True)
        Log.__CoreLogger.set_pattern("%^[%T] %n: %v%$")
        Log.__CoreLogger.set_level(spdlog.LogLevel.TRACE)

        Log.__ClientLogger = spdlog.ConsoleLogger("Client" , multithreaded=True)
        Log.__ClientLogger .set_pattern("%^[%T] %n: %v%$")
        Log.__ClientLogger.set_level(spdlog.LogLevel.TRACE)

    @staticmethod
    def GetCoreLogger() -> spdlog.Logger:
        return Log.__CoreLogger

    @staticmethod
    def GetClientLogger() -> spdlog.Logger:
        return Log.__ClientLogger
