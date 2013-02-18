"""
World.py: A class representation of our world, its contained bodies, and its physics
"""
from random import random
import itertools

from Phys.Force import Force
from Util.Vector2 import Vector2
from Util.Geometry import is_in_polygon
from Entity.Circle import Circle
from Entity.Square import Square
from Entity.Plane import Plane

class World(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # list of objects that are in the world
        self.entities = []

        # list of bodies that are in the world
        self.bodies = []

    def get_objects_in(self, top_left, top_right, bottom_left, bottom_right):
        """
            Returns a list of objects that should be drawn.
        """
        return self.entities + self.bodies

    # naive imp.
    def detect_collisions(self):
        body_pairs = list(itertools.combinations(self.bodies, 2))
        for i,j in body_pairs:
            if self.detect_collision(i, j):
                dist = i.entity.position.distance_between(j.entity.position)
                i_radius = i.get_bounding_radius()
                j_radius = j.get_bounding_radius()

                # move back until not intersecting
                d_v = i.entity.position.subtract(j.entity.position).normalize().multiply_scalar((i_radius + j_radius) - dist)
                i.entity.position.add_self(d_v)

                # calculate momentum
                # i_momentum = i.linear_velocity.multiply_scalar(i.mass)
                # j_momentum = j.linear_velocity.multiply_scalar(j.mass)

                total_mass = i.mass + j.mass
                v1i = ((i.mass - j.mass) / total_mass)
                v1i = i.linear_velocity.multiply_scalar(v1i)

                v2i = (2 * j.mass) / total_mass
                v2i = j.linear_velocity.multiply_scalar(v2i)

                vi = v1i.add(v2i)

                v1j = ((j.mass - i.mass) / total_mass)
                v1j = j.linear_velocity.multiply_scalar(v1j)

                v2j = (2 * i.mass) / total_mass
                v2j = i.linear_velocity.multiply_scalar(v2j)

                vj = v1j.add(v2j)

                # final momentum
                # i_momentum_f = vi.multiply_scalar(i.mass)
                # j_momentum_f = vj.multiply_scalar(j.mass)

                # # delta momentum
                # d_i_momentum = i_momentum_f.subtract(i_momentum)
                # d_j_momentum = j_momentum_f.subtract(j_momentum)

                # dvi = vi.add(i.linear_velocity)
                # dvj = vj.add(j.linear_velocity)
                
                new_color = tuple((int(random() * 255), int(random() * 255), int(random() * 255), 255))
                i.entity.color = new_color
                j.entity.color = new_color

                # apply forces
                i_offset = i.entity.position.subtract(j.entity.position).normalize().multiply_scalar(i_radius)
                j_offset = j.entity.position.subtract(i.entity.position).normalize().multiply_scalar(j_radius)

                ### not working 100%, shouldn't need to set linear_velocity
                i.add_impulse(Force(vector=vi.multiply_scalar(i.mass), offset=i_offset))
                j.add_impulse(Force(vector=vj.multiply_scalar(j.mass), offset=j_offset))

                i.linear_velocity = vi
                j.linear_velocity = vj

    def detect_collision(self, body1, body2):
        if isinstance(body1, Plane) or isinstance(body2, Plane):
            return True
        else:
            body1_radius = body1.get_bounding_radius()
            body2_radius = body2.get_bounding_radius()
            dist = body2.entity.position.distance_between(body1.entity.position)

            if dist > (body1_radius + body2_radius):
                return False
            else:
                return True

        # bb_1 = body1.get_bounding_box()
        # bb_1 = [bb_1['min_x'], bb_1['min_y'], bb_1['max_x'], bb_1['max_y']]
        # bb_2 = body2.get_bounding_box()
        # bb_2 = ((bb_2['min_x'].x, bb_2['min_x'].y),
        #         (bb_2['min_y'].x, bb_2['min_y'].y), 
        #         (bb_2['max_x'].x, bb_2['max_x'].y),
        #         (bb_2['max_y'].x, bb_2['max_y'].y))

        # for v in bb_1:
        #     if is_in_polygon(bb_2, (v.x, v.y)) == True:
        #         return True

        return False

    def update(self, dt):
        for _ in self.bodies:
            _.update(dt)

        self.detect_collisions()
        
    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        self.entities.remove(entity)

    def add_body(self, body):
        self.bodies.append(body)

    def remove_body(self, body):
        self.bodies.remove(body)
