#include "vectors.hpp"

namespace matrix
{
    class Matrix {
        public:
            int columns, rows;
            float **matrix;

            Matrix(int, int);
            Matrix(int, int, float);

            Matrix(vectors::Vector3&);
            vectors::Vector3 asVector();

            Matrix operator*(Matrix&);

            void setValue(int, int, float);
            float getValue(int, int);

            static Matrix dot(Matrix&, Matrix&);

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

    Matrix::Matrix(vectors::Vector3& v) : columns{3}, rows{1} {
        matrix = new float *[3];

        matrix[0] = new float[1];
        matrix[0][0] = v.x;

        matrix[1] = new float[1];
        matrix[1][0] = v.y;

        matrix[2] = new float[1];
        matrix[2][0] = v.z;
    }

    vectors::Vector3 Matrix::asVector() {
        if (columns == 3 && rows == 1)
            return vectors::Vector3(matrix[0][0], matrix[1][0], matrix[2][0]);

        return vectors::Vector3();
    }

    Matrix Matrix::operator*(Matrix& m) {
        Matrix _m = Matrix::dot((*this), m);
        return _m;
    }

    void Matrix::setValue(int x, int y, float value) {
        matrix[x][y] = value;
    }

    float Matrix::getValue(int x, int y) {
        return matrix[x][y];
    }

    Matrix Matrix::dot(Matrix& m1, Matrix& m2) {
        Matrix m = Matrix(m1.columns, m2.rows);

        for (int i = 0; i < m1.rows; i++) {
            for (int j = 0; j < m2.columns; j++) {
                for (int k = 0; k < m1.columns; k++) {
                    m.matrix[i][j] += m1.matrix[i][k] * m2.matrix[k][j];
                }
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
