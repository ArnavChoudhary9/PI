from ..Core import PI_LOGGING
from .Log  import Log

def DoNothingFunc(msg: str, *args) -> None:
    pass

# Core Logging
PI_CORE_TRACE = DoNothingFunc
PI_CORE_INFO  = DoNothingFunc
PI_CORE_DEBUG = DoNothingFunc
PI_CORE_WARN  = DoNothingFunc
PI_CORE_ERROR = DoNothingFunc
PI_CORE_CRITICAL = DoNothingFunc

# Client Logging
PI_CLIENT_TRACE = DoNothingFunc
PI_CLIENT_INFO  = DoNothingFunc
PI_CLIENT_DEBUG = DoNothingFunc
PI_CLIENT_WARN  = DoNothingFunc
PI_CLIENT_ERROR = DoNothingFunc
PI_CLIENT_CRITICAL = DoNothingFunc

# # Assert
PI_CORE_ASSERT = DoNothingFunc

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
        Log.GetClientLogger().trace(msg.format(*args))

    def _PI_CLIENT_INFO(msg: str, *args) -> None:
        Log.GetClientLogger().info(msg.format(*args))

    def _PI_CLIENT_DEBUG(msg: str, *args) -> None:
        Log.GetClientLogger().debug(msg.format(*args))

    def _PI_CLIENT_WARN(msg: str, *args) -> None:
        Log.GetClientLogger().warn(msg.format(*args))

    def _PI_CLIENT_ERROR(msg: str, *args) -> None:
        Log.GetClientLogger().error(msg.format(*args))

    def _PI_CLIENT_CRITICAL(msg: str, *args) -> None:
        Log.GetClientLogger().critical(msg.format(*args))

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
    
    PI_CLIENT_TRACE = _PI_CLIENT_TRACE
    PI_CLIENT_INFO  = _PI_CLIENT_INFO
    PI_CLIENT_DEBUG = _PI_CLIENT_DEBUG
    PI_CLIENT_WARN  = _PI_CLIENT_WARN
    PI_CLIENT_ERROR = _PI_CLIENT_ERROR
    PI_CLIENT_CRITICAL = _PI_CLIENT_CRITICAL

    PI_CLIENT_ASSERT = _PI_CLIENT_ASSERT
    PI_CORE_ASSERT   = _PI_CORE_ASSERT
