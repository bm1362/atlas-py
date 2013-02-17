"""
World.py: A class representation of our world, its contained bodies, and its physics
"""

import itertools

from Phys.Force import Force
from Util.Vector2 import Vector2
from Util.Geometry import is_in_polygon

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
            Returns a list of objects that are within the bounding box.
        """

        # returns any object with a vertex within the dimensions given
        result = []
        for _ in self.entities:
            for v in _.get_abs_vertices():
                vertices = ((top_left['x'], top_left['y']),(top_right['x'], top_right['y']),(bottom_left['x'], bottom_left['y']),(bottom_right['x'], bottom_right['y']))
                if is_in_polygon(vertices, (v.x, v.y)):
                    result.append(_)
                    break

        for _ in self.bodies:
            if _.entity in result:
                result.append(_)

        return result

    # naive imp.
    def detect_collisions(self):
        body_pairs = list(itertools.combinations(self.bodies, 2))
        for i,j in body_pairs:
            if self.detect_collision(i, j):
                v = i.entity.position.subtract(j.entity.position)
                i.add_impulse(force(vector=v.multiply_scalar(100)))
                j.add_impulse(force(vector=v.multiply_scalar(-100)))

    # Not scaling well, need to use a better technique to determine which objects could collide
    def detect_collision(self, body1, body2):
        bb_1 = body1.get_bounding_box()
        bb_1 = [bb_1['min_x'], bb_1['min_y'], bb_1['max_x'], bb_1['max_y']]
        bb_2 = body2.get_bounding_box()
        bb_2 = ((bb_2['min_x'].x, bb_2['min_x'].y),
                (bb_2['min_y'].x, bb_2['min_y'].y), 
                (bb_2['max_x'].x, bb_2['max_x'].y),
                (bb_2['max_y'].x, bb_2['max_y'].y))

        for v in bb_1:
            if is_in_polygon(bb_2, (v.x, v.y)) == True:
                return True

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
