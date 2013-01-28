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
        self.window = pyglet.window.Window()
        self.window.on_draw = self.on_draw
        self.window.on_key_press = self.on_key_press
        self.window.on_key_release = self.on_key_release
        self.window.width = width
        self.window.height = height
        self.key_pressed = []

        # create fps display 
        self.fps_display = pyglet.clock.ClockDisplay()

        # sync clock
        pyglet.clock.schedule_interval(self.tick, 1.0/30.0)   
        pyglet.clock.set_fps_limit(30)

        # create world
        world_width = 5000
        world_height = 5000
        self.world = world.world(world_width, world_height)

        # create scene- match dimensions of the app window
        self.scene = scene.scene(self.world, offset_x=0, offset_y=0,width=width, height=height)
        
        # add event listeners

        # create physics engine
        self.engine = engine.engine()

        for _ in xrange(0, 100):
            theta = random() * 2 * math.pi
            pos = dict(x=random() * world_width, y=random() * world_height)
            s = square.square(position=pos, size=50)
            s.rotate(theta)
            self.world.add_entity(s)

    def tick(self, dt):
        # update physics 
        self.engine.update()

        # update scene
        self.scene.update()

        # move scene
        if key.LEFT in self.key_pressed:
            self.scene.translateX(-10)
        if key.RIGHT in self.key_pressed:
            self.scene.translateX(10)
        if key.UP in self.key_pressed:
            self.scene.translateY(-10)
        if key.DOWN in self.key_pressed:
            self.scene.translateY(10)

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
            self.key_pressed.append(key.LEFT)
        elif symbol == key.RIGHT:
            self.key_pressed.append(key.RIGHT)
        elif symbol == key.UP:
            self.key_pressed.append(key.UP)
        elif symbol == key.DOWN:
            self.key_pressed.append(key.DOWN)

    def on_key_release(self, symbol, modifiers):
        self.key_pressed.remove(symbol)

sim = simulation(1000, 500)
pyglet.app.run()