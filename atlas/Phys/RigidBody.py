"""
RigidBody.py: A class representation of an object that obeys physics rules in our world.
"""
import math

import pyglet
from pyglet.gl import glPolygonMode, glDrawArrays, glEnable, GLfloat, GL_FLOAT, GL_FRONT_AND_BACK, GL_POLYGON, GL_FILL, glColor4ub
from pyglet.gl import GL_LINE, GL_BLEND, glEnableClientState, GL_VERTEX_ARRAY, glVertexPointer

from Util.Matrix3 import Matrix3
from Util.Vector2 import Vector2
from Util.Vector3 import Vector3
from Force import Force
from Entity.Square import Square
from Entity.Circle import Circle

class RigidBody(object):
    def __init__(self, **kwargs):
        self.entity = kwargs.get('entity', None)

        self.position = kwargs.get('position', Vector2())
        self.vertices = kwargs.get('vertices', self.entity.vertices)
        self.bounding_box = self.get_object_oriented_bb() # stored as a dict of Vector2
        self.movable = kwargs.get('movable', True)
        # private force and impulses- used to calculate acceleration.
        self._forces = kwargs.get('forces', [])
        self._impulses = kwargs.get('impulses', [])

        self.size = self.entity.size
        self.mass = kwargs.get('mass', 1)
        self.inv_mass = 1.0/self.mass
        self.linear_velocity = kwargs.get('linear_velocity', Vector2(x=0, y=0))
        self.angular_velocity = kwargs.get("angular_velocity", Vector3(x=0,y=0,z=0))
        self.angular_momentum = kwargs.get("angular_momentum", Vector3(x=0,y=0,z=0))
        self.orientation = kwargs.get('orientation', Matrix3())
        self.orientation = self.entity.orientation.clone()

        self.inertia_tensor = kwargs.get('inertia_tensor', 1.0/12.0 * self.mass * (1250))
        self.inv_inertia_tensor = 1/self.inertia_tensor
        # self.inertia_tensor = kwargs.get('inertia_tensor', Matrix3())
        # tensor = 1/12 * self.mass * (1250)
        # self.inertia_tensor.set(tensor,     0,  0,
        #                             0, tensor,  0,
        #                             0,      0, tensor)

        assert self.mass > 0, "Invalid mass."
        assert self.entity is not None, "Invalid entity."

    def zero_forces(self):
        self._forces = []
        self._impulses = []
        self.linear_acceleration = Vector2(x=0, y=0)
        self.linear_velocity = Vector2(x=0, y=0)

        self.angular_velocity = Vector3()
        self.angular_momentum = Vector3()

    def add_force(self, force):
        self._forces.append(force)

    def remove_force(self, force):
        self._forces.remove(force)

    def add_impulse(self, force):
        self._impulses.append(force)

    def calculate_forces(self):
        forces = []
        forces += self._forces + self._impulses
        force = Vector2(x=0,y=0)
        torque = Vector3()

        for i in forces:
            force.add_self(i.vector)
            if not i.offset.equal(Vector2()):
                r = Vector3(x=i.offset.x, y=i.offset.y, z=1)
                f = Vector3(x=i.vector.x, y=i.vector.y, z=1)
                
                r_cross = r.cross(f, True)
                torque.add_self(r_cross)

        return force, torque

    def translate(self, new_pos):
        if self.movable == True:
            self.position.add_self(new_pos)
            # self.entity.position.add_self(new_pos)

    def update(self, dt):
        # get total force and divide by mass- acceleration
        force, torque = self.calculate_forces()
        force.divide_scalar_self(self.mass)

        # clear impulses
        self._impulses = []

        # update object's velocity: Semi implicit Euler
        self.linear_velocity.add_self(force.multiply_scalar(dt))

        # update object's position
        new_pos = self.entity.position.add(self.linear_velocity.multiply_scalar(dt))
        self.position = new_pos
        self.entity.set_position(self.position)
        # update angular momentum and velocity
        self.angular_momentum.add_self(torque)

        # not working at the moment
        # moment_inverse = self.orientation.multiply_matrix3(self.inertia_tensor.inverse()).multiply_matrix3(self.orientation.transpose())
        # self.angular_velocity = moment_inverse.multiply_vector3(self.angular_momentum)
        self.angular_velocity = (self.angular_momentum).multiply_scalar(self.inv_inertia_tensor)
        
        if not self.angular_velocity.equal(Vector3()):
            # rotate body
            skew = Matrix3()
            w1 = 0
            w2 = 0
            w3 = self.angular_velocity.z

            skew.set(0, -w3, w2,
                     w3, 0, -w1,
                     -w2, w1, 0)

            orientation_integration = skew.multiply_matrix3(self.orientation).multiply_scalar(dt)
            self.orientation = self.orientation.add(orientation_integration)
            self.orientation.normalize().clean()
            self.entity.orientation = self.orientation

        # clamp values to prevent it from growing too large
        self.linear_velocity.clamp(100000, -100000)
        self.angular_momentum.clamp(10000, -10000)
        self.angular_velocity.clamp(10000, -10000)

    def get_object_oriented_bb(self):
        left = min(self.vertices, key=lambda v: v.x)
        top = min(self.vertices, key=lambda v: v.y)
        right = max(self.vertices, key=lambda v: v.x)
        bot = max(self.vertices, key=lambda v: v.y)

        return dict(left=left, top=top, right=right, bottom=bot)

    def is_moving(self):
        return (not self.linear_velocity.equal(Vector2())) or (not self.angular_velocity.equal(Vector3()))

    def get_abs_vertices(self):
        vertices = []
        for _ in self.vertices:
            rot_v = self.orientation.multiply_vector2(_)
            v = self.position.add(rot_v)
            vertices.append(v)

        return vertices

    def generate_contact(self, body):
        pass


