"""
rigid_body.py: A class representation of an object that obeys physics rules in our world.
"""

from entity.entity import entity
from util.vector2 import vector2
from force import force
import entity

class rigid_body(object):
	def __init__(self, **kwargs):
		self.entity = kwargs.get('entity', None)
		self.forces = kwargs.get('forces', [])
		self.impulses = kwargs.get('impulses', [])
		self.mass = kwargs.get('mass', 1)
		self.velocity = kwargs.get('velocity', vector2(x=0, y=0))
		self.acceleration = kwargs.get('acceleration', vector2(x=0, y=0))
		self.momentum = kwargs.get('momentum', vector2(x=0, y=0))
		self.resistance = .99

		assert self.mass > 0, "Invalid mass."
		assert self.entity is not None, "Invalid entity."

	def add_force(self, force):
		self.forces.append(force)

	def remove_force(self, force):
		self.forces.remove(force)

	# does not attempt rotational at the moment
	def update_acceleration(self):
		for _ in self.forces:
			self.acceleration.add_self(_.vector)

		# add any impulses
		for _ in self.impulses:
			self.acceleration.add_self(_.vector)

		self.impulses = []

	def update(self, dt):
		# update object's acceleration
		self.update_acceleration()

		# update object's velocity
		self.velocity.add_self(self.acceleration.multiply_scalar(dt))

		# update velocity based on resistance
		self.velocity.multiply_scalar(self.resistance)

		# update object's position
		self.entity.translate_vector(self.velocity)

	def add_impulse(self, force):
		self.impulses.append(force)