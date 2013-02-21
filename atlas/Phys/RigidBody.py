"""
RigidBody.py: A class representation of an object that obeys physics rules in our world.
"""
import math

import pyglet
from pyglet.gl import glPolygonMode, glDrawArrays, glEnable, GLfloat, GL_FLOAT, GL_FRONT_AND_BACK, GL_POLYGON, GL_FILL, glColor4ub
from pyglet.gl import GL_LINE, GL_BLEND, glEnableClientState, GL_VERTEX_ARRAY, glVertexPointer

from Util.Vector2 import Vector2
from Force import Force
from Entity.Square import Square
from Entity.Circle import Circle

class RigidBody(object):
    def __init__(self, **kwargs):
        self.entity = kwargs.get('entity', None)
        self.forces = kwargs.get('forces', [])
        self.impulses = kwargs.get('impulses', [])
        self.mass = kwargs.get('mass', 1)
        self.moment_of_inertia = kwargs.get("moment_of_inertia", 1000)

        self.acceleration = kwargs.get('acceleration', Vector2(x=0, y=0))
        self.angular_acceleration = kwargs.get('angular_acceleration', 0)
        self.linear_velocity = kwargs.get('linear_velocity', Vector2(x=0, y=0))
        self.linear_momentum = kwargs.get('linear_momentum', Vector2(x=0, y=0))

        self.angular_velocity = kwargs.get('angular_velocity', 0)
        self.angular_momentum = kwargs.get('angular_momentum', Vector2(x=0, y=0))

        self.temp_velocity = Vector2(x=0, y=0)
        
        self.resistance = 1

        assert self.mass > 0, "Invalid mass."
        assert self.entity is not None, "Invalid entity."

    def add_force(self, force):
        self.forces.append(force)

    def remove_force(self, force):
        self.forces.remove(force)

    def update_acceleration(self, dt):
        da = Vector2(x=0, y=0)
        origin = Vector2(x=0, y=0)
        forces = []
        forces += self.forces + self.impulses
        self.angular_acceleration = 0
        for _ in forces:
            if _.offset.equal(origin):
                da.add_self(_.vector)
            else:
                r = _.offset
                proj = _.vector.dot_product(r) / _.offset.dot_product(r)
                parallel_component = _.offset.multiply_scalar(proj)     # calculate parallel component
                angular_force = _.vector.subtract(parallel_component)   # get perpendicular component
                torque = r.cross(_.vector)                              # calculate torque

                # update the angular acceleration
                self.angular_acceleration += torque / self.moment_of_inertia

                # use parallel component to add a translational force
                trans_force = Force(vector=parallel_component)
                forces.append(trans_force)

        # divide the net force by the mass to get the acceleration
        da.divide_scalar_self(self.mass)
        # update acceleration
        self.acceleration = da
        # clear impulses
        self.impulses = []

    def draw_forces(self, x, y):
        pyglet.text.Label(str(self.acceleration.length() * self.mass) ,x=x, y=y).draw()
        for force in self.forces:
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                ('v2f', (x+force.offset.x, y+force.offset.y, x+force.offset.x+force.vector.x , y+force.offset.y+force.vector.y)),
                ('c4B', (255,)*4*2))


    def draw(self, offset_x, offset_y, screen_height):
        x = self.entity.position.x - offset_x
        y = screen_height - self.entity.position.y + offset_y

        # self.draw_forces(x, y)
        # self.draw_bounding_box(x, y, screen_height)

    def update(self, dt):   
        # update object's position- using eq: Xi+1 = Xi + Ti*Vi + 1/2*(Ti^2)*Ai
        vt = self.linear_velocity.multiply_scalar(dt)
        at = self.acceleration.multiply_scalar(dt * dt * .5)
        new_pos = self.entity.position.multiply_scalar(1)

        new_pos.add_self(vt)
        new_pos.add_self(at)
        self.entity.set_position(new_pos)

        # update object's acceleration
        self.update_acceleration(dt)

        # update object's velocity- using eq: Vi+1 = Vi + Ti * Ai
        self.linear_velocity.add_self(self.acceleration.multiply_scalar(dt))
        self.linear_velocity.add_self(self.temp_velocity)
        self.temp_velocity = Vector2(x=0, y=0)

        # update velocity based on resistance
        self.linear_velocity.multiply_scalar_self(self.resistance)

        # update the rotation
        self.entity.orientation += .5 * self.angular_velocity * dt

        # update the angular velocity
        self.angular_velocity += self.angular_acceleration * dt

    def add_impulse(self, force):
        self.impulses.append(force)

    def get_bounding_radius(self):
        if isinstance(self.entity, Circle) == True:
            return self.entity.radius

        if isinstance(self.entity, Square) == True:
            return math.sqrt(2 * (self.entity.size / 2)**2) * 1.5

        return 1

    def get_bounding_box(self):
        vertices = self.entity.abs_vertices

        max_x = vertices[0]
        max_y = vertices[1]
        min_x = vertices[2]
        min_y = vertices[3]
        
        for _ in vertices:
            if _.x >= max_x.x:
                max_x = _
                
            if _.x < min_x.x:
                min_x = _
                
            if _.y > max_y.y:
                max_y = _
                
            if _.y < min_y.y:
                min_y = _
                    
        return dict(min_x = min_x.multiply_scalar(1), max_x = max_x.multiply_scalar(1), min_y = min_y.multiply_scalar(1), max_y = max_y.multiply_scalar(1))

    def draw_bounding_box(self, x, y, screen_height):
        bb = self.get_bounding_box()
        bb = [bb['min_x'], bb['min_y'], bb['max_x'], bb['max_y']]
        vertices = ()
        for _ in bb:
            vertices += (_.x,)
            vertices += (screen_height - _.y,)

        # get opengl vertices of type GLfloat
        vertices_gl = (GLfloat * len(vertices))(*vertices)

        # set the color
        glColor4ub(0, 255, 0, 255);
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );

        # turn on blend for alpha channel
        glEnable(GL_BLEND)

        # tell open GL were passing a vertex array
        glEnableClientState(GL_VERTEX_ARRAY)

        # create a pointer to vertices_gl
        glVertexPointer(2, GL_FLOAT, 0, vertices_gl)
       
        # draw the array
        glDrawArrays(GL_POLYGON, 0, len(vertices) // 2)

        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL );