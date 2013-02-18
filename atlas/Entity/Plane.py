"""
Plane.py: A class representation of a plane in our world. Subclass of entity.
"""

import math

from Entity import Entity
from Util.Vector2 import Vector2

class Plane(Entity):
    def __init__(self, **kwargs):
        super(Plane, self).__init__(**kwargs)
        self.width = kwargs.get('width', 1000)
        self.height = kwargs.get('height', 10)
        self.vertices = [Vector2(x=-self.width/2, y=-self.height/2),
                         Vector2(x=self.width/2, y=-self.height/2),
                         Vector2(x=self.width/2, y=self.height/2),
                         Vector2(x=-self.width/2, y=self.height/2)]
        self.update()