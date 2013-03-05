import pyglet 


class Music(object):
	def __init__(self):

		# self.location = 'assets/boing_x.wav'
		self.location = 'assets/mrrogers.wav'
		self.source = pyglet.resource.media(self.location)
		self.player = pyglet.media.Player()
		self.player.queue(self.source)
		self.playing = True
		self.pausing = 0

		self.player.eosaction = 'loop'


	def play_bg(self):
		self.player.play()
		pass

	def pause_bg(self):
		self.pausing += 1
		print 'pausing ', self.pausing
		if self.player.playing == True:
			self.player.pause()
		else:
			self.player.play()