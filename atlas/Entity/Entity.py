"""
Entity.py: A class representation of an entity in our world. Serves as the superclass for all interactable items.
"""

import math
from math import floor
from uuid import uuid4
from random import random

import pyglet 
from pyglet.gl import glColor4ub, glEnable, glVertexPointer, glDrawArrays, GLfloat, GL_BLEND, GL_POLYGON, GL_VERTEX_ARRAY, glEnableClientState, GL_FLOAT

from Util.Vector2 import Vector2
from Util.Matrix3 import Matrix3

class Entity(object):
    def __init__(self, **kwargs):
        self.id = uuid4()
        self.color = kwargs.get('color', (int(random() * 255), int(random() * 255), int(random() * 255), 255))
        self.position = kwargs.get('position', Vector2(x = 0, y = 0))
        self.orientation = kwargs.get('orientation', Matrix3())
        self.orientation.set(1, 0, 0, 
                             0, 1, 0, 
                             0, 0, 1)

        self.z_index = kwargs.get('z_index', 0)
        self.vertices = kwargs.get('vertices', [])
        self.abs_vertices = self.get_abs_vertices()
        self.orbital_angle = kwargs.get('orbital_angle', 0)
        self.scale_factor = 1
        self.scale_matrix = Matrix3()
        self.scale_matrix.set(1, 0, 0, 
                              0, 1, 0, 
                              0, 0, 1)

        self.cached_vertices = None
        self.dirty = True

    def update(self):
        self.update_abs_vertices()
        self.dirty = True
        # self.update_relative_vertices()

    def update_abs_vertices(self):
        self.abs_vertices = self.get_abs_vertices()

    def get_abs_vertices(self):
        vertices = []
        for _ in self.vertices:
            rot_v = self.orientation.multiply_vector2(_)
            v = self.position.add(rot_v)
            vertices.append(v)

        return vertices

    def get_screen_relative_vertices(self, offset_x, offset_y, screen_height):
        x = self.position.x - offset_x
        y = screen_height - self.position.y + offset_y

        vertices = ()
        for _ in self.vertices:
            rot_v = self.orientation.multiply_vector2(_)
            v = Vector2(x = x-rot_v.x, y=y + rot_v.y)
            scale = self.scale_matrix.multiply_vector2(v)
            vertices += (scale.x, scale.y,)

        self.dirty = False
        self.cached_vertices = vertices

        return vertices

    def get_screen_relative_vertices_vectors(self, offset_x, offset_y, screen_height):
        vertices = self.get_screen_relative_vertices(offset_x, offset_y, screen_height)

        vectors = [Vector2(x=vertices[i], y=vertices[i+1]) for i in xrange(0, len(vertices), 2)]

        return vectors

    def draw(self, offset_x, offset_y, screen_height, dirty=False):
        if dirty or self.dirty:
            vertices = self.get_screen_relative_vertices(offset_x, offset_y, screen_height)
        else:
            vertices = self.cached_vertices
        
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
        self.update()
            
    def orbit_around(self, origin, distance, angle):
        self.orbital_angle += angle
        x = origin['x'] + math.cos(self.orbital_angle * math.pi/180) * distance;
        y = origin['y'] + math.sin(self.orbital_angle * math.pi/180) * distance;
        self.position.x = x
        self.position.y = y
        self.update()

    def translate_vector(self, vector):
        self.position = self.position.add(vector)
        self.update()

    def translate(self, x, y):
        self.translate_vector(Vector2(x = x, y = y))
        self.update()

    def scale(self, factor):
        self.scale_matrix.set(factor, 0, 0, 
                             0, factor, 0, 
                             0, 0, 1)
        self.scale_factor = factor
        self.update()

    def set_position(self, position_vector):
        self.position = position_vector
        self.update()