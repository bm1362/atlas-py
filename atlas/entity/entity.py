import math
from math import floor
from uuid import uuid4
from random import random
import pyglet 
from pyglet.gl import *
from util.vector2 import rotate_vector

class entity(object):
    def __init__(self, **kwargs):
        self.id = uuid4()
        self.color = kwargs.get('color', (int(random() * 255), int(random() * 255), int(random() * 255), int(random() * 255)))
        self.position = kwargs.get('position', dict(x=0, y=0))
        self.z_index = kwargs.get('z_index', 0)
        self.vertices = kwargs.get('vertices', [])

    def get_abs_vertices(self):
        vertices = []
        for _ in self.vertices:
            vertices.append(dict(x = self.position['x'] - _['x'], y = self.position['y'] - _['y']))
        return vertices

    def get_screen_relative_vertices(self, offset_x, offset_y, screen_height):
        x = self.position['x'] - offset_x
        y = screen_height - self.position['y'] + offset_y

        vertices = ()
        for _ in self.vertices:
            vertices += (x - _['x'],)
            vertices += (y + _['y'],)

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
        new_verts = []
        for _ in self.vertices:
            new_verts.append(rotate_vector(_, angle))
            
        self.vertices = new_verts