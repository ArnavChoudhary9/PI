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

            static Matrix dot(Matrix&);

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
