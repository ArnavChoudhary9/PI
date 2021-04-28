#include "renderer.hpp"

extern "C" {
    __declspec(dllexport) void drawSquare(int *arr, int *color, int frameWidth, Vector3Struct *pos, Vector3Struct *dim) { drawSquareCpp(arr, color, frameWidth, pos, dim); }
}
