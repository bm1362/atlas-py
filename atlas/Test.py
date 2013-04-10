from Util.Vector2 import Vector2
import unittest



import unittest

class VectorClassTestCases(unittest.TestCase):

	def setUp(self):
		self.v1 = Vector2(x=1, y=2)
		self.v2 = Vector2(x=5, y=5)
		self.v3 = Vector2(x=1.7976931348623157e+308, y=1.7976931348623157e+308)

	def testInit(self):
		self.assertEquals(self.v1.x, 1)
		self.assertEquals(self.v1.y, 2)

		self.assertAlmostEqual(self.v2.x, 5)
		self.assertAlmostEqual(self.v2.y, 5)

		self.assertAlmostEqual(self.v3.x, 1.7976931348623157e+308)
		self.assertAlmostEqual(self.v3.y, 1.7976931348623157e+308)

	def testRotate(self):
		self.v3 = self.v2.rotate(180)
		self.v4 = self.v2.rotate(180)
		self.assertAlmostEqual(self.v3.x, -5)
		self.assertAlmostEqual(self.v3.y, -5)

		


	def runTest(self):
		testInit()

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