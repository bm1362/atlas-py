class world(object):
	def __init__(self):
		# list of objects that are within the physics environment
		self.bodies = []

		# list of objects that are in the world
		self.entities = []

	def get_entities_in(self, top_left, top_right, bottom_left, bottom_right):
		"""
			Returns a list of objects that are within the bounding box.
		""" 	
		# is it to the right of the left side of ths screen and below the top of the screen
		result = filter(lambda o: o.position['x'] > top_left['x'] and o.position['x'] < top_right['x'], self.entities)
		# is it inside the window
		result = filter(lambda o: o.position['y'] < bottom_left['y'] and o.position['y'] > top_left['y'], result)
		return result

		return filter(lambda o: o.position['x'] > top_left['x'] and o.position['y'] > bottom_left['y'] and o.position['x'] < top_right['x'] and o.position['y'] < bottom_right['y'], self.entities)

	def add_entity(self, entity):
		self.entities.append(entity)

	def remove_entity(self, entity):
		self.entities.remove(entity)

	def add_body(self, body):
		self.bodies.append(body)

	def remove_body(self, body):
		self.bodies.remove(body)