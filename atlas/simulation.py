from random import random

import pyglet
from pyglet.window import key, mouse

import entity, scene, world 

class square(object):
    def __init__(self, size, initial, xVel, yVel):
        self.size = size
        self.pos = initial
        self.xVel = xVel
        self.yVel = yVel

    def update(self):
        self.pos = (self.pos[0]+self.xVel, self.pos[1]+self.yVel)

    def draw(self):
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
                ('v2f',(self.pos[0]-self.size, self.pos[1]+self.size, 
                    self.pos[0]+self.size, self.pos[1]+self.size,
                    self.pos[0]+self.size, self.pos[1]-self.size, 
                    self.pos[0]-self.size, self.pos[1]-self.size)))
        self.update()
        
window = pyglet.window.Window()
fps_display = pyglet.clock.ClockDisplay()

@window.event
def on_draw():
    window.clear()
    fps_display.draw()
    scene.render()

pyglet.app.run()