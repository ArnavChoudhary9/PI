import numpy as np

class Color():
    def __init__(self, x: int=0, y: int=0, z: int=0):
        if x < 0:
            x = 0
        elif x > 255:
            x = 255
            
        if y < 0:
            y = 0
        elif y > 255:
            y = 255
            
        if z < 0:
            z = 0
        elif z > 255:
            z = 255

        self.x = x
        self.y = y
        self.z = z

    @property
    def array(self):
        return np.array([self.x, self.y, self.z])
