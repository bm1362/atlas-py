"""
world.py: A class representation of our world, its contained bodies, and its physics
"""

import itertools

from phys.force import force
from util.vector2 import vector2
from util.geometry import is_in_polygon

class world(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # list of objects that are in the world
        self.entities = []

        # list of bodies that are in the world
        self.bodies = []

    def get_objects_in(self, top_left, top_right, bottom_left, bottom_right):
        """
            Returns a list of objects that are within the bounding box.
        """

        return self.entities + self.bodies
        # returns any object with a vertice within the dimensions given
        result = []
        for _ in self.entities:
            for v in _.get_abs_vertices():
                vertices = ((top_left['x'], top_left['y']),(top_right['x'], top_right['y']),(bottom_left['x'], bottom_left['y']),(bottom_right['x'], bottom_right['y']))
                if is_in_polygon(vertices, (v.x, v.y)):
                    result.append(_)
                    break

        return result

    def detect_collisions(self):
        body_pairs = list(itertools.combinations(self.bodies, 2))
        for i,j in body_pairs:
            if self.detect_collision(i, j):
                print ("collision", i.forces, i.linear_velocity)
                i.add_force(force(vector=vector2(x=-10000, y=0)))

    def detect_collision(self, body1, body2):
            bb_1 = body1.get_bounding_box()
            bb_2 = body2.get_bounding_box()

            left1 = bb_1['min_x'].x
            left2 = bb_2['min_x'].x
            right1 = bb_1['max_x'].x
            right2 = bb_2['max_x'].x
            bottom1 = bb_1['max_y'].y
            bottom2 = bb_2['max_y'].y
            top1 = bb_1['min_y'].y
            top2 = bb_2['min_y'].y

            if bottom1 < top2: return False;
            if top1 > bottom2: return False;

            if right1 < left2: return False;
            if left1 > right2: return False;

            return True

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
