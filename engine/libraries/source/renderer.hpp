#include "matrix.hpp"

using namespace std;
using namespace vectors;
using namespace matrix;

void drawSquareCpp(int *arr, int *color, int frameWidth, Vector3Struct *pos, Vector3Struct *dim) {
    for (int y = -dim->y/2; y < dim->y/2; y++) {
        for (int x = -dim->x/2; x < dim->x/2; x++) {
            int posX = (int)(pos->x + x);
            int posY = (int)(pos->y + y);

            arr[posY*frameWidth + posX + 0] = color[0];
            arr[posY*frameWidth + posX + 1] = color[1];
            arr[posY*frameWidth + posX + 2] = color[2];
        }
    }
}
