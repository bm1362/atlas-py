class Entity(object):
	def __init__(self, **kwargs):
		self.position = dict(x=0, y=0)
        self.linearVelocity = dict(x=0, y=0)
        self.linearAcceleration = dict(x=0, y=0)
        self.rotationalVelocity = 0
        self.rotationalAcceleration = 0

    def update(self):
        pass

    def draw(self):
        pass
