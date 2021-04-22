import numpy as np
from .matrix import Matrix

class Vector3:
    x = 0
    y = 0
    z = 0

    def __init__(self, x: float=0, y: float=0, z: float=0):
        self.x = x
        self.y = y
        self.z = z

    # Properties
    @property
    def array(self):
        return np.array([self.x, self.y, self.z])
    
    @property
    def magnitude(self):
        return np.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    @property
    def magnitudeSqr(self):
        return self.x*self.x + self.y*self.y + self.z*self.z

    @property
    def normalized(self):
        v = Vector3(self.x, self.y, self.z)
        v.normalize()
        return v

    # Dot and Cross products
    @staticmethod
    def dot(v1, v2):
        return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z

    @staticmethod
    def cross(v1, v2):
        v = Vector3()

        v.x = v1.y*v2.z - v1.z*v2.y
        v.y = v1.z*v2.y - v1.x*v2.z
        v.z = v1.x*v2.y - v1.y*v2.x

        return v

    # Matrix
    @property
    def matrix(self):
        m = Matrix(3, 1, 0)

        m[0] = self.x
        m[1] = self.x
        m[2] = self.x

    # Math
    def scale(self, scaler):
        self.x *= scaler
        self.y *= scaler
        self.z *= scaler
    
    def normalize(self):
        self *= 1 / self.magnitude

    def distance(self, other):
        xdist = (other.x-self.x)*(other.x-self.x)
        ydist = (other.y-self.y)*(other.y-self.y)
        zdist = (other.z-self.z)*(other.z-self.z)

        return np.sqrt(xdist + ydist + zdist)

    def distanceSqr(self, other):
        xdist = (other.x-self.x)*(other.x-self.x)
        ydist = (other.y-self.y)*(other.y-self.y)
        zdist = (other.z-self.z)*(other.z-self.z)

        return xdist + ydist + zdist

    def setMegnitude(self, meg):
        self.normalize()
        self *= meg

    def __add__(self, other):
        v = Vector3()

        v.x = self.x + other.x
        v.y = self.y + other.y
        v.z = self.z + other.z
        
        return v

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z

        return self

    def __sub__(self, other):
        v = Vector3()

        v.x = self.x - other.x
        v.y = self.y - other.y
        v.z = self.z - other.z
        
        return v

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

        return self

    def __mul__(self, other):
        v = Vector3()

        if type(other) in [float, int, np.float64]:
            v.x = self.x
            v.y = self.y
            v.z = self.z

            v.scale(other)

        elif type(other) in [tuple, list, np.ndarray] and np.array(other).shape == (3,):
            _v = Vector3(other[0], other[1], other[2])
            v = Vector3.dot(self, _v)

        elif type(other) == Vector3:
            v = Vector3.dot(self, other)

        else:
            raise NotImplementedError("This type of Vector multiplication is not implimented yet.")

        return v

    def __imul__(self, other):
        if type(other) in [float, int, np.float64]:
            self.scale(other)
        
        elif type(other) in [tuple, list, np.ndarray] and np.array(other).shape == (3,):
            v = Vector3(other[0], other[1], other[2])
            self = Vector3.dot(self, v)

        elif type(other) == Vector3:
            self = Vector3.dot(self, other)

        else:
            raise NotImplementedError("This type of Vector multiplication is not implimented yet.")
            
        return self

    # Conversion        
    def __repr__(self):
        return "<Vector3 at {}>: {}i + {}j + {}k".format(hex(id(self)), self.x, self.y, self.z)

    @staticmethod
    def fromMatrix(matrix):
        return Vector3(matrix.matrix[0][0], matrix.matrix[1][0], matrix.matrix[2][0])
