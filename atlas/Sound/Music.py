import pyglet 

class Music(object):
	def __init__(self):

		self.bg_music_location = 'assets/mrrogers.wav'


	def play_bg(self):
		bg_music = pyglet.resource.media(self.bg_music_location)
		bg_music.play()