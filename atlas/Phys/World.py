"""
World.py: A class representation of our world, its contained bodies, and its physics
"""

import math
from sys import maxint
from random import random
import itertools

from Phys.Force import Force
from Util.Vector2 import Vector2
from Util.Geometry import is_in_polygon, get_polygon_edges, project_polygon, get_interval_distance
from Entity.Circle import Circle
from Entity.Square import Square
from Entity.Plane import Plane

class World(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # list of bodies that are in the world
        self.bodies = []

    # naive imp. could use trees
    def detect_collisions(self):
        body_pairs = list(itertools.combinations(self.bodies, 2))
        for i,j in body_pairs:
            if self.detect_collision_projection(i, j):
               self.handle_collision_bounding_radius(i, j)

    def handle_collision_bounding_radius(self, body_a, body_b):
            dist = body_a.entity.position.distance_between(body_b.entity.position)
            a_radius = body_a.get_bounding_radius() + 5
            b_radius = body_b.get_bounding_radius() + 5

            restitution = .5

            ma = body_a.mass
            mb = body_b.mass

            va = body_a.linear_velocity
            vb = body_b.linear_velocity

            ma_va = va.multiply_scalar(ma)
            mb_vb = vb.multiply_scalar(mb)

            ma_va_ma_vb = ma_va.add(mb_vb)

            total_mass = ma + mb

            vaf = vb.subtract(va).multiply_scalar_self(restitution * mb).add_self(ma_va_ma_vb).divide_scalar_self(total_mass)
            vbf = va.subtract(vb).multiply_scalar_self(restitution * ma).add_self(ma_va_ma_vb).divide_scalar_self(total_mass)
            
            new_color = tuple((int(random() * 255), int(random() * 255), int(random() * 255), 255))
            body_a.entity.color = new_color
            body_b.entity.color = new_color

            # apply forces
            a_offset = body_a.entity.position.subtract(body_b.entity.position).normalize().multiply_scalar(a_radius)
            b_offset = body_b.entity.position.subtract(body_a.entity.position).normalize().multiply_scalar(b_radius)

            ### not working 100%, shouldn't need to set linear_velocity
            body_a.add_impulse(Force(vector=vaf.multiply_scalar(body_a.mass), offset=a_offset))
            body_b.add_impulse(Force(vector=vbf.multiply_scalar(body_b.mass), offset=b_offset))

            body_a.linear_velocity = (vaf)
            body_b.linear_velocity = (vbf)


    def detect_collision_bounding_radius(self, body1, body2):
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

    def detect_collision_projection(self, body_a, body_b):
        """
        Detects collisions between two bodies using the seperating axis theorem. Will move body_a out of the collision.

        See: http://www.codezealot.org/archives/55
        """
        a_edges = get_polygon_edges(body_a.entity.abs_vertices)
        b_edges = get_polygon_edges(body_b.entity.abs_vertices)

        edges = a_edges + b_edges
        translation_axis = None
        min_translational_vector = Vector2()
        min_interval_distance = maxint

        for e in edges:
            # get axis, perp to the edge
            axis = Vector2(x=e.y, y=-e.x).normalize()

            # get projections
            a_proj = project_polygon(body_a.entity.abs_vertices, axis)
            b_proj = project_polygon(body_b.entity.abs_vertices, axis)

            # get overlap, are they currently overlapping?
            overlap = get_interval_distance(a_proj, b_proj)

            # if overlap is negative, the polygons are intersecting
            if overlap > 0:
                return False

            # find smallest overlap and record it and the axis- our mtv is on the axis with magnitude equal to the overlap
            overlap = math.fabs(overlap)
            if overlap < min_interval_distance:
                min_interval_distance = overlap
                translation_axis = axis

        # calculate vector to back out of collision
        min_translational_vector = translation_axis.multiply_scalar(min_interval_distance)

        # determine if the mtv is in the direction of object b, if it is we need to reverse direction
        d_pos = body_a.entity.position.subtract(body_b.entity.position)
        
        # ensure the mtv is in the opposite direction of the collision
        if min_translational_vector.dot_product(d_pos) < 0:
            min_translational_vector.multiply_scalar_self(-1)

        # add mtv to body_a position- this will ensure that we never have overlapping bodies
        body_a.entity.position.add_self(min_translational_vector)
        #body_b.entity.position.add_self(min_translational_vector.multiply_scalar(-1))
        return True
            
    def update(self, dt):
        for _ in self.bodies:
            _.update(dt)

        self.update_gravitational_forces()
        self.detect_collisions()

    def add_body(self, body):
        self.bodies.append(body)

    def remove_body(self, body):
        self.bodies.remove(body)

    def update_gravitational_forces(self):
        body_pairs = list(itertools.combinations(self.bodies, 2))
        for i,j in body_pairs:
            self.apply_gravity(i, j)

    def apply_gravity(self, body_a, body_b):
        G = 6.37 * 10**-11
        dist = body_a.entity.position.distance_between(body_b.entity.position)

        grav_force = G * (body_a.mass * body_b.mass) / dist**2

        force_a = body_b.entity.position.subtract(body_a.entity.position).multiply_scalar(grav_force)
        force_b = body_a.entity.position.subtract(body_b.entity.position).multiply_scalar(grav_force)

        body_a.add_impulse(Force(vector=force_a))
        body_b.add_impulse(Force(vector=force_b))
