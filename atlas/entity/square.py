"""
square.py: A class representation of a square in our world. Subclass of entity.
"""

import math

import pyglet

from entity import entity
from util.vector2 import vector2

class square(entity):
    def __init__(self, **kwargs):
        super(square, self).__init__(**kwargs)
        self.size = kwargs.get('size', 5)
        self.vertices = [
            vector2(x = -self.size, y = self.size),
            vector2(x = self.size, y = self.size),
            vector2(x = self.size, y = -self.size),
            vector2(x = -self.size, y = -self.size)
        ]