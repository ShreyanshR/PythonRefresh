import math
from array import array

class Vector:
    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y
    
    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __repr__(self):
        # the !r is uses to represent the standard respresentation
        #return f"Vector({self.x}, {self.y})"
        class_name = type(self).__name__
        return '{}({!r},{!r})'.format(class_name, *self)
        
    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __add__(self, other):
        x = other.x + self.x
        y = other.y + self.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(scalar * self.x, scalar * self.y)

    def angle(self):
        return math.atan2(self.x, self.y)

    def __format__(self, fmt_spec=''):
        print(fmt_s)