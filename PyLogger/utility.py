from .console import Console, LogSeverity

def Trace(console: Console, msg: str) -> None:
    console.Log(msg, LogSeverity.Trace)

def Log(console: Console, msg: str) -> None:
    console.Log(msg, LogSeverity.Log)
    
def Warn(console: Console, msg: str) -> None:
    console.Log(msg, LogSeverity.Warn)
    
def Error(console: Console, msg: str) -> None:
    console.Log(msg, LogSeverity.Error)
