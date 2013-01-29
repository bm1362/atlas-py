import math

from util import geometry

class scene(object):
	def __init__(self, world, **kwargs):
		self.entities = []
		self.world = world

		assert(self.world is not None)

		self.offset_x = kwargs.get('offset_x', 0)
		self.offset_y = kwargs.get('offset_y', 0)
		self.width = kwargs.get('width', 300)
		self.height = kwargs.get('height', 300)

		self.top_left = dict(x = self.offset_x, y = self.offset_y)
		self.top_right = dict(x = self.offset_x + self.width, y = self.offset_y)
		self.bottom_left = dict(x = self.offset_x, y = self.offset_y + self.height)
		self.bottom_right = dict(x = self.offset_x + self.width, y = self.offset_y + self.width)
	
	def update(self):
		# ask the world for the objects we should render
		self.entities = self.world.get_entities_in(self.top_left, self.top_right, self.bottom_left, self.bottom_right)

		# print ("scene", self.top_left, self.top_right, self.bottom_left, self.bottom_right)

	def render(self):
		# get all the entities and draw them
		for e in self.entities:
			e.draw(self.top_left['x'], self.top_left['y'], self.height)

	def translateX(self, x):
		if self.top_left['x'] + x < 0 or self.top_right['x'] + x > self.world.width:
			x = 0

		self.top_left['x'] += x
		self.top_right['x'] += x
		self.bottom_left['x'] += x
		self.bottom_right['x'] += x

	def translateY(self, y):
		if self.top_left['y'] + y < 0 or self.bottom_left['y'] + y > self.world.height:
			y = 0

		self.top_left['y'] += y
		self.top_right['y'] += y
		self.bottom_left['y'] += y
		self.bottom_right['y'] += y

	def add_entity(self, entity):
		self.entities.append(entity)

	def remove_entity(self, entity):
		self.entities.remove(entity)