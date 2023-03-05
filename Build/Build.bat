@ECHO OFF

ECHO Starting Build . . .
ECHO Building application

pyinstaller --collect-all PI --collect-all Theta --collect-all PIL --collect-all imgui --collect-all OpenGL --collect-all tkinter --collect-all debugpy --collect-all xmlrpc --collect-all importlib --hidden-import spdlog --hidden-import yaml --hidden-import pywavefront --hidden-import dataclasses --hidden-import esper --hidden-import pyrr --hidden-import cProfile --hidden-import pstats --hidden-import uuid "%1\%1.py"

ECHO Copying dependencies . . .
xcopy /s "Build\Essentials" "dist\%1"
copy ".\imgui.ini" "dist\%1\"

mkdir "dist\PI"
xcopy /s /i "PI" "dist\PI"

mkdir "dist\%1\Assets"
xcopy /s /i "Assets" "dist\%1\Assets"

mkdir "dist\%1\Resources"
xcopy /s /i "%1\Resources" "dist\%1\Resources"

xcopy /s /i "%1" "dist" /E

@rd /S /Q "Build\%1"
del "dist\%1.py"
del "%1.spec"

ECHO Done!!
PAUSE
