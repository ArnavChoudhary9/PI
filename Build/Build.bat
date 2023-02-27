@ECHO OFF

ECHO Starting Build . . .
ECHO Building application

pyinstaller --hidden-import spdlog --hidden-import PIL --hidden-import PIL.Image --hidden-import imgui --hidden-import imgui.integrations.glfw --hidden-import OpenGL --hidden-import yaml --hidden-import pywavefront --hidden-import dataclasses --hidden-import esper --hidden-import pyrr --hidden-import cProfile --hidden-import pstats --hidden-import OpenGL.GL.shaders --hidden-import uuid --hidden-import xmlrpc --hidden-import xmlrpc.server --hidden-import debugpy --hidden-import tkinter --hidden-import tkinter.filedialog "%1\%1.py"

ECHO Copying dependencies . . .
xcopy /s "Build\Essentials" "dist\%1"
copy ".\imgui.ini" "dist\%1\"

mkdir "dist\PI"
xcopy /s /i "PI" "dist\PI"

mkdir "dist\%1\Assets"
xcopy /s /i "Assets" "dist\%1\Assets"

mkdir "dist\%1\Resources"
xcopy /s /i "%1\Resources" "dist\%1\Resources"

mkdir "dist\%1\debugpy"
xcopy /s /i "virtualenv\Lib\site-packages\debugpy" "dist\%1\debugpy"

xcopy /s /i "%1" "dist" /E

@rd /S /Q "Build\%1"
del "dist\%1.py"
del "%1.spec"

ECHO Done!!
PAUSE
