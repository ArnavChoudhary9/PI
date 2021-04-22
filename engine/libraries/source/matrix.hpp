#include "vectors.hpp"

namespace matrix
{
    class Matrix {
        public:
            int columns, rows;
            float **matrix;

            Matrix(int, int);
            Matrix(int, int, float);

            Matrix operator + (float);
            void operator += (float);

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

    Matrix Matrix::operator + (float scaler) {
        Matrix m = Matrix(columns, rows);

        for (int x = 0; x < columns; x++) {
            for (int y = 0; y < rows; y++) {
                m.matrix[x][y] = matrix[x][y] + scaler;
            }
        }
        
        return m;
    }

    std::ostream& operator << (std::ostream& dout, Matrix& m) {
        dout << "<Matrix> :\n[";

        for (int x = 0; x < m.columns; x++) {
            if (x != 0)
                dout << " ";
            dout << "[";

            for (int y = 0; y < m.rows; y++) {
                dout << m.matrix[x][y];

                if (y != m.rows-1)
                    dout << " ";
            }
            dout << "]";

            if (x != m.columns-1)
                dout << "\n";
        }

        dout << "]";        
        return dout;
    }
}
