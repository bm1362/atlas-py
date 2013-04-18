"""
Force.py: A class representation of a square in our world. Subclass of entity.
"""

from Util.Vector2 import Vector2
class Force(object):

    def __init__(self, **kwargs):
        
        # represents the offset from the center of mass
        self.offset = kwargs.get("offset", Vector2(x=0 , y=0))

        # represents the actual force vector
        self.vector = kwargs.get("vector", Vector2(x=0, y=0))

    def __unicode__(self):
        return "magnitude = %s" % (self.vector.length())
