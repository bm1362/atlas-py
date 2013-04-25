"""
CollisionContact.py: A CollisionContact represents a collision between two rigid_bodies.
"""

from Contact import Contact
from Util.Vector2 import Vector2
from Force import Force
import pyglet
from pyglet.gl import *
from Util.Vector3 import *
from math import pi, sin, cos
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

	def circle(self, x,y,radius, color):
		iterations = int(2 * radius * pi)
		s = sin(2 * pi/iterations)
		c = cos(2 * pi/iterations)

		dx, dy = radius, 0
		glColor3f(color[0], color[1], color[2])
		glBegin(GL_TRIANGLE_FAN)
		glVertex2f(x, y)
		for i in xrange(iterations):
			glVertex2f(x+dx, y+dy)
			dx, dy = (dx * c - dy * s), (dy * c + dx * s)
		glEnd()

	def line(self, start, end, color):
		glColor3f(color[0], color[1], color[2])
		glBegin(GL_LINES)
		glVertex2f(start.x, start.y)
		glVertex2f(end.x, end.y)
		glEnd()

	def draw(self):
		pass
		# self.circle(self.b1.position.x, self.b1.position.y, 25, (.5, 0, 0))
		# self.circle(self.b2.position.x, self.b2.position.y, 25, (0, .5, 0))
		# offset = self.normal.multiply_scalar(self.b1.size)
		# self.line(self.b1.position, self.b1.position.add(offset), (0, 0, .5))
		# self.circle(self.b1.position.add(offset).x, self.b1.position.add(offset).y, 10, (1,1,1))

	def resolve_collision(self):

		n3 = vector3_from_vector2(self.normal)
		# calculate relative velocity
		rv = vector3_from_vector2(self.b1.linear_velocity.subtract(self.b2.linear_velocity))

		# calculate relative projected onto penetration axis
		axis_vel = rv.dot_product(n3)

		# if they're moving away don't resolve
		if axis_vel > 0:
			return
	 	
	 	# get min restitution
	 	e = min(self.b1.restitution, self.b2.restitution)

	 	# calculate impulse scalar
	 	j = - (1 + e) * axis_vel
	 	j = j / (self.inv_mass_sum)

	 	# apply impulse
	 	impulse = n3.multiply_scalar(j)

	 	impulse_b1 = impulse.multiply_scalar(self.b1.inv_mass)
	 	impulse_b2 = impulse.multiply_scalar(-self.b2.inv_mass)
	 	offset_b1 = n3.multiply_scalar(self.b1.size)
	 	offset_b2 = n3.multiply_scalar(-self.b2.size)
	 	torque_b1 = impulse_b1.cross(offset_b1).multiply_scalar(self.b1.mass)
	 	torque_b2 = impulse_b2.cross(offset_b2).multiply_scalar(self.b2.mass)

	 	self.b1.angular_momentum.add_self(Vector3(x=0,y=0,z=torque_b1.length()))
	 	self.b2.angular_momentum.add_self(Vector3(x=0,y=0,z=torque_b2.length()))
	 	# print impulse_b1, impulse_b2
	 	# print offset_b1, offset_b2
	 	print (self.b1.angular_momentum, torque_b1), torque_b2

	 	self.b1.linear_velocity.add_self(impulse_b1)
	 	self.b2.linear_velocity.add_self(impulse_b2)

	def correct_position(self):
		self.b1.translate(self.corrective_vector)
		self.b2.translate(self.corrective_vector.multiply_scalar(-1))