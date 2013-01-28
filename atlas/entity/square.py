import pyglet
import math

from entity import entity
class square(entity):
    def __init__(self, **kwargs):
        super(square, self).__init__(**kwargs)
        self.size = kwargs.get('size', 5)
        self.vertices = [
            dict(x = -self.size, y = self.size),
            dict(x = self.size, y = self.size),
            dict(x = self.size, y = -self.size),
            dict(x = -self.size, y = -self.size)
        ]