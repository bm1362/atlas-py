from uuid import uuid4
import math

import pyglet 

class entity(object):
    def __init__(self, **kwargs):
        self.id = uuid4()

        self.color = kwargs.get('color', (255, 255, 255, 255))
        self.position = kwargs.get('position', dict(x=0, y=0))
        self.vertices = []

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

    # rotates the entity clockwise by theta, in radians
    def rotate(self, theta):
        new_verts = []
        for _ in self.vertices:
            new_verts.append(self.rotate_vector(_, theta))
            
        self.vertices = new_verts

    # push to a util package? requires theta as a radian
    def rotate_vector(self, v, theta):
        x = v['x']
        y = v['y']
        cosa = math.cos(theta)
        sina = math.sin(theta)

        result = dict(x = x * cosa - y * sina, y = x * sina + y * cosa)
        return result
