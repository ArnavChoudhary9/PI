#include "matrix.hpp"

using namespace std;
using namespace vectors;
using namespace matrix;

int main() {
    Vector3 v1 = Vector3(1, 3, 1);
    Matrix m1 = Matrix(v1);
    Vector3 v2 = m1.asVector();

    cout << "Hello, World!" << endl << v2 << endl;

    return 0;
}
