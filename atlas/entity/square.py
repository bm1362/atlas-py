import pyglet

from entity import entity
class square(entity):
    def __init__(self, **kwargs):
        super(square, self).__init__(**kwargs)
        self.size = kwargs.get('size', 5)

    def draw(self):
        vertices = (self.position['x']-self.size, self.position['y']+self.size, 
                    self.position['x']+self.size, self.position['y']+self.size,
                    self.position['x']+self.size, self.position['y']-self.size, 
                    self.position['x']-self.size, self.position['y']-self.size)
        
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
            ('v2f', vertices),
            ('c4B', self.color * 4)
        )
