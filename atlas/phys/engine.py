class engine(object):
	def __init__(self):
		self.bodies = []
		pass

	def update(self):
		for _ in self.bodies:
			_.update()

		pass

	def detect_collision(body1, body2):
		pass
	