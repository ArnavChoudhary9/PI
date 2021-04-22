#include "vectors.hpp"

namespace matrix
{
    class Matrix {
        public:
            int columns, rows;
            float **matrix;

            Matrix(int, int);
            Matrix(int, int, float);

            friend std::ostream& operator << (std::ostream&, Matrix&);
    };

    Matrix::Matrix(int _columns, int _rows) : columns{_columns}, rows{_rows} {
        matrix = new float *[columns];

        for (int x = 0; x < columns; x++) {
            matrix[x] = new float[rows];

            for (int y = 0; y < rows; y++) {
                matrix[x][y] = 0;
            }
        }
    }

    Matrix::Matrix(int _columns, int _rows, float filler) : columns{_columns}, rows{_rows} {
        matrix = new float *[columns];

        for (int x = 0; x < columns; x++) {
            matrix[x] = new float[rows];

            for (int y = 0; y < rows; y++) {
                matrix[x][y] = filler;
            }
        }
    }

    std::ostream& operator << (std::ostream& dout, Matrix& m) {
        
        for (int x = 0; x < m.columns; x++) {
            for (int y = 0; y < m.rows; y++) {
                dout << m.matrix[x][y] << " ";
            }
            dout << "\n";
        }
        
        return dout;
    }
}
