"""
Circle.py: A class representation of a circle in our world. Subclass of entity.
"""

import math

from Entity import Entity
from Util.Vector2 import Vector2

class Circle(Entity):
    def __init__(self, **kwargs):
        super(Circle, self).__init__(**kwargs)
        self.radius = kwargs.get('radius', 50)
        self.num_vertices = kwargs.get('num_vertices', 20)
        for i in xrange(0, self.num_vertices):
            theta = 2.0 * math.pi * (float(i)/self.num_vertices);   # get the current angle 
            x = self.radius * math.cos(theta) 						# calculate the x component 
            y = self.radius * math.sin(theta) 					    # calculate the y component 
            self.vertices += [Vector2(x = x, y = y)]