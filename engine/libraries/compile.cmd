@echo off

echo Compiling...

echo Making Object files...
g++ -c -fPIC "source\renderer.cpp" -O2 -o "bin-int\renderer.o"

echo Making dll's...
g++ -shared -Wl,-soname,"bin\renderer.dll" -O2 -o "bin\renderer.dll" "bin-int\renderer.o"

echo Copying...
copy "bin\renderer.dll"

echo Done

Pause
