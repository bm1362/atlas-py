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
from CollisionContact import CollisionContact

class World(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # list of bodies that are in the world
        self.bodies = []

        # list of contacts in the world to be resolved
        self.contacts = []
        self.old_contacts = []

    def add_body(self, body):
        self.bodies.append(body)

    def remove_body(self, body):
        self.bodies.remove(body)

    def add_contact(self, contact):
        self.contacts.append(contact)

    def remove_contact(self, contact):
        self.contacts.remove(contact)

    def update(self, dt):
        self.update_gravitational_forces()
        self.detect_collisions()
        self.handle_contacts()

        for b in self.bodies:
            if b.is_moving():
                b.update(dt)

    def draw(self):
        for c in self.old_contacts:
            c.draw()
            
    # naive imp. could use trees
    def detect_collisions(self):
        lbodies = len(self.bodies)
        if lbodies > 1:
            for i in xrange(0, lbodies):
                for j in xrange(i+1, lbodies):
                    a = self.bodies[i]
                    b = self.bodies[j]
                    self.detect_collision(a, b)

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

            contact = CollisionContact(body_a, body_b, min_interval_distance, translation_axis, min_translational_vector)
            self.add_contact(contact)

            return True
        else: 
            return False
    
    def handle_contacts(self):

        for c in self.contacts:
            c.solve()

        self.old_contacts += self.contacts
        self.contacts = []


    def update_gravitational_forces(self):
        body_pairs = list(itertools.combinations(self.bodies, 2))
        for i,j in body_pairs:
            self.apply_gravity(i, j)

    def apply_gravity(self, body_a, body_b):
        G = 6.37 * 10**-21
        dist = body_a.entity.position.distance_between(body_b.entity.position)
        grav_force = G * (body_a.mass * body_b.mass) / dist**2

        force_a = body_b.entity.position.subtract(body_a.entity.position).multiply_scalar(grav_force)
        force_b = body_a.entity.position.subtract(body_b.entity.position).multiply_scalar(grav_force)
        force_a.clean(.1)
        force_b.clean(.1)

        body_a.add_impulse(Force(vector=force_a))
        body_b.add_impulse(Force(vector=force_b))
