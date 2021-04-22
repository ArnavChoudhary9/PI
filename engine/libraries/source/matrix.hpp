#include "vectors.hpp"

class Matrix {
    public:
        int columns, rows;
        float **matrix;

        friend std::ostream& operator << (std::ostream&, Matrix&);
};

std::ostream& operator << (std::ostream& dout, Matrix& m) {
    dout << "Test";
    return dout;
}
