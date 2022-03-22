from .Core import JD_LOGGING
from .Log  import Log

def DoNothingFunc(msg: str, *args) -> None:
    pass

# Core Logging
JD_CORE_TRACE = DoNothingFunc
JD_CORE_INFO = DoNothingFunc
JD_CORE_DEBUG = DoNothingFunc
JD_CORE_WARN = DoNothingFunc
JD_CORE_ERROR = DoNothingFunc

# Client Logging
JD_CLIENT_TRACE = DoNothingFunc
JD_CLIENT_INFO = DoNothingFunc
JD_CLIENT_DEBUG = DoNothingFunc
JD_CLIENT_WARN = DoNothingFunc
JD_CLIENT_ERROR = DoNothingFunc

# # Assert
JD_CORE_ASSERT = DoNothingFunc

# ------------------------------------------------- #
if JD_LOGGING:
    # Core Logging
    def _JD_CORE_TRACE(msg: str, *args) -> None:
        Log.GetCoreLogger().trace(msg.format(*args))

    def _JD_CORE_INFO(msg: str, *args) -> None:
        Log.GetCoreLogger().info(msg.format(*args))

    def _JD_CORE_DEBUG(msg: str, *args) -> None:
        Log.GetCoreLogger().debug(msg.format(*args))

    def _JD_CORE_WARN(msg: str, *args) -> None:
        Log.GetCoreLogger().warn(msg.format(*args))

    def _JD_CORE_ERROR(msg: str, *args) -> None:
        Log.GetCoreLogger().error(msg.format(*args))

    # Client Logging
    def _JD_CLIENT_TRACE(msg: str, *args) -> None:
        Log.GetClientLogger().trace(msg.format(*args))

    def _JD_CLIENT_INFO(msg: str, *args) -> None:
        Log.GetClientLogger().info(msg.format(*args))

    def _JD_CLIENT_DEBUG(msg: str, *args) -> None:
        Log.GetClientLogger().debug(msg.format(*args))

    def _JD_CLIENT_WARN(msg: str, *args) -> None:
        Log.GetClientLogger().warn(msg.format(*args))

    def _JD_CLIENT_ERROR(msg: str, *args) -> None:
        Log.GetClientLogger().error(msg.format(*args))

    # Assert
    def _JD_CORE_ASSERT(condition: bool, msg: str, *args) -> None:
        assert condition, JD_CORE_ERROR(msg, *args)

    JD_CORE_TRACE = _JD_CORE_TRACE
    JD_CORE_INFO = _JD_CORE_INFO
    JD_CORE_DEBUG = _JD_CORE_DEBUG
    JD_CORE_WARN = _JD_CORE_WARN
    JD_CORE_ERROR = _JD_CORE_ERROR
    
    JD_CLIENT_TRACE = _JD_CLIENT_TRACE
    JD_CLIENT_INFO = _JD_CLIENT_INFO
    JD_CLIENT_DEBUG = _JD_CLIENT_DEBUG
    JD_CLIENT_WARN = _JD_CLIENT_WARN
    JD_CLIENT_ERROR = _JD_CLIENT_ERROR

    JD_CORE_ASSERT = _JD_CORE_ASSERT
