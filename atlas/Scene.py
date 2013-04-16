"""
Scene.py: A class representation of the current contents of the screen.
"""

import math
from random import random, uniform, seed

import pyglet
from pyglet.gl import glEnable, glVertexPointer, glDrawArrays, glColorPointer, glEnableClientState, glDisableClientState, GLfloat
from pyglet.gl import GL_FLOAT, GL_BLEND, GL_POINTS, GL_VERTEX_ARRAY, GL_COLOR_ARRAY, GL_VERTEX_PROGRAM_POINT_SIZE, GL_POINT_SIZE_MAX_ARB, GL_TRIANGLES

from Entity.Square import Square
from Util.Vector2 import Vector2
from Util.Matrix3 import Matrix3
class Scene(object):
    def __init__(self, **kwargs):
        self.position = kwargs.get('position', Vector2(x=0, y=0))
        self.width = kwargs.get('width', 300)
        self.height = kwargs.get('height', 300)

        self.top_left = dict(x=self.position.x, y=self.position.y)
        self.top_right = dict(x=self.position.x + self.width, y=self.position.y)
        self.bottom_left = dict(x=self.position.x, y=self.position.y + self.height)
        self.bottom_right = dict(x=self.position.x + self.width, y=self.position.y + self.height)

        # list of entities
        self.entities = []

        self.background_width = kwargs.get('background_width', self.width)
        self.background_height = kwargs.get('background_height', self.height)

        self.scale_factor = 1
        self.dirty = False

    def draw_background(self):
        pass

    def render(self):
        # draw background
        self.draw_background()

        # get all the entities and draw them
        entities = sorted(self.entities, key = lambda e: e.z_index)
        for e in entities:
            e.scale(self.scale_factor)
            e.draw(self.top_left['x'], self.top_left['y'], self.height, self.dirty)

        self.dirty = False

    def translate_x(self, x):
        # if self.top_left['x'] * self.scale_factor + x < 0 or self.top_right['x'] * self.scale_factor + x > self.background_width:
        #     x = 0
        x = 1/self.scale_factor * x
        self.top_left['x'] += x
        self.top_right['x'] += x
        self.bottom_left['x'] += x
        self.bottom_right['x'] += x

        self.position.x += x
        self.dirty = True

    def translate_y(self, y):
        # if self.top_left['y'] * self.scale_factor + y < 0 or self.bottom_left['y'] * self.scale_factor + y > self.background_height:
        #     y = 0
        y = 1/self.scale_factor * y
        self.top_left['y'] += y
        self.top_right['y'] += y
        self.bottom_left['y'] += y
        self.bottom_right['y'] += y

        self.position.y += y
        self.dirty = True

    def center(self, x, y):
        self.position.x = x - self.width/2
        self.position.y = y - self.height/2
        self.top_left = dict(x=self.position.x, y=self.position.y)
        self.top_right = dict(x=self.position.x + self.width, y=self.position.y)
        self.bottom_left = dict(x=self.position.x, y=self.position.y + self.height)
        self.bottom_right = dict(x=self.position.x + self.width, y=self.position.y + self.height)
        self.dirty = True

    def scale(self, factor):
        self.scale_factor = factor
        self.dirty = True