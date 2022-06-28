@ECHO OFF

ECHO Starting Build . . .
ECHO Building application

pyinstaller --hidden-import spdlog --hidden-import PIL --hidden-import imgui --hidden-import imgui.integrations.glfw --hidden-import OpenGL --hidden-import yaml --hidden-import pywavefront --hidden-import dataclasses --hidden-import esper --hidden-import pyrr --hidden-import cProfile --hidden-import pstats --hidden-import OpenGL.GL.shaders "%1\%1.py"

ECHO Copying dependencies . . .
xcopy /s "Build\Essentials" "dist\%1"
copy ".\imgui.ini" "dist\%1\"

mkdir "dist\PI"
xcopy /s /i "PI" "dist\PI"

mkdir "dist\%1\Assets"
xcopy /s /i "Assets" "dist\%1\Assets"

xcopy /s /i "%1" "dist" /E

@rd /S /Q "Build\%1"
del "dist\%1.py"
del "%1.spec"

ECHO Done!!
PAUSE
