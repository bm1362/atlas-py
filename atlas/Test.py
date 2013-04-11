from Util.Vector2 import Vector2
import unittest


class VectorClassTestCases(unittest.TestCase):

	def setUp(self):
		self.v1 = Vector2(x=1, y=2)
		self.v2 = Vector2(x=5, y=5)
		self.v3 = Vector2(x=1.7976931348623157e+308, y=1.7976931348623157e+308)
		self.v4 = Vector2(x=-1.7976931348623157e+308, y=-1.7976931348623157e+308)
		self.v_a = Vector2(x=50, y=0)
		self.v_b = Vector2(x=0, y=50)

	def test__init__(self):
		self.assertEquals(self.v1.x, 1)
		self.assertEquals(self.v1.y, 2)

		self.assertAlmostEqual(self.v2.x, 5)
		self.assertAlmostEqual(self.v2.y, 5)

		self.assertAlmostEqual(self.v3.x, 1.7976931348623157e+308)
		self.assertAlmostEqual(self.v3.y, 1.7976931348623157e+308)

		self.assertAlmostEqual(self.v3.x, -1.7976931348623157e+308)
		self.assertAlmostEqual(self.v3.y, -1.7976931348623157e+308)

	def test_rotate(self):
		self.testVector = self.v2.rotate(180)
		self.assertAlmostEqual(self.testVector.x, -5)
		self.assertAlmostEqual(self.testVector.y, -5)

	def test_rotate_self(self):
		self.v2.rotate_self(180)
		self.assertAlmostEqual(self.v2.x, -5)
		self.assertAlmostEqual(self.v2.y, -5)

	def test_angle_between(self):
		self.assertAlmostEqual(self.v1.angle_between(self.v2), 18.43, places=2)
		assert self.v_a.angle_between(self.v_b) == 90, "vector2.angle_between failed."

	def test_dot_product(self):
		 assert self.v_a.dot_product(self.v_b) == 0, "vector2.dot_product failed."

	def test_distance_between(self):
		self.assertEquals(self.v_a.distance_between(self.v_b), self.v_b.distance_between(self.v_a))

	def test_add(self):
		pass

	def test_add(self):
		pass

	def test_add_self(self):
		pass

	def test_subtract(self):
		pass

	def test_length(self):
		pass

	# def test_multiply_scalar_self(self):
	# 	self.assertEquals(self.v_a.multiply_scalar(50).x, 50)

	def test_divide_scalar(self):
		pass

	def test_divide_scalar_self(self):
		pass

	def test_normalize(self):
		assert self.v_a.normalize().length() == 1, "vector2.normalize failed."

	def test_equal(self):
		pass

	def test_get_angle(self):
		pass



	def runTest(self):
		setUp()
		test__init__()
		test_rotate()
		test_rotate_self()
		test_angle_between()
		test_dot_product()
		test_distance_between()
		test_add()
		test_add_self()
		test_subtract()
	 	test_length()
		# test_multiply_scalar_self()
		test_divide_scalar()
		test_divide_scalar_self()
		test_normalize()
		test_equal()
		test_get_angle()

if __name__ == '__main__':
    unittest.main()




# v1 = Vector2(x=1, y=1)
# v2 = Vector2(x=5, y=5)


# print 'I am running a test'

# assert v1.x == 1, 'vectors initialization error v1x'
# assert v1.y == 1, 'vector initialization error v1y'
# assert v2.x == 5, 'vectors initialization error v2x'
# assert v2.y == 5, 'vectors initialization error v2y'

# v3 = v2.rotate(180)
# print v2.x
# print v2.y

# print v3.x
# print v3.y

# assert v3.x == -5, 'yo dawn'
# assert v3.y == -5, 'yo dawg'
# # assertAlmostEqual v3.x, -5.0), 'rotation by 180 degrees'
# # assertAlmostEqual(v3.y, -5.0), 'rotation by 180 degrees'



# print 'All tests passed'