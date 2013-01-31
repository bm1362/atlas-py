from random import random
import math

import pyglet
from pyglet.window import key, mouse
from pyglet.gl import *

import scene, world
from phys import engine
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

        # sync clock
        pyglet.clock.schedule_interval(self.tick, 1.0/60.0)   
        pyglet.clock.set_fps_limit(60)

        # create world
        world_width = 1500
        world_height = 1500
        self.world = world.world(world_width, world_height)

        # set background
        # self.background = pyglet.graphics.OrderedGroup(0)
        # self.background_image = pyglet.image.load('assets/space.png')
        # self.background_image.x_anchor = world_width / 2
        # self.background_image.y_anchor = world_height / 2
        # self.background_image.blit_into(img1,0,0,0)

        # create scene- match dimensions of the app window
        self.scene = scene.scene(self.world, offset_x=0, offset_y=0,width=width, height=height)

        # create physics engine
        self.engine = engine.engine()

        # throw some objects in there for now
        for _ in xrange(0, 50):
            theta = random() * 2 * math.pi
            pos = dict(x=random() * world_width, y=random() * world_height)
            s = circle(position=pos, size=50)
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
        if key.Q in self.key_pressed:
            self.scene.rotate(.1)

    def on_draw(self):
        # clear window
        self.window.clear()
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        # draw background
        self.scene.draw_background()

        # background_x = self.scene.top_left['x'] / 1
        # background_y = self.scene.top_left['y'] / 1
        # image = self.background_image.get_region(background_x, background_y, 1000, 500)
        # image.blit(0,0,0)
        # #self.background_image.blit(background_x,background_y,0)

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

sim = simulation(1000, 500)
pyglet.app.run()
