// #include <iostream>
#include "matrix.hpp"

using namespace std;
using namespace vectors;
using namespace matrix;

int main() {
    Matrix m1 = Matrix(5, 5, 5);
    Matrix m2 = m1;

    cout << "Hello, World!" << endl << m2 << endl;

    return 0;
}
