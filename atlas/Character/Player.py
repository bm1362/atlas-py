import math
import pyglet
import Resources
from pyglet.window import key
from Util.Vector2 import Vector2
from Entity.Entity import Entity
from Phys.RigidBody import RigidBody
from Phys.Force import Force
'''
The player will take in a rigid body. This allows us to move the player using
the rigid body class, as the class has most of the functions needed to move
the player around.

Differences include:
	The player will not automatically rotate. His spaceship is special so he can
		stop it whenever he wants (it does it automatically)
	He will not have a natural acceleration to be dealt with. He has a thrust, that
		when applied, acts as his acceleration. This is used to update his velocity
	There will be a sprite drawn on his position. This ensures easy locateability for the
		user
'''
class Player(RigidBody):
	def __init__(self, body=None, **kwargs):
		super(Player, self).__init__(**kwargs)
		self.batch = pyglet.graphics.Batch()
		
		self.entity.color = (0, 0, 0, 0)

		# put the engine sprite to the image
		self.ship_sprite = pyglet.sprite.Sprite(img=Resources.player_image, batch=self.batch)
		self.engine_sprite = pyglet.sprite.Sprite(img=Resources.engine_image, batch=self.batch)
		self.engine_sprite.visible = False

		self.thrust = 2000.0
		self.rotate_speed = 200.0


	#Sets the image's anchor points to the center of the picture
	def center_image(self, image):
		image.anchor_x = image.width/2
		image.anchor_y = image.height/2


	def translate(self, dt, key_pressed):
		if key.A in key_pressed:
			self.entity.orientation -= self.rotate_speed * dt
		if key.D in key_pressed:
			self.entity.orientation += self.rotate_speed * dt
		if key.W in key_pressed:
			angle_radians = math.radians(self.entity.orientation)
			force = Vector2(x=math.cos(angle_radians) * self.thrust, y=math.sin(angle_radians) * self.thrust)
			self.add_impulse(Force(vector=force, offset=Vector2()))
			self.engine_sprite.visible = True
		else:
			self.engine_sprite.visible = False

		#If key up, make engine visible and at player position
		self.ship_sprite.rotation = self.entity.orientation
		self.ship_sprite.x = self.entity.position.x
		self.ship_sprite.y = self.entity.position.y
		
		self.engine_sprite.rotation = self.entity.orientation
		self.engine_sprite.x = self.entity.position.x
		self.engine_sprite.y = self.entity.position.y
		

	def draw(self, scene):
		s_y = scene.height - self.entity.position.y + scene.top_left['x']
		self.engine_sprite.y = s_y
		self.ship_sprite.x = self.entity.position.x
		self.ship_sprite.y = s_y
		self.batch.draw()
