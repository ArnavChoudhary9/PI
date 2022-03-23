@ECHO OFF

ECHO Starting Build . . .
ECHO Building application

pyinstaller --hidden-import spdlog --hidden-import imgui --hidden-import imgui.integrations.glfw --hidden-import OpenGL --hidden-import pyrr --hidden-import OpenGL.GL.shaders -i "%2" "%1\%1.py"

ECHO Copying dependencies . . .
xcopy /s "Build\Essentials" "dist\%1"

mkdir "dist\Jordan"
xcopy /s /i "Jordan" "dist\Jordan"

mkdir "dist\%1\Assets"
xcopy /s /i "Assets" "dist\%1\Assets"

xcopy /s /i "%1" "dist" /E

@rd /S /Q "Build\%1"
del "dist\%1\%1.py"
del "%1.spec"

ECHO Done!!
PAUSE
