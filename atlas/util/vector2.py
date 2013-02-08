"""
vector2.py: Contains a collection of functions that aid in the various movements of the entities in our world.
"""

import math

class vector2(object):
	def __init__(self, **kwargs):
		self.x = float(kwargs.get('x', 0))
		self.y = float(kwargs.get('y', 0))

	# rotates a vector clockwise
	def rotate(self, angle):
	    x = self.x
	    y = self.y
	    cosa = math.cos(angle * math.pi / 180)
	    sina = math.sin(angle * math.pi / 180)

	    result = dict(x = x * cosa - y * sina, y = x * sina + y * cosa)
	    return result

	def angle_between(self, v2):
		dot = self.dot_product(v2)
		origin = vector2(x = 0, y = 0)
		d1 = self.distance_between(origin)
		d2 = v2.distance_between(origin)
		d_product = d1 * d2
		dot = dot / d_product
		dot = min(1,max(dot,-1))
		acos = math.acos(dot)
		return acos * 180 / math.pi

	def dot_product(self, v2):
		return self.x * v2.x + self.y * v2.y

	def distance_between(self, v2):
		dx = self.x - v2.x
		dy = self.y - v2.y
		return math.sqrt(dx * dx + dy * dy)

	def add(self, v2):
		return vector2(x = self.x + v2.x, y = self.y + v2.y)

	def add_self(self, v2):
		self.x += v2.x
		self.y += v2.y

		return self

	def subtract(self, v2):
		return vector2(x = self.x - v2.x, y = self.y - v2.y)

	def length(self):
		return math.sqrt(self.x * self.x + self.y * self.y)

	def multiply_scalar(self, scalar):
		return vector2(x = self.x * scalar, y = self.y * scalar)

	def multiply_scalar_self(self, scalar):

		self.x *= scalar
		self.y *= scalar
		return self

	def divide_scalar(self, scalar):
		if scalar != 0:
			x = float(self.x) / scalar
			y = float(self.y) / scalar
			return vector2(x = x, y = y)
		else:
			return vector2(x = 0, y = 0)

	def divide_scalar_self(self, scalar):
		if scalar != 0:
			self.x = float(self.x) / scalar
			self.y = float(self.y) / scalar
		else:
			self.x = 0
			self.y = 0

		return self

	def normalize(self):
		return self.divide_scalar(self.length())

	def equal(self, v2):
		return self.x == v2.x and self.y == v2.y

# Finds the angle that passes through any two points relative to the x-axis
def get_angle(point1, point2):
    opp = math.fabs(point1['x'] - point2['x'])
    adj = math.fabs(point1['y'] - point2['y'])
    theta = math.atan2(opp, adj)

    return theta

def test():
	a = vector2(x = 50, y = 0)
	b = vector2(x = 0, y = 50)

	assert a.dot_product(b) == 0, "vector2.dot_product failed."
	assert a.distance_between(b) == b.distance_between(a), "vector2.distance_between failed."
	assert a.angle_between(b) == 90, "vector2.angle_between failed."
	assert a.normalize().length() == 1, "vector2.normalize failed."
	assert a.multiply_scalar(50).x == 50, "vector2.mulitply_scalar failed"

	c = a.add(b)
	assert c.x == 50 and c.y == 50, "vector2.add failed."
	
	d = a.subtract(b)
	assert d.x == 50 and d.y == -50, "vector2.substract failed."

	e = b.add(a)
	assert c.equal(e) == True, "vector2.equal failed"

	print "passed all tests"
