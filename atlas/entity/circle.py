import pyglet
import math

from pyglet.gl import *

from entity import entity
class circle(entity):
    def __init__(self, **kwargs):
        super(circle, self).__init__(**kwargs)
        self.radius = kwargs.get('radius', 50)
        num_verts = 20
        for i in xrange(0, num_verts):
            theta = 2.0 * math.pi * (float(i)/num_verts); #get the current angle 
            x = self.radius * math.cos(theta) #calculate the x component 
            y = self.radius * math.sin(theta) #calculate the y component 
            cx = x + self.position['x']
            cy = y + self.position['y']
            self.vertices.append(dict(x = cx, y = cy))