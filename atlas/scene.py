class scene(object):
	def __init__(self, world, **kwargs):
		self.entities = []
		self.world = world
		
		assert(self.world is not None)

		self.offset_x = kwargs.get('offset_x', 0)
		self.offset_y = kwargs.get('offset_y', 0)
	
	def update(self):
		self.entites = world.get_entities_in()
	def render(self):
		for e in self.entities:
			e.draw()

	def add_entity(self, entity):
		self.entities.append(entity)

	def remove_entity(self, entity):
		self.entities.remove(entity)