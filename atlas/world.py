class world(object):
	def __init__(self):
		# list of objects that are within the physics environment
		self.bodies = []

		# list of objects that are in the world
		self.entities = []

	def get_objects_in(top_left, top_right, bottom_left, bottom_right):
		"""
			Returns a list of objects that are within the bounding box.
		"""
		return "unimplemented"

	def add_entity(self, entity):
		self.entities.append(entity)

	def remove_entity(self, entity):
		self.entities.remove(entity)

	def add_body(self, body):
		self.bodies.append(body)

	def remove_body(self, body):
		self.bodies.remove(body)
