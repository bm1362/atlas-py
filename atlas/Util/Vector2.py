"""
Vector2.py: Contains a collection of functions that aid in the 
various movements of the entities in our world.
"""

import math

class Vector2(object):
    def __init__(self, **kwargs):
        self.x = float(kwargs.get('x', 0))
        self.y = float(kwargs.get('y', 0))

    def rotate(self, angle):
        """
        Returns a new Vector2 that is rotated from the vector clockwise by the angle given, in degrees.
        """
        x = self.x
        y = self.y
        angle = math.radians(angle)
        cosa = math.cos(angle)
        sina = math.sin(angle )

        return Vector2(x = x * cosa - y * sina, y = x * sina + y * cosa)

    # expects radians
    def rotate_self(self, angle):
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
        return self

    def angle_between(self, v2):
        """
        Returns the angle between the vector and another vector given, in degrees.
        """
        dot = self.dot_product(v2)
        origin = Vector2(x=0, y=0)
        d1 = self.distance_between(origin)
        d2 = v2.distance_between(origin)
        d_product = d1 * d2
        dot = dot / d_product
        dot = min(1, max(dot, -1))
        acos = math.acos(dot)
        return math.degrees(acos)

    def dot_product(self, v2):
        """
        Returns the dot product of the vector with another vector.
        """
        return self.x * v2.x + self.y * v2.y

    def distance_between(self, v2):
        """
        Returns the distance between the vector and another vector.
        """
        dx = self.x - v2.x
        dy = self.y - v2.y
        return math.sqrt(dx * dx + dy * dy)

    def add(self, v2):
        """
        Returns a new Vector2 that is equal to the addition of the vector with another.
        """
        return Vector2(x=self.x + v2.x, y=self.y + v2.y)

    def add_self(self, v2):
        """
        Adds the vector given to the vector.
        """
        self.x += v2.x
        self.y += v2.y

        return self

    def subtract(self, v2):
        """
        Returns a new Vector2 that is equal to the subtraction of the vector with another.
        """
        return Vector2(x=self.x - v2.x, y=self.y - v2.y)

    def subtract_self(self, v2):
        """
        Subtraction of the vector with another.
        """
        self.x -= v2.x
        self.y -= v2.y

        return self

    def length(self):
        """
        Returns the length of the vector, from the origin.
        """
        return math.sqrt(self.x * self.x + self.y * self.y)

    def multiply_scalar(self, scalar):
        """
        Returns a new Vector2 that is the result of the product of the scalar given and the vector.
        """
        return Vector2(x=self.x * scalar, y=self.y * scalar)

    def multiply_scalar_self(self, scalar):
        """
        Multiplies the vector by the scalar given.
        """
        self.x *= scalar
        self.y *= scalar
        return self

    def divide_scalar(self, scalar):
        """
        Returns a new Vector2 that is the result of the division of the vector by the scalar given.
        """
        if scalar != 0:
            x = float(self.x) / scalar
            y = float(self.y) / scalar
            return Vector2(x=x, y=y)
        else:
            return Vector2(x=0, y=0)

    def divide_scalar_self(self, scalar):
        """
        Divides the vector by the given scalar.
        """
        if scalar != 0:
            self.x = float(self.x) / scalar
            self.y = float(self.y) / scalar
        else:
            self.x = 0
            self.y = 0

        return self

    def normalize(self):
        """
        Normalizes the vector
        """
        return self.divide_scalar_self(self.length())

    def equal(self, v2):
        """
        Returns true if both the vector and the vector2 given are equal.
        """
        return self.x == v2.x and self.y == v2.y

    def cross(self, v2):
        """
        Returns the cross product of the vector with the given vector.
        """
        return self.x * v2.y - self.y * v2.x

    def clamp(self, maximum=1000000, minimum=-1000000):

        self.x = max(minimum, self.x)
        self.x = min(maximum, self.x)
        self.y = max(minimum, self.y)
        self.y = min(maximum, self.y)

        return self

    def clean(self, threshhold=.01):
        self.x = 0 if abs(self.x) < threshhold else self.x
        self.y = 0 if abs(self.y) < threshhold else self.y

    def __repr__(self):
        return "(%f, %f)" % (self.x, self.y)

def vector2_from_vector3(v3):

    return Vector2(x=v3.x, y=v3.y)

def test():
    """
    Unit tests for the vector2 class.
    """
    v_a = Vector2(x=50, y=0)
    v_b = Vector2(x=0, y=50)

    assert v_a.dot_product(v_b) == 0, "vector2.dot_product failed."
    assert v_a.distance_between(v_b) == v_b.distance_between(v_a), "vector2.distance_between failed."
    assert v_a.angle_between(v_b) == 90, "vector2.angle_between failed."
    assert v_a.normalize().length() == 1, "vector2.normalize failed."
    assert v_a.multiply_scalar(50).x == 50, "vector2.mulitply_scalar failed"

    v_a = Vector2(x=50, y=0)
    v_c = v_a.add(v_b)
    assert v_c.x == 50 and v_c.y == 50, "vector2.add failed."
    
    v_d = v_a.subtract(v_b)
    assert v_d.x == 50 and v_d.y == -50, "vector2.substract failed."

    v_e = v_b.add(v_a)
    assert v_c.equal(v_e) == True, "vector2.equal failed"

    print "passed all tests"
