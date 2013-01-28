import pyglet
import math

from entity import entity
class square(entity):
    def __init__(self, **kwargs):
        super(square, self).__init__(**kwargs)
        self.size = kwargs.get('size', 5)

    def draw(self, offset_x, offset_y, screen_height):
        x = self.position['x'] - offset_x

        # holy shit origin is bottom left
        y = screen_height - self.position['y'] + offset_y

        vertices = (x-self.size, y+self.size, 
                    x+self.size, y+self.size,
                    x+self.size, y-self.size, 
                    x-self.size, y-self.size)
        
        # print vertices
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
            ('v2f', vertices),
            ('c4B', self.color * 4)
        )
