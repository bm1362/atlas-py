"""
Triangle.py: A class representation of a triangle in our world. Subclass of entity.
"""

import math

from Entity import Entity
from Util.Vector2 import Vector2

class Triangle(Entity):
    def __init__(self, **kwargs):
        super(Triangle, self).__init__(**kwargs)
        self.size = kwargs.get('size', 5)
        self.vertices = [
	    Vector2(x = self.size * 1.1, y = -self.size),
            Vector2(x = -self.size * 1.25, y = 0),
            Vector2(x = self.size * 1.1, y = self.size),
        ]

        self.update()
