class world(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height
		
		# list of objects that are within the physics environment
		self.bodies = []

		# list of objects that are in the world
		self.entities = []

	def get_entities_in(self, top_left, top_right, bottom_left, bottom_right):
		"""
			Returns a list of objects that are within the bounding box.
		"""
		# may not be correct needs to be updated
		result = filter(lambda o: o.position['x'] > top_left['x'] and o.position['x'] < top_right['x'], self.entities)
		result = filter(lambda o: o.position['y'] > top_left['y'] and o.position['y'] < bottom_right['y'], self.entities)
		return result
		
	def add_entity(self, entity):
		self.entities.append(entity)

	def remove_entity(self, entity):
		self.entities.remove(entity)

	def add_body(self, body):
		self.bodies.append(body)

	def remove_body(self, body):
		self.bodies.remove(body)