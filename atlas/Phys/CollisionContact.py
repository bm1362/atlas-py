"""
CollisionContact.py: A CollisionContact represents a collision between two rigid_bodies.
"""

from Contact import Contact
from Util.Vector2 import Vector2

class CollisionContact(Contact):
	def __init__(self, b1, b2, penetration_dist, penetration_axis, corrective_vector):
		# super(CollisionContact, self).__init__(b1, b2)
		self.b1 = b1
		self.b2 = b2
		self.penetration_dist = penetration_dist
		self.penetration_axis = penetration_axis
		self.corrective_vector = corrective_vector
		self.inv_mass_sum = self.b1.inv_mass + self.b2.inv_mass
		self.normal = self.b1.position.subtract(self.b2.position).normalize()

	def solve(self):
		self.correct_position()
		self.resolve_collision()

	def resolve_collision(self):
		# calculate relative velocity
		rv = self.b1.linear_velocity.subtract(self.b2.linear_velocity)

		# calculate relative projected onto penetration axis
		axis_vel = rv.dot_product(self.normal)

		# if they're moving away don't resolve
		if axis_vel > 0:
			return
	 	
	 	# get min restitution
	 	e = min(self.b1.restitution, self.b2.restitution)

	 	# calculate impulse scalar
	 	j = - (1 + e) * axis_vel
	 	j = j / (self.inv_mass_sum)

	 	# apply impulse
	 	impulse = self.normal.multiply_scalar(j)

	 	self.b1.linear_velocity.add_self(impulse.multiply_scalar(self.b1.inv_mass))
	 	self.b2.linear_velocity.subtract_self(impulse.multiply_scalar(self.b2.inv_mass))

	def correct_position(self):
		self.b1.translate(self.corrective_vector)
		self.b2.translate(self.corrective_vector.multiply_scalar(-1))