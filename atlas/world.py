"""
world.py: A class representation of our world, its contained bodies, and its physics
"""

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

    def update(self, dt):
        for _ in self.bodies:
            _.update(dt)
        
    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        self.entities.remove(entity)

    def add_body(self, body):
        self.bodies.append(body)

    def remove_body(self, body):
        self.bodies.remove(body)
