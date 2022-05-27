import importlib
import os
def ImportClass(path: str, error: bool=True):
    '''
    This Function returns the class of matching name to filename.
    NOTE: File shiuld be in some folder else it will not work.
    '''
    if error and not os.path.exists(path): raise ImportError("Invalid path to file")
    path = path.replace("\\", "/")
    if not path.startswith("./"): path = "./" + path
    path: list = path.split("/")[1:]

    package = ".".join(path[:-1])
    _className = path[-1][:-3]
    module  = "." + _className
    module  = importlib.import_module(module, package)

    _class = module.__dict__.get(_className, None)
    if error and _class is None: raise ImportError("There is no class matching filename in this file.")
    return _className, _class
