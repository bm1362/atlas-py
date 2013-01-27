from uuid import uuid4
class entity(object):
	def __init__(self, **kwargs):
		self.id = uuid4()

		self.color = kwargs.get('color', (255, 255, 255, 255))
		self.position = kwargs.get('position', dict(x=0, y=0))

	def draw():
		pass

	# def update():
	# 	pass
