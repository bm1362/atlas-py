import pyglet

from entity import entity
class square(entity):
    def __init__(self, **kwargs):
        super(square, self).__init__(**kwargs)
        self.size = kwargs['size'] if 'size' in kwargs else 5

    def draw(self, offset_x, offset_y):
        vertices = (self.position['x']-self.size - offset_x, self.position['y']+self.size - offset_y, 
                    self.position['x']+self.size - offset_x, self.position['y']+self.size - offset_y,
                    self.position['x']+self.size - offset_x, self.position['y']-self.size - offset_y, 
                    self.position['x']-self.size - offset_x, self.position['y']-self.size - offset_y)
        
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
            ('v2f', vertices),
            ('c4B', self.color * 4)
        )