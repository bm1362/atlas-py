from random import random
import math

import pyglet
from pyglet.window import key, mouse

import scene, world
from phys import engine
from entity import entity, square
        
class simulation(object):
    def __init__(self, width, height):
        # create pyglet window
        # super(Simulation, self).__init__()
        self.tick_count = 0
        self.window = pyglet.window.Window()
        self.window.on_draw = self.on_draw
        self.window.on_key_press = self.on_key_press
        self.window.width = width
        self.window.height = height

        # create fps display 
        self.fps_display = pyglet.clock.ClockDisplay()

        # sync clock
        pyglet.clock.schedule_interval(self.tick, 1.0/75.0)   
        pyglet.clock.set_fps_limit(75)

        # create world
        self.world = world.world()

        # create scene
        self.scene = scene.scene(self.world)
        
        # add event listeners

        # create physics engine
        self.engine = engine.engine()
        
        # generate objects
        for _ in xrange(0, 10):
            pos = dict(x = random()*500, y = random()*500)
            size = random()*50
            s = square.square(position=pos, size=size)
            # self.scene.add_entity(s)
            self.world.add_entity(s)
        # add objects to world

    def tick(self, dt):
        # update physics 
        self.engine.update()

        # update scene
        self.scene.update()

    def on_draw(self):
        # clear window
        self.window.clear()

        # draw fps clock
        self.fps_display.draw()

        # draw background

        # redraw scene
        self.scene.render()

        # draw foreground/ui

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.scene.offset_x -= 10
        elif symbol == key.RIGHT:
            self.scene.offset_x += 10

sim = simulation(300, 500)
pyglet.app.run()