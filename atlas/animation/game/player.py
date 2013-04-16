import pyglet
import math
from pyglet.window import key

import physicalobject, resources

class Player(physicalobject.PhysicalObject):

	def __init__(self, *args, **kwargs):
		super(Player, self).__init__(img=resources.player_image, *args, **kwargs)
		#make the flame to know when the ship is thrusting
		self.engine_sprite = pyglet.sprite.Sprite(img=resources.engine_image, *args, **kwargs)
		self.engine_sprite.visible = False

		#Thrust speed to move
		self.thrust = 300.0
		#Rotation speed to move
		self.rotate_speed = 200.0

		#Initialize the key_handler
		self.key_handler = key.KeyStateHandler()


	def update(self, dt):
		super(Player, self).update(dt)

		if self.key_handler[key.LEFT]:
			self.rotation -= self.rotate_speed * dt
		if self.key_handler[key.RIGHT]:
			self.rotation += self.rotate_speed * dt

		if self.key_handler[key.UP]:
			angle_radians = -math.radians(self.rotation)
			force_x = math.cos(angle_radians) * self.thrust * dt
			force_y = math.sin(angle_radians) * self.thrust * dt
			self.velocity_x += force_x
			if self.velocity_x > 1500:
				self.velocity_x = 1500
			self.velocity_y += force_y
			if self.velocity_y > 1500:
				self.velocity_y = 1500

			#If key up, make engine visible and at player position
			self.engine_sprite.rotation = self.rotation
			self.engine_sprite.x = self.x
			self.engine_sprite.y = self.y
			self.engine_sprite.visible = True

		else:
			self.engine_sprite.visible = False

	def delete(self):
		self.engine_sprite.delete()
		super(Player, self).delete()
