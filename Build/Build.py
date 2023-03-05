import sys
import o

PyInstaller.__main__.run((
    "--collect-all PIL",
    "--collect-all imgui",
    "--collect-all OpenGL",
    "--collect-all tkinter",
    "--collect-all debugpy",
    "--collect-all xmlrpc",

    "--hidden-import spdlog",
    "--hidden-import yaml",
    "--hidden-import pywavefront",
    "--hidden-import dataclasses",
    "--hidden-import esper",
    "--hidden-import pyrr",
    "--hidden-import cProfile",
    "--hidden-import pstats",
    "--hidden-import uuid",

    f"{sys.argv[1]}\\{sys.argv[1]}.py"
))
