"""
Scene.py: A class representation of the current contents of the screen.
"""

import math
from random import random, uniform, seed

import pyglet
from pyglet.gl import glEnable, glVertexPointer, glDrawArrays, glColorPointer, glEnableClientState, glDisableClientState, GLfloat
from pyglet.gl import GL_FLOAT, GL_BLEND, GL_POINTS, GL_VERTEX_ARRAY, GL_COLOR_ARRAY, GL_VERTEX_PROGRAM_POINT_SIZE, GL_POINT_SIZE_MAX_ARB

from Entity.Square import Square
from Util.Vector2 import Vector2

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

        # generating background needs to generalized
        self.background = []
        seed_val = 133700
        max_depth = .2

        for i in xrange(0, 500):
            # # determine i-th star's position
            basePosition = (random() * self.background_width, random() * self.background_height);
            depth = uniform(.001, max_depth)
            color = [random(), random(), random(), depth/max_depth]

            self.background.append((basePosition, depth, color))

    def draw_background(self):
        varray = []
        carray = []
        x = self.top_left['x']
        y = self.top_left['y']
        
        for _ in self.background:
            basePosition = _[0]
            depth = _[1]
            color = _[2]

            #parallax scrolling and wrapping
            realPosition = (basePosition[0] + x * depth, basePosition[1] + y * depth)
            wrappedPosition = ( realPosition[0] % self.background_width, realPosition[1] % self.background_height)
            varray += [wrappedPosition[0], wrappedPosition[1], 0]
            carray += color

        # # # needs to be commented and understood..
        # glEnable(GL_BLEND)
        # glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        # point_size = GLfloat(10.0)
        # glGetFloatv(GL_POINT_SIZE_MAX_ARB, point_size)
        # glPointSize(point_size)
        # glPointParameterfvARB(GL_POINT_DISTANCE_ATTENUATION_ARB, (GLfloat * 3)(0, 0, 5))
        # glPointParameterfARB(GL_POINT_SIZE_MIN_ARB, 5)
                
        varray = (GLfloat * len(varray))(*varray)
        carray = (GLfloat * len(carray))(*carray)

        glVertexPointer(3, GL_FLOAT, 0, varray)
        glColorPointer(4, GL_FLOAT, 0, carray)

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        
        glDrawArrays(GL_POINTS, 0, len(varray)//3)
        glDisableClientState(GL_VERTEX_ARRAY);
        glDisableClientState(GL_COLOR_ARRAY);

    def render(self):
        # draw background
        self.draw_background()

        # get all the entities and draw them
        entities = sorted(self.entities, key = lambda e: e.z_index)
        for e in entities:
            e.draw(self.top_left['x'], self.top_left['y'], self.height)

    def translate_x(self, x):
        if self.top_left['x'] + x < 0 or self.top_right['x'] + x > self.background_width:
            x = 0

        self.top_left['x'] += x
        self.top_right['x'] += x
        self.bottom_left['x'] += x
        self.bottom_right['x'] += x

    def translate_y(self, y):
        if self.top_left['y'] + y < 0 or self.bottom_left['y'] + y > self.background_height:
            y = 0

        self.top_left['y'] += y
        self.top_right['y'] += y
        self.bottom_left['y'] += y
        self.bottom_right['y'] += y

    def center(self, x, y):
        self.position.x = x - self.width/2
        self.position.y = y - self.height/2
        self.top_left = dict(x=self.position.x, y=self.position.y)
        self.top_right = dict(x=self.position.x + self.width, y=self.position.y)
        self.bottom_left = dict(x=self.position.x, y=self.position.y + self.height)
        self.bottom_right = dict(x=self.position.x + self.width, y=self.position.y + self.height)