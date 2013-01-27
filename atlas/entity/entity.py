from uuid import uuid4
class entity(object):
	def __init__(self, **kwargs):
		self.id = uuid4()

		if 'color' in kwargs:
			self.color = kwargs['color']
		else:
			self.color = (255, 255, 255, 255)

		if 'position' in kwargs:
			self.position = kwargs['position']
		else:
			self.position = dict(x = 0, y = 0)

	def draw():
		pass

	# def update():
	# 	pass