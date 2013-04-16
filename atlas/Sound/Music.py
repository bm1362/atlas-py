import pyglet 

class Music(object):
	def __init__(self):

		self.bg_music_location = 'assets/mrrogers.wav'
		self.bg_music = pyglet.resource.media(self.bg_music_location)


	def play_bg(self):
		self.bg_music.play()

	def stop_bg(self):
		self.bg_music.stop()

	def pause_bg(self):
		self.bg_music.pause()