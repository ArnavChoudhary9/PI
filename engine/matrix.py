import numpy as np

class Matrix:
    rows = 0
    columns = 0

    matrix = []

    def __init__(self, columns: int=1, rows: int=1, filler: float=0):
        self.rows = rows
        self.columns = columns
        self.matrix = np.array([[filler for __ in range(rows)] for _ in range(columns)])

    def setElement(self, x, y, value):
        self.matrix[x][y] = value

    def getElement(self, x, y):
        return self.matrix[x][y]

    @staticmethod
    def dot(a, b):       
        if b.columns != a.rows:
            raise ValueError("Columns of first matrix should match the number of rows of the second")

        a = a.matrix
        b = b.matrix

        mat = np.dot(a, b)
        m = Matrix(mat.shape[0], mat.shape[1])

        for x in range(mat.shape[0]):
            for y in range(mat.shape[1]):
                m.setElement(x, y, mat[x][y])

        return m

    def scale(self, scaler):
        for x in range(self.columns):
            for y in range(self.rows):
                self.matrix[x][y] *= scaler

    def __repr__(self):
        return "<Matrix at {}>\n".format(hex(id(self))) + str(self.matrix)
