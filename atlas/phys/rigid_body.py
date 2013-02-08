"""
rigid_body.py: A class representation of an object that obeys physics rules in our world.
"""
import math

import pyglet

from entity.entity import entity
from util.vector2 import vector2
from force import force
import entity

class rigid_body(object):
    def __init__(self, **kwargs):
        self.entity = kwargs.get('entity', None)
        self.forces = kwargs.get('forces', [])
        self.impulses = kwargs.get('impulses', [])
        self.mass = kwargs.get('mass', 1)
        self.moment_of_inertia = kwargs.get("moment_of_inertia", 1000)

        self.acceleration = kwargs.get('acceleration', vector2(x=0, y=0))
        self.angular_acceleration = kwargs.get('angular_acceleration', 0)
        self.linear_velocity = kwargs.get('linear_velocity', vector2(x=0, y=0))
        self.linear_momentum = kwargs.get('linear_momentum', vector2(x=0, y=0))

        self.angular_velocity = kwargs.get('angular_velocity', 0)
        self.angular_momentum = kwargs.get('angular_momentum', vector2(x=0, y=0))
        
        self.resistance = .5

        assert self.mass > 0, "Invalid mass."
        assert self.entity is not None, "Invalid entity."

    def add_force(self, force):
        self.forces.append(force)

    def remove_force(self, force):
        self.forces.remove(force)

    # does not attempt rotational at the moment
    def update_acceleration(self, dt):
        da = vector2(x=0, y=0)
        origin = vector2(x=0, y=0)
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
                trans_force = force(vector=parallel_component)
                forces.append(trans_force)

        # divide the net force by the mass to get the acceleration
        da.divide_scalar_self(self.mass)
        # update acceleration
        self.acceleration.add_self(da)
        # clear impulses
        self.impulses = []

    def draw_forces(self):
        pass

    def draw(self, offset_x, offset_y, screen_height):
        x = self.entity.position.x - offset_x
        y = screen_height - self.entity.position.y + offset_y

        pyglet.text.Label(str(self.acceleration.length() * self.mass) ,x=x, y=y).draw()

    def update(self, dt):
        # update object's position- using eq: Xi+1 = Xi + Ti*Vi + 1/2*(Ti^2)*Ai
        vt = self.linear_velocity.multiply_scalar(dt)
        at = self.acceleration.multiply_scalar(dt * dt * .5)
        self.entity.position.add_self(vt)
        self.entity.position.add_self(at)

        # update object's acceleration
        self.update_acceleration(dt)

        # update object's velocity- using eq: Vi+1 = Vi + Ti * Ai
        self.linear_velocity.add_self(self.acceleration.multiply_scalar(dt))

        # update velocity based on resistance
        self.linear_velocity.multiply_scalar(self.resistance)

        # update the rotation
        self.entity.orientation += .5 * self.angular_velocity * dt

        # update the angular velocity
        self.angular_velocity += self.angular_acceleration * dt

    def add_impulse(self, force):
        self.impulses.append(force)

    def get_bounding_box(self):
        pass