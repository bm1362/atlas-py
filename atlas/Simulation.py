"""
Simulation.py: A class representation of the current simulation. When executed also serves as the driver for the simulation.
"""

from random import random, seed
from time import time
import math

import pyglet
from pyglet.window import key, mouse
from pyglet.gl import glClear, GL_COLOR_BUFFER_BIT, glLoadIdentity

from Scene import Scene

from Phys.World import World
from Phys.RigidBody import RigidBody
from Phys.Force import Force
from Entity.Entity import Entity
from Entity.Square import Square
from Entity.Circle import Circle
from Entity.Plane import Plane
from Util.Vector2 import Vector2
from Util.Geometry import is_in_polygon
from Sound.Music import Music

class Simulation(object):
    def __init__(self, width, height):
        # create pyglet window
        self.window = pyglet.window.Window(resizable=True)
        self.window.on_draw = self.on_draw
        self.window.on_key_press = self.on_key_press
        self.window.on_key_release = self.on_key_release
        self.window.on_mouse_press = self.on_mouse_press
        self.window.on_mouse_release = self.on_mouse_release
        self.window.on_mouse_drag = self.on_mouse_drag
        self.window.width = width
        self.window.height = height
        self.key_pressed = []
        self.clicked_object = None
        self.clicked_dx = 0
        self.clicked_dy = 0

        # create fps display 
        self.fps_display = pyglet.clock.ClockDisplay()
        self.clock = 0

        # sync clock
        pyglet.clock.schedule_interval(self.tick, 1.0/60.0)   
        pyglet.clock.set_fps_limit(60)

        # create world
        world_width = 1000
        world_height = 1000
        self.world = World(world_width, world_height)

        # create scene- match dimensions of the app window
        self.scene = Scene(width=width, height=height, background_width=world_width, background_height=world_height)

        #self.demo_1(world_width, world_height)
        #self.demo_2(world_width, world_height)
        #self.demo_3(world_width, world_height)

        # initialize background music
        self.music = Music()
        self.music.play_bg()

    def tick(self, dt):
        # update physics 
        self.world.update(dt)

        # move scene
        if key.LEFT in self.key_pressed:
            self.scene.translate_x(-10)
        if key.RIGHT in self.key_pressed:
            self.scene.translate_x(10)
        if key.UP in self.key_pressed:
            self.scene.translate_y(-10)
        if key.DOWN in self.key_pressed:
            self.scene.translate_y(10)
        if key.M in self.key_pressed:
            self.music.stop_bg()

        self.clock += 1

    def on_draw(self):
        # clear window
        self.window.clear()
        
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
        elif symbol == key.M:
            self.key_pressed.append(key.M)

    def on_key_release(self, symbol, modifiers):
        self.key_pressed.remove(symbol)

    def demo_1(self, world_width, world_height):
        mag = 100000
        offset = 100
        sq1 = Square(size=50, position=Vector2(x=offset, y=offset))
        self.scene.entities.append(sq1)
        body1 = RigidBody(entity=sq1, mass=100)
        body1.add_impulse(Force(vector=Vector2(x=mag, y=mag)))
        self.world.add_body(body1)

        sq2 = Circle(size=50, position=Vector2(x=world_width-offset, y=offset))
        self.scene.entities.append(sq2)
        body2 = RigidBody(entity=sq2, mass=100)
        body2.add_impulse(Force(vector=Vector2(x=-mag, y=mag)))
        self.world.add_body(body2)

        sq3 = Square(size=50, position=Vector2(x=offset, y=world_height/2-offset))
        self.scene.entities.append(sq3)
        body3 = RigidBody(entity=sq3, mass=100)
        body3.add_impulse(Force(vector=Vector2(x=mag, y=-0)))
        self.world.add_body(body3)

        sq4 = Circle(size=50, position=Vector2(x=world_width - offset, y=world_height/2-offset))
        self.scene.entities.append(sq4)
        body4 = RigidBody(entity=sq4, mass=100)
        body4.add_impulse(Force(vector=Vector2(x=-mag, y=0)))
        self.world.add_body(body4)

    def demo_2(self, world_width, world_height):
        for i in xrange(0, 5):
            size = 50
            pos = Vector2(x=(i * size * 1) + world_width/2 - (size * 3), y=world_height/2)

            ent = Square(size=size, position=pos, num_vertices=10)

            bdy = RigidBody(entity=ent, mass=100)
            v = Vector2(x=random() * 100, y=random() * 100)
            o = Vector2(x=random() * size, y=random() * size)
            bdy.add_impulse(Force(vector=v, offset=o))

            self.scene.entities.append(ent)
            self.world.add_body(bdy)

        for i in xrange(0, 5):
            size = 50
            pos = Vector2(x=(i * size * 1) + world_width/2 - (size * 3), y=world_height/2 + size)

            ent = Square(size=size, position=pos, num_vertices=10)

            bdy = RigidBody(entity=ent, mass=100)

            self.scene.entities.append(ent)
            self.world.add_body(bdy)

        for i in xrange(0, 5):
            size = 50
            pos = Vector2(x=(i * size * 1) + world_width/2 - (size * 3), y=world_height/2 + 2 * size)

            ent = Square(size=size, position=pos, num_vertices=10)

            bdy = RigidBody(entity=ent, mass=100)

            self.scene.entities.append(ent)
            self.world.add_body(bdy)

        sq4 = Circle(radius=25, position=Vector2(x=world_width/2 + 10, y=100))
        self.scene.entities.append(sq4)
        body4 = RigidBody(entity=sq4, mass=10)
        body4.add_impulse(Force(vector=Vector2(x=0, y=100000)))
        self.world.add_body(body4)

    def demo_3(self, world_width, world_height):
        for _ in xrange(0, 10):
            pos = Vector2(x=random() * world_width, y=random() * world_height)
            size = random() * 50 + 25

            ent = Circle(radius=size, position=pos, num_vertices=10)

            bdy = RigidBody(entity=ent, mass=100)
            v = Vector2(x=random() * 100, y=random() * 100)
            o = Vector2(x=random() * size, y=random() * size)
            bdy.add_impulse(Force(vector=v, offset=o))

            self.scene.entities.append(ent)
            self.world.add_body(bdy)

    def on_mouse_press(self, x, y, button, modifiers):
        #Clear the stored dx and dy
        self.clicked_dx = 0
        self.clicked_dy = 0

        #If there is an item under the pointer, remove it from bodies,
        #keep track of it by itself, and zero out all forces
        for body in self.world.bodies:
            if is_in_polygon(body.entity.get_screen_relative_vertices_vectors(
                self.scene.top_left['x'], self.scene.top_left['y'], 
                self.scene.height), Vector2(x=x, y=y)):
                self.world.remove_body(body)
                self.clicked_object = body
                self.clicked_object.zero_forces()
                return

        #If there was no object under the pointer, create a new object but 
        #keep it free from physics for now
        entity = Circle(size=50, position=Vector2(
            x=x + self.scene.top_left['y'], 
            y=self.scene.height - y + self.scene.top_left['y']))
        self.scene.entities.append(entity)
        self.clicked_object = RigidBody(entity=entity, mass=100)


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        #Store the dx and dy since mouse release does not track movements
        self.clicked_dx = dx
        self.clicked_dy = dy
        
        #If there is an item being clicked on, move it.
        if self.clicked_object is not None:
            self.clicked_object.entity.translate_vector(Vector2(x=dx, y=-dy))

    def on_mouse_release(self, x, y, button, modifiers):
        #If there is an object being clicked on, release it with the velocity
        #determined from self.dx and self.dy
        if self.clicked_object is not None:
            self.world.add_body(self.clicked_object)
            self.clicked_object.add_impulse(Force(vector=Vector2(
                x=self.clicked_dx*100000, y=-self.clicked_dy*100000)))

        #Clear the stored dx, dy, as well as the object being clicked on
        self.clicked_dx = 0
        self.clicked_dy = 0
        self.clicked_object = None

if __name__ == '__main__':
    sim = Simulation(1000, 500)
    pyglet.app.run()
