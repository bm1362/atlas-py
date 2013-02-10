"""
simulation.py: A class representation of the current simulation. When executed also serves as the driver for the simulation.
"""

from random import random, seed
import math

import pyglet
from pyglet.window import key, mouse
from pyglet.gl import *

import scene, world
from phys.rigid_body import rigid_body
from phys.force import force
from entity.entity import entity
from entity.square import square
from entity.circle import circle
from character import character
from util.vector2 import vector2
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
        self.clock = 0

        # sync clock
        pyglet.clock.schedule_interval(self.tick, 1.0/60.0)   
        pyglet.clock.set_fps_limit(60)

        # create world
        world_width = 2500
        world_height = 2500
        self.world = world.world(world_width, world_height)

        # seed(random() * 100000)

        # create scene- match dimensions of the app window
        self.scene = scene.scene(self.world, width=width, height=height)

        for _ in xrange(0, 10):
            pos = vector2(x=random() * world_width, y=random() * world_height)
            size = random() * 50 + 25

            if _ % 2 == 0:
                ent = circle(radius=size, position = pos)
            else:
                ent = square(size=size, position=pos)

            bdy = rigid_body(entity=ent)
            v = vector2(x = random() * 100, y = random() * 100)
            o = vector2(x = random() * size, y = random() * size)
            bdy.add_impulse(force(vector=v, offset=o))

            self.world.add_entity(ent)
            self.world.add_body(bdy)

    def tick(self, dt):
        # update physics 
        self.world.update(dt)

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
        if key.Q in self.key_pressed:
            self.scene.rotate(.1)

        self.clock += 1

    def on_draw(self):
        # clear window
        self.window.clear()
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        # redraw scene
        self.scene.render()

        # draw fps clock
        self.fps_display.draw()

        # draw foreground/ui ? in here or scene

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.key_pressed.append(key.LEFT)
        elif symbol == key.RIGHT:
            self.key_pressed.append(key.RIGHT)
        elif symbol == key.UP:
            self.key_pressed.append(key.UP)
        elif symbol == key.DOWN:
            self.key_pressed.append(key.DOWN)
        elif symbol == key.Q:
            self.key_pressed.append(key.Q)
        elif symbol == key.E:
            self.key_pressed.append(key.E)

    def on_key_release(self, symbol, modifiers):
        self.key_pressed.remove(symbol)

if __name__ == '__main__':
    sim = simulation(1000, 1000)
    pyglet.app.run()
