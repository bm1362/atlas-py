from util.geometry import is_in_polygon

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
		# returns any object with a vertice within the dimensions given
		result = []
		for _ in self.entities:
			for v in _.get_abs_vertices():
				vertices = ((top_left['x'], top_left['y']),(top_right['x'], top_right['y']),(bottom_left['x'], bottom_left['y']),(bottom_right['x'], bottom_right['y']))
				if is_in_polygon(vertices, (v['x'], v['y'])):
					result.append(_)
					break

		return result
		
	def add_entity(self, entity):
		self.entities.append(entity)

	def remove_entity(self, entity):
		self.entities.remove(entity)

	def add_body(self, body):
		self.bodies.append(body)

	def remove_body(self, body):
		self.bodies.remove(body)