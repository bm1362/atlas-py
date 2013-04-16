"""
Square.py: A class representation of a square in our world. Subclass of entity.
"""

import math

from Entity import Entity
from Util.Vector2 import Vector2

class Square(Entity):
    def __init__(self, **kwargs):
        super(Square, self).__init__(**kwargs)
        self.size = kwargs.get('size', 5)
        self.radius = self.size
        self.vertices = [
            Vector2(x = -self.size/2, y = self.size/2),
            Vector2(x = self.size/2, y = self.size/2),
            Vector2(x = self.size/2, y = -self.size/2),
            Vector2(x = -self.size/2, y = -self.size/2)
        ]

        self.update()