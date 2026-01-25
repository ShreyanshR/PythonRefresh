import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        # the !r is uses to represent the standard respresentation
        #return f"Vector({self.x}, {self.y})"
        return f"Vector({self.x!r}, {self.y!r})"
        
    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = other.x + self.x
        y = other.y + self.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(scalar * self.x, scalar * self.y)