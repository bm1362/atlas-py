import math
from uuid import uuid4

import pyglet 

from util.vector2 import rotate_vector

class entity(object):
    def __init__(self, **kwargs):
        self.id = uuid4()
        self.color = kwargs.get('color', (255, 255, 255, 255))
        self.position = kwargs.get('position', dict(x=0, y=0))
        self.z_index = kwargs.get('z_index', 0)
        self.vertices = kwargs.get('vertices', [])

    def get_abs_vertices(self):
        vertices = []
        for _ in self.vertices:
            vertices.append(dict(x = self.position['x'] - _['x'], y = self.position['y'] - _['y']))
        return vertices

    def draw(self, offset_x, offset_y, screen_height):
        x = self.position['x'] - offset_x
        # holy shit origin is bottom left
        y = screen_height - self.position['y'] + offset_y

        vertices = ()
        for _ in self.vertices:
            vertices += (x - _['x'],)
            vertices += (y + _['y'],)

        pyglet.graphics.draw(len(self.vertices), pyglet.gl.GL_POLYGON,
            ('v2f', vertices),
            ('c4B', self.color * 4)
        )

    # rotates the entity counter clockwise by theta, in degrees
    def rotate(self, theta):
        new_verts = []
        for _ in self.vertices:
            new_verts.append(rotate_vector(_, theta))
            
        self.vertices = new_verts

    # push to a util package? rotates a vector counter clockwise by theta, requires theta as a degree
