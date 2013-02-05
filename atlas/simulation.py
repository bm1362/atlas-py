from random import random, seed
import math

import pyglet
from pyglet.window import key, mouse
from pyglet.gl import *

import scene, world
from phys import engine
from entity.entity import entity
from entity.square import square
from entity.circle import circle
        
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
        world_width = 3000
        world_height = 3000
        self.world = world.world(world_width, world_height)

        # create scene- match dimensions of the app window
        self.scene = scene.scene(self.world, offset_x=0, offset_y=0,width=width, height=height)

        # create physics engine
        self.engine = engine.engine()

        self.sun = []
        self.moon = []
        self.earth = []

        # throw some objects in there for now
        moon_pos = dict(x=world_width/2, y=world_height/2)
        moon = circle(position=moon_pos, color=(100, 100, 100, 255), radius=400, num_vertices=50, z_index=100)
        self.world.add_entity(moon)
        self.moon.append(moon)

        moon_pos = dict(x=world_width/2, y=world_height/2)
        moon = circle(position=moon_pos, color=(200, 200, 200, 255), radius=380, num_vertices=50, z_index=101)
        self.world.add_entity(moon)
        self.moon.append(moon)

        sun_pos = dict(x=world_width/4, y=world_height/4)
        sun = circle(position=sun_pos, color=(255, 255, 0, 200), radius=100, num_vertices=50, z_index=3)
        self.world.add_entity(sun)
        self.sun.append(sun)

        sun_pos = dict(x=world_width/4, y=world_height/4)
        sun = circle(position=sun_pos, color=(255, 215, 0, 200), radius=110, num_vertices=50, z_index=2)
        self.world.add_entity(sun)
        self.sun.append(sun)

        sun_pos = dict(x=world_width/4, y=world_height/4)
        sun = circle(position=sun_pos, color=(255, 150, 0, 200), radius=120, num_vertices=50, z_index=1)
        self.world.add_entity(sun)
        self.sun.append(sun)

        earth_pos = dict(x=world_width/8, y=world_height/8)
        earth = circle(position=earth_pos, color=(255, 255, 255, 100), radius=42, num_vertices=50, z_index=100)
        self.world.add_entity(earth)
        self.earth.append(earth)

        earth_pos = dict(x=world_width/8, y=world_height/8)
        earth = circle(position=earth_pos, color=(27, 92, 174, 255), radius=38, num_vertices=50, z_index=101)
        self.world.add_entity(earth)
        self.earth.append(earth)

        earth_pos = dict(x=world_width/8 + 5, y=world_height/8 + 5)

        land = [dict(x=-10, y=30), dict(x=0,y=0), dict(x=15, y=7.5), dict(x=20, y=15), dict(x=22, y=10), dict(x=20,y=-15)]
        earth = entity(position=earth_pos, color=(27, 98, 22, 225), z_index=102, vertices=land)
        self.world.add_entity(earth)
        self.earth.append(earth)

    def tick(self, dt):
        # update physics 
        self.engine.update()

        # update scene
        self.scene.update()

        # crappy orbit stuff, just temporary. Cosnidering making a system class that handles sets of objects
        scale = 2 * (math.fabs(self.moon[0].position['y'] - self.sun[0].position['y']) / self.world.height ) + .5
        # rotate sun
        for _ in self.sun:
            _.orbit_around(self.moon[0].position, self.moon[0].radius + 150, (dt * 360) / 120)
            _.scale(scale)

        for _ in self.earth:
            if scale > .5:
                _.z_index = self.moon[0].z_index + 1
            else:
                _.z_index = self.moon[0].z_index - 1
            _.scale(scale)
            _.rotate(1)
            _.orbit_around(self.sun[0].position, self.sun[0].radius + 150, (dt * 360) / 10)

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

        # draw background
        self.scene.draw_background()

        # # redraw scene
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

sim = simulation(1500, 1000)
pyglet.app.run()
