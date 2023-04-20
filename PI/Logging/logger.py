from ..Core import PI_LOGGING
from .Log  import Log

from typing import List, Any

# ---------------------------------------------------------
class LogSubcriprtions:
    __Subcribers: List[Any] = []

    @staticmethod
    def Subscribe(obj: Any) -> None:
        if obj in LogSubcriprtions.__Subcribers: return
        LogSubcriprtions.__Subcribers.append(obj)
    @staticmethod
    def Unsubscribe(obj: Any) -> None:
        try: LogSubcriprtions.__Subcribers.remove(obj)
        except Exception as _: pass

    def Trace(msg: str):
        for obj in LogSubcriprtions.__Subcribers: obj.Trace(msg)

    def Info(msg: str) -> None:
        for obj in LogSubcriprtions.__Subcribers: obj.Info(msg)

    def Debug(msg: str) -> None:
        for obj in LogSubcriprtions.__Subcribers: obj.Debug(msg)

    def Warn(msg: str) -> None:
        for obj in LogSubcriprtions.__Subcribers: obj.Warn(msg)

    def Error(msg: str) -> None:
        for obj in LogSubcriprtions.__Subcribers: obj.Error(msg)

    def Critical(msg: str) -> None:
        for obj in LogSubcriprtions.__Subcribers: obj.Critical(msg)
# ---------------------------------------------------------

def _LOG_DoNothingFunc(msg: str, *args) -> None:
    pass

# Core Logging
PI_CORE_TRACE = _LOG_DoNothingFunc
PI_CORE_INFO  = _LOG_DoNothingFunc
PI_CORE_DEBUG = _LOG_DoNothingFunc
PI_CORE_WARN  = _LOG_DoNothingFunc
PI_CORE_ERROR = _LOG_DoNothingFunc
PI_CORE_CRITICAL = _LOG_DoNothingFunc

# Client Logging
def _PI_CLIENT_TRACE    (msg: str, *args) -> None: LogSubcriprtions.Trace    (msg.format(*args))
def _PI_CLIENT_INFO     (msg: str, *args) -> None: LogSubcriprtions.Info     (msg.format(*args))
def _PI_CLIENT_DEBUG    (msg: str, *args) -> None: LogSubcriprtions.Debug    (msg.format(*args))
def _PI_CLIENT_WARN     (msg: str, *args) -> None: LogSubcriprtions.Warn     (msg.format(*args))
def _PI_CLIENT_ERROR    (msg: str, *args) -> None: LogSubcriprtions.Error    (msg.format(*args))
def _PI_CLIENT_CRITICAL (msg: str, *args) -> None: LogSubcriprtions.Critical (msg.format(*args))

# Assert
PI_CORE_ASSERT = _LOG_DoNothingFunc
PI_CLIENT_ASSERT = _LOG_DoNothingFunc

# ------------------------------------------------- #
if PI_LOGGING:
    # Core Logging
    def _PI_CORE_TRACE(msg: str, *args) -> None:
        Log.GetCoreLogger().trace(msg.format(*args))

    def _PI_CORE_INFO(msg: str, *args) -> None:
        Log.GetCoreLogger().info(msg.format(*args))

    def _PI_CORE_DEBUG(msg: str, *args) -> None:
        Log.GetCoreLogger().debug(msg.format(*args))

    def _PI_CORE_WARN(msg: str, *args) -> None:
        Log.GetCoreLogger().warn(msg.format(*args))

    def _PI_CORE_ERROR(msg: str, *args) -> None:
        Log.GetCoreLogger().error(msg.format(*args))

    def _PI_CORE_CRITICAL(msg: str, *args) -> None:
        Log.GetCoreLogger().critical(msg.format(*args))

    # Client Logging
    def _PI_CLIENT_TRACE(msg: str, *args) -> None:
        msg = msg.format(*args)
        LogSubcriprtions.Trace(msg)
        Log.GetClientLogger().trace(msg)

    def _PI_CLIENT_INFO(msg: str, *args) -> None:
        msg = msg.format(*args)
        LogSubcriprtions.Info(msg)
        Log.GetClientLogger().info(msg)

    def _PI_CLIENT_DEBUG(msg: str, *args) -> None:
        msg = msg.format(*args)
        LogSubcriprtions.Debug(msg)
        Log.GetClientLogger().debug(msg)

    def _PI_CLIENT_WARN(msg: str, *args) -> None:
        msg = msg.format(*args)
        LogSubcriprtions.Warn(msg)
        Log.GetClientLogger().warn(msg)

    def _PI_CLIENT_ERROR(msg: str, *args) -> None:
        msg = msg.format(*args)
        LogSubcriprtions.Error(msg)
        Log.GetClientLogger().error(msg)

    def _PI_CLIENT_CRITICAL(msg: str, *args) -> None:
        msg = msg.format(*args)
        LogSubcriprtions.Critical(msg)
        Log.GetClientLogger().critical(msg)

    # Assert
    def _PI_CORE_ASSERT(condition: bool, msg: str, *args) -> None:
        assert condition, PI_CORE_CRITICAL(msg, *args)

    def _PI_CLIENT_ASSERT(condition: bool, msg: str, *args) -> None:
        assert condition, PI_CLIENT_CRITICAL(msg, *args)

    PI_CORE_TRACE = _PI_CORE_TRACE
    PI_CORE_INFO  = _PI_CORE_INFO
    PI_CORE_DEBUG = _PI_CORE_DEBUG
    PI_CORE_WARN  = _PI_CORE_WARN
    PI_CORE_ERROR = _PI_CORE_ERROR
    PI_CORE_CRITICAL = _PI_CORE_CRITICAL

    PI_CLIENT_ASSERT = _PI_CLIENT_ASSERT
    PI_CORE_ASSERT   = _PI_CORE_ASSERT

# They Must be defined for subscription system
PI_CLIENT_TRACE = _PI_CLIENT_TRACE
PI_CLIENT_INFO  = _PI_CLIENT_INFO
PI_CLIENT_DEBUG = _PI_CLIENT_DEBUG
PI_CLIENT_WARN  = _PI_CLIENT_WARN
PI_CLIENT_ERROR = _PI_CLIENT_ERROR
PI_CLIENT_CRITICAL = _PI_CLIENT_CRITICAL
