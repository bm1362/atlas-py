import pyglet 

class Music(object):
	def __init__(self):
		pass
		# self.location = 'assets/mrrogers.wav'
		# self.source = pyglet.resource.media(self.location)
		self.player = pyglet.media.Player()
		# self.player.queue(self.source)

	def play_bg(self):
		self.player.play()
		
	def pause_bg(self):
		if self.player.playing == True:
			self.player.pause()
		else:
			self.player.play()

		self.bg_music.pause()