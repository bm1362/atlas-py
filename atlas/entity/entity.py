"""
entity.py: A class representation of an entity in our world. Serves as the superclass for all interactable items.
"""

import math
from math import floor
from uuid import uuid4
from random import random

import pyglet 
from pyglet.gl import *

from util.vector2 import vector2

class entity(object):
    def __init__(self, **kwargs):
        self.id = uuid4()
        self.color = kwargs.get('color', (int(random() * 255), int(random() * 255), int(random() * 255), 255))
        self.position = kwargs.get('position', vector2(x = 0, y = 0))
        self.orientation = kwargs.get('orientation', 0)
        self.z_index = kwargs.get('z_index', 0)
        self.vertices = kwargs.get('vertices', [])
        self.orbital_angle = kwargs.get('orbital_angle', 0)
        self.scale_factor = 1

    def get_abs_vertices(self):
        vertices = []
        for _ in self.vertices:
            rot_v = _.rotate(self.orientation)
            v = self.position.add(rot_v)
            vertices.append(v)

        return vertices

    def get_screen_relative_vertices(self, offset_x, offset_y, screen_height):
        x = self.position.x - offset_x
        y = screen_height - self.position.y + offset_y

        vertices = ()
        for _ in self.vertices:
            rot_v = _.rotate(self.orientation)
            vertices += (x - rot_v.x * self.scale_factor,)
            vertices += (y + rot_v.y * self.scale_factor,)

        return vertices

    def draw(self, offset_x, offset_y, screen_height):
        vertices = self.get_screen_relative_vertices(offset_x, offset_y, screen_height)

        # get opengl vertices of type GLfloat
        vertices_gl = (GLfloat * len(vertices))(*vertices)

        # set the color
        glColor4ub(*self.color);

        # turn on blend for alpha channel
        glEnable(GL_BLEND)

        # tell open GL were passing a vertex array
        glEnableClientState(GL_VERTEX_ARRAY)

        # create a pointer to vertices_gl
        glVertexPointer(2, GL_FLOAT, 0, vertices_gl)
       
        # draw the array
        glDrawArrays(GL_POLYGON, 0, len(vertices) // 2)

    # rotates the entity counter clockwise by the angle
    def rotate(self, angle):
        self.orientation += angle
            
    def orbit_around(self, origin, distance, angle):
        self.orbital_angle += angle
        x = origin['x'] + math.cos(self.orbital_angle * math.pi/180) * distance;
        y = origin['y'] + math.sin(self.orbital_angle * math.pi/180) * distance;
        self.position.x = x
        self.position.y = y

    def translate_vector(self, vector):
        self.position = self.position.add(vector)

    def translate(self, x, y):
        self.translate_vector(vector2(x = x, y = y))

    def scale(self, factor):
        self.scale_factor = factor