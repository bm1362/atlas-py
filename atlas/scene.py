class scene(object):
	def __init__(self, world, **kwargs):
		self.entities = []
		self.world = world
		
		assert(self.world is not None)

		self.offset_x = kwargs.get('offset_x', 0)
		self.offset_y = kwargs.get('offset_y', 0)
		self.width = kwargs.get('width', 300)
		self.height = kwargs.get('height', 300)
	
	def update(self):
		top_left = dict(x = self.offset_x, y = self.offset_y)
		top_right = dict(x = self.offset_x + self.width, y = self.offset_y)
		bottom_left = dict(x = self.offset_x, y = self.offset_y + self.height)
		bottom_right = dict(x = self.offset_x + self.width, y = self.offset_y + self.height)

		self.entities = self.world.get_entities_in(top_left, top_right, bottom_left, bottom_right)

		print "Scene"
		print top_left
		print top_right
		print bottom_left
		print bottom_right
		print "/Scene"

	def render(self):
		for e in self.entities:
			e.draw(self.offset_x, self.offset_y)
			print e.position

	def add_entity(self, entity):
		self.entities.append(entity)

	def remove_entity(self, entity):
		self.entities.remove(entity)