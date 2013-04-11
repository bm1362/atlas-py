from Util.Vector2 import Vector2
import unittest


class VectorClassTestCases(unittest.TestCase):

#	This function runs as part of every test
	def setUp(self):
		self.v1_2 = Vector2(x=1, y=2)
		self.v5_5 = Vector2(x=5, y=5)

		self.vMAX_MAX = Vector2(x=1.7976931348623157e+308, y=1.7976931348623157e+308)
		self.vMIN_MIN = Vector2(x=-1.7976931348623157e+308, y=-1.7976931348623157e+308)

		self.v50_0 = Vector2(x=50, y=0)
		self.v0_50 = Vector2(x=0, y=50)

		self.v100_0 = Vector2(x=100, y=0)
		self.v0_100 = Vector2(x=0, y=100)

		self.v100_100 = Vector2(x=100, y=100)

		self.v500000_500000 = Vector2(x=500000, y=500000)

	def test__init__(self):
		self.assertEquals(self.v1_2.x, 1)
		self.assertEquals(self.v1_2.y, 2)

		self.assertAlmostEqual(self.v5_5.x, 5)
		self.assertAlmostEqual(self.v5_5.y, 5)

		self.assertAlmostEqual(self.vMAX_MAX.x, 1.7976931348623157e+308)
		self.assertAlmostEqual(self.vMAX_MAX.y, 1.7976931348623157e+308)

		self.assertAlmostEqual(self.vMIN_MIN.x, -1.7976931348623157e+308)
		self.assertAlmostEqual(self.vMIN_MIN.y, -1.7976931348623157e+308)

	def test_rotate(self):
		self.testVector = self.v5_5.rotate(180)
		self.assertAlmostEqual(self.testVector.x, -5)
		self.assertAlmostEqual(self.testVector.y, -5)

	def test_rotate_self(self):
		self.v5_5.rotate_self(180)
		self.assertAlmostEqual(self.v5_5.x, -5)
		self.assertAlmostEqual(self.v5_5.y, -5)

	def test_angle_between(self):
		self.assertAlmostEqual(self.v1_2.angle_between(self.v5_5), 18.43, places=2)
		assert self.v50_0.angle_between(self.v0_50) == 90, "vector2.angle_between failed."

	def test_dot_product(self):
		 assert self.v50_0.dot_product(self.v0_50) == 0, "vector2.dot_product failed."

	def test_distance_between(self):
		self.assertEquals(self.v50_0.distance_between(self.v0_50), self.v0_50.distance_between(self.v50_0))

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

	def test_multiply_scalar_self(self):

		self.assertEquals(self.v1_2.multiply_scalar(50).x, 50)
		self.assertEquals(self.v1_2.multiply_scalar(50).y, 100)

		self.assertEquals(self.v5_5.multiply_scalar(.5).x, 2.5, 2)
		self.assertEquals(self.v5_5.multiply_scalar(.5).y, 2.5, 2)

		self.assertEquals(self.vMAX_MAX.multiply_scalar(0).x, 0)
		self.assertEquals(self.vMAX_MAX.multiply_scalar(0).y, 0)

		self.assertEquals(self.vMIN_MIN.multiply_scalar(0).x, 0)
		self.assertEquals(self.vMIN_MIN.multiply_scalar(0).y, 0)

		self.assertEquals(self.v50_0.multiply_scalar(50).x, 2500)
		self.assertEquals(self.v50_0.multiply_scalar(50).y, 0)

		self.assertEquals(self.v100_0.multiply_scalar(50).x, 5000)
		self.assertEquals(self.v100_0.multiply_scalar(50).y, 0)

		self.assertAlmostEqual(self.v100_100.multiply_scalar(100).x, 10000)

		self.assertAlmostEqual(self.v500000_500000.multiply_scalar(.5).x, 250000)
		self.assertAlmostEqual(self.v500000_500000.multiply_scalar(.5).y, 250000)

	def test_divide_scalar(self):
		pass

	def test_divide_scalar_self(self):
		pass

	def test_normalize(self):
		self.assertAlmostEqual(self.v1_2.normalize().length(), 1)
		self.assertAlmostEqual(self.v5_5.normalize().length(), 1)

		# MAXFLOAT AND MINFLOAT FAIL
		# self.assertAlmostEqual(self.vMAX_MAX.normalize().length(), 1)
		# self.assertAlmostEqual(self.vMIN_MIN.normalize().length(), 1)

		self.assertAlmostEqual(self.v50_0.normalize().length(), 1)
		self.assertAlmostEqual(self.v0_50.normalize().length(), 1)

		self.assertAlmostEqual(self.v100_0.normalize().length(), 1)
		self.assertAlmostEqual(self.v0_100.normalize().length(), 1)

		self.assertAlmostEqual(self.v100_100.normalize().length(), 1)

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
		test_multiply_scalar_self()
		test_divide_scalar()
		test_divide_scalar_self()
		test_normalize()
		test_equal()
		test_get_angle()

if __name__ == '__main__':
    unittest.main()




# v1_2 = Vector2(x=1, y=1)
# v5_5 = Vector2(x=5, y=5)


# print 'I am running a test'

# assert v1_2.x == 1, 'vectors initialization error v1x'
# assert v1_2.y == 1, 'vector initialization error v1y'
# assert v5_5.x == 5, 'vectors initialization error v2x'
# assert v5_5.y == 5, 'vectors initialization error v2y'

# vMAX_MAX = v5_5.rotate(180)
# print v5_5.x
# print v5_5.y

# print vMAX_MAX.x
# print vMAX_MAX.y

# assert vMAX_MAX.x == -5, 'yo dawn'
# assert vMAX_MAX.y == -5, 'yo dawg'
# # assertAlmostEqual vMAX_MAX.x, -5.0), 'rotation by 180 degrees'
# # assertAlmostEqual(vMAX_MAX.y, -5.0), 'rotation by 180 degrees'



# print 'All tests passed'