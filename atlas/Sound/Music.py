import pyglet 


class Music(object):
	def __init__(self):

		self.location = 'assets/mrrogers.wav'
		self.source = pyglet.resource.media(self.location)
		self.player = pyglet.media.Player()
		self.player.queue(self.source)
		self.playing = True

		print self.player.eos_action

		self.player.eos_action = 'loop'

		print self.player.eos_action


	def play_bg(self):
		self.player.play()
		pass

	def pause_bg(self):
		if self.playing == True:
			self.player.pause()
			self.playing = False
		else:
			self.player.play()
			self.playing = True
		pass