"""
force.py: A class representation of a square in our world. Subclass of entity.
"""

from util.vector2 import vector2
class force(object):

	def __init__(self, **kwargs):
		
		# represents the offset from the center of mass
		self.offset = kwargs.get("offset", vector2(x = 0, y = 0))

		# represents the actual force vector
		self.vector = kwargs.get("vector", vector2(x = 0, y = 0))
