"""
World.py: A class representation of our world, its contained bodies, and its physics
"""

import math
from sys import maxint
from random import random
import itertools

from Phys.Force import Force
from Util.Vector2 import Vector2, vector2_from_vector3
from Util.Vector3 import Vector3, vector3_from_vector2
from Util.Geometry import is_in_polygon, get_polygon_edges, project_polygon, get_interval_distance
from Entity.Circle import Circle
from Entity.Square import Square
from Entity.Plane import Plane

class Contact(object):
    def __init__(self):
        pass

class World(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # list of bodies that are in the world
        self.bodies = []

    def add_body(self, body):
        self.bodies.append(body)

    def remove_body(self, body):
        self.bodies.remove(body)

    # naive imp. could use trees
    def detect_collisions(self):
        lbodies = len(self.bodies)
        if lbodies > 1:
            for i in xrange(0, lbodies):
                for j in xrange(i+1, lbodies):
                    a = self.bodies[i]
                    b = self.bodies[j]
                    if self.detect_collision(a, b):
                        a.generate_contact(b)

    def detect_collision(self, body_a, body_b):
        radius_sum = body_a.size + body_b.size
        collision_normal = body_b.position.subtract(body_a.position)
        collision_normal.normalize()

        distsq = collision_normal.length() ** 2
        if(distsq <= radius_sum ** 2):
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

            if body_a.movable and body_b.movable:
                body_b.translate(min_translational_vector.multiply_scalar(-1))
                body_a.translate(min_translational_vector)
            else:
                if body_a.movable and not body_b.movable:
                    body_a.translate(min_translational_vector.multiply_scalar(1))
                else:
                    body_b.translate(min_translational_vector.multiply_scalar(-1))

            # # handling linear and angular momentum           
            # collision_point = collision_normal.multiply_scalar(body_a.size)
            # collision_point = vector3_from_vector2(collision_point)
            # cn = vector3_from_vector2(collision_normal)

            # p1 = vector3_from_vector2(body_a.position)
            # p2 = vector3_from_vector2(body_b.position)
            # r1 = collision_point.subtract(p1)
            # r2 = collision_point.subtract(p2)

            # v1 = vector3_from_vector2(body_a.linear_velocity)
            # vel1 = v1.add(body_a.angular_velocity.cross(r1))

            # v2 = vector3_from_vector2(body_b.linear_velocity)
            # vel2 = v2.add(body_b.angular_velocity.cross(r2))
            # relative_velocity = vector2_from_vector3(vel1.subtract(vel2))
            # dot_normal = relative_velocity.dot_product(collision_normal)

            # if dot_normal < 0:
            #     return True

            # modified_velocity = dot_normal / (body_a.inv_mass + body_b.inv_mass)

            # j1 = -modified_velocity # need to add elasticity here
            # j2 = -modified_velocity

            # body_a.linear_velocity.add_self(collision_normal.multiply_scalar(j1 * body_a.inv_mass))
            # body_b.linear_velocity.subtract_self(collision_normal.multiply_scalar(j2 * body_b.inv_mass))

            return True
        else: 
            return False
            
    def update(self, dt):
        # these are performance drags
        self.update_gravitational_forces()
        self.detect_collisions()
        # self.handle_contacts()

        for _ in self.bodies:
            _.update(dt)

    def update_gravitational_forces(self):
        body_pairs = list(itertools.combinations(self.bodies, 2))
        for i,j in body_pairs:
            self.apply_gravity(i, j)

    def apply_gravity(self, body_a, body_b):
        G = 6.37 * 10**-21
        dist = body_a.entity.position.distance_between(body_b.entity.position)

        # if dist > 100000: return
        if dist < (body_a.size + body_b.size): 
            mass_ratio_a = body_a.mass / body_b.mass
            mass_ratio_b = body_b.mass / body_a.mass
            # if mass_ratio_a < .01:
            #     body_a.zero_forces()
            # if mass_ratio_b < .01:
            #     body_b.zero_forces()

            return

        grav_force = G * (body_a.mass * body_b.mass) / dist**2

        force_a = body_b.entity.position.subtract(body_a.entity.position).multiply_scalar(grav_force)
        force_b = body_a.entity.position.subtract(body_b.entity.position).multiply_scalar(grav_force)
        # force_a.clean(.1)
        # force_b.clean(.1)

        body_a.add_impulse(Force(vector=force_a))
        body_b.add_impulse(Force(vector=force_b))
