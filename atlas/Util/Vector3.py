"""
Vector3.py: Contains a collection of functions that aid in the 
various movements of the entities in our world.
"""

import math

class Vector3(object):
    def __init__(self, **kwargs):
        self.x = float(kwargs.get('x', 0))
        self.y = float(kwargs.get('y', 0))
        self.z = float(kwargs.get('z', 0))

    def rotateZ(self, angle):
        """
        Returns a new Vector3 that is rotated from the vector clockwise by the angle given, in degrees.
        """
        x = self.x
        y = self.y
        angle = math.radians(angle)
        cosa = math.cos(angle)
        sina = math.sin(angle )

        return Vector3(x = x * cosa - y * sina, y = x * sina + y * cosa, z=1)

    # expects radians
    def rotateZ_self(self, angle):
        """
        Rotates the vector clockwise by the angle given, in degrees.
        """
        x = self.x
        y = self.y
        angle = math.radians(angle)
        cosa = math.cos(angle)
        sina = math.sin(angle)
        self.x = x * cosa - y * sina
        self.y = x * sina + y * cosa
        self.z = 1
        return self

    def angle_between(self, v3):
        """
        Returns the angle between the vector and another vector given, in degrees.
        """
        dot = self.dot_product(v3)
        origin = Vector3(x=0, y=0, z=0)
        d1 = self.distance_between(origin)
        d2 = v3.distance_between(origin)
        d_product = d1 * d2
        dot = dot / d_product
        dot = min(1, max(dot, -1))
        acos = math.acos(dot)
        return math.degrees(acos)

    def dot_product(self, v3):
        """
        Returns the dot product of the vector with another vector.
        """
        return self.x * v3.x + self.y * v3.y + self.z * v3.z

    def distance_between(self, v3):
        """
        Returns the distance between the vector and another vector.
        """
        dx = self.x - v3.x
        dy = self.y - v3.y
        return math.sqrt(dx * dx + dy * dy)

    def add(self, v3):
        """
        Returns a new Vector3 that is equal to the addition of the vector with another.
        """
        return Vector3(x=self.x + v3.x, y=self.y + v3.y)

    def add_self(self, v3):
        """
        Adds the vector given to the vector.
        """
        self.x += v3.x
        self.y += v3.y
        self.z += v3.z

        return self

    def subtract(self, v3):
        """
        Returns a new Vector3 that is equal to the subtraction of the vector with another.
        """
        return Vector3(x=self.x - v3.x, y=self.y - v3.y, z=self.z - v3.z)

    def length(self):
        """
        Returns the length of the vector, from the origin.
        """
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def multiply_scalar(self, scalar):
        """
        Returns a new Vector3 that is the result of the product of the scalar given and the vector.
        """
        return Vector3(x=self.x * scalar, y=self.y * scalar, z=self.z * scalar)

    def multiply_scalar_self(self, scalar):
        """
        Multiplies the vector by the scalar given.
        """
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar

        return self

    def divide_scalar(self, scalar):
        """
        Returns a new Vector3 that is the result of the division of the vector by the scalar given.
        """
        if scalar != 0:
            x = float(self.x) / scalar
            y = float(self.y) / scalar
            z = float(self.z) / scalar
            return Vector3(x=x, y=y, z=z)
        else:
            return Vector3(x=0, y=0, z=0)

    def divide_scalar_self(self, scalar):
        """
        Divides the vector by the given scalar.
        """
        if scalar != 0:
            self.x = float(self.x) / scalar
            self.y = float(self.y) / scalar
            self.z = float(self.z) / scalar
        else:
            self.x = 0
            self.y = 0
            self.z = 0

        return self

    def normalize(self):
        """
        Normalizes the vector
        """
        return self.divide_scalar_self(self.length())

    def equal(self, v3):
        """
        Returns true if both the vector and the vector3 given are equal.
        """
        return self.x == v3.x and self.y == v3.y and self.z == v3.z

    def cross(self, v3, debug=False):
        """
        Returns the cross product of the vector with the given vector.
        """
        return Vector3(x=self.y * v3.z - self.z * v3.y, 
                       y=self.z * v3.x - self.x * v3.z, 
                       z=self.x * v3.y - self.y * v3.x)

    def clamp(self, maximum=1000000, minimum=-1000000):

        self.x = max(minimum, self.x)
        self.x = min(maximum, self.x)
        self.y = max(minimum, self.y)
        self.y = min(maximum, self.y)
        self.z = max(minimum, self.z)
        self.z = min(maximum, self.z)
        
        return self
    
    def clean(self, threshhold=.01):
        self.x = 0 if self.x in xrange(-threshhold, threshhold) else self.x
        self.y = 0 if self.y in xrange(-threshhold, threshhold) else self.y
        self.z = 0 if self.z in xrange(-threshhold, threshhold) else self.z

    def __repr__(self):
        return "(%f, %f, %f)" % (self.x, self.y, self.z)

def vector3_from_vector2(v2):
    return Vector3(x=v2.x, y=v2.y, z=1)
