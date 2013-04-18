import pyglet

def center_image(image):
	#Set the image's anchor points to the center
	image.anchor_x = image.width/2
	image.anchor_y = image.height/2

pyglet.resource.path = ['./assets']
pyglet.resource.reindex()

player_image = pyglet.resource.image("player.png")
center_image(player_image)

#Load flame to be attached to the player
engine_image = pyglet.resource.image("engine_flame.png")
#draw it behind the player
engine_image.anchor_x = engine_image.width * 1.5
engine_image.anchor_y = engine_image.height / 2
