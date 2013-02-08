import pyglet
import math

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