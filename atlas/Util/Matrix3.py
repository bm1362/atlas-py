from Vector2 import Vector2
from Vector3 import Vector3

class Matrix3(object):
	def __init__(self, **kwargs):
		self._data = [[0,0,0],
					 [0,0,0],
					 [0,0,0]]

	def __repr__(self):
		return unicode(self._data)

	def _to_array(self):
		return self._data[0] + self._data[1] + self._data[2]

	def clone(self):
		ret = Matrix3()
		ret.set(self._data[0][0], self._data[0][1], self._data[0][2],
				self._data[1][0], self._data[1][1], self._data[1][2],
				self._data[2][0], self._data[2][1], self._data[2][2])

		return ret

	def set(self, d00, d01, d02, d10, d11, d12, d20, d21, d22):
		self._data = [[d00,d01,d02],
					 [d10,d11,d12],
					 [d20,d21,d22]]

		return self

	def identity(self):
		self.set(1, 0, 0,
				 0, 1, 0,
				 0, 0, 1)

		return self

	def normalize(self):
		""" Normalizes each vector in the matrix! Only useful for transformation matrices.
		"""
		for i in xrange(0, 3):
			v = Vector3(x=self._data[i][0], y=self._data[i][1], z=self._data[i][2])
			norm = v.normalize()
			self._data[i][0] = norm.x
			self._data[i][1] = norm.y
			self._data[i][2] = norm.z

		return self

	def clean(self, threshold=.01):

		for i in xrange(0, 3):
			for j in xrange(0, 3):
				if abs(self._data[i][j]) < threshold:
					self._data[i][j] = 0
		return self

	def multiply_vector2(self, v):
		"""
		Takes a Vector2 and creates a 3D Vector with Z = 0 then multiplies 
		it by the invoking matrix. Av = M
		"""
		ret = list()
		vect = [v.x, v.y, 1]
		for i in xrange(0, 3):
			res = 0
			for j in xrange(0, 3):
				res += self._data[i][j] * vect[j]

			ret.append(res)

		return Vector2(x=ret[0], y=ret[1])

	def multiply_vector3(self, v):
		"""
		Takes a Vector3 and multiplies
		it by the invoking matrix. Av = M
		"""
		ret = list()
		vect = [v.x, v.y, v.z]
		for i in xrange(0, 3):
			res = 0
			for j in xrange(0, 3):
				res += self._data[i][j] * vect[j]

			ret.append(res)

		return Vector3(x=ret[0], y=ret[1], z=ret[2])

	def multiply_matrix3(self, m):
		"""
		Result of A * M, where A is the invoking matrix and M is the matrix passed.
		"""
		mat = Matrix3()

		for i in xrange(0, 3):
			for j in xrange(0, 3):
				for k in xrange(0, 3):
					mat._data[i][j] += self._data[i][k] * m._data[k][j]

		return mat

	def multiply_scalar(self, s):
		mat = Matrix3()
		mat._data[0] = [x * s for x in self._data[0]]
		mat._data[1] = [x * s for x in self._data[1]]
		mat._data[2] = [x * s for x in self._data[2]]

		return mat

	def multiply_scalar_self(self, s):
		self._data[0] = [x * s for x in self._data[0]]
		self._data[1] = [x * s for x in self._data[1]]
		self._data[2] = [x * s for x in self._data[2]]

		return self

	def divide_scalar(self, s):
		mat = Matrix3()
		mat._data[0] = [x / s for x in self._data[0]]
		mat._data[1] = [x / s for x in self._data[1]]
		mat._data[2] = [x / s for x in self._data[2]]

		return mat

	def divide_scalar_self(self, s):
		self._data[0] = [x / s for x in self._data[0]]
		self._data[1] = [x / s for x in self._data[1]]
		self._data[2] = [x / s for x in self._data[2]]

		return self

	def determinant(self):
		a = self._to_array()
		return (a[0] * self.determinant2x2(a[4], a[5], a[7], a[8])) - (a[1] * self.determinant2x2(a[3], a[5], a[6], a[8])) + (a[2] * self.determinant2x2(a[3], a[4], a[6], a[7]))

	def determinant2x2(self, e00, e01, e10, e11):
		return (e00 * e11 - e01* e10)

	def add(self, m):
		ret = Matrix3()

		for i in xrange(0, 3):
			for j in xrange(0, 3):
				ret._data[i][j] = self._data[i][j] + m._data[i][j]

		return ret

	def inverse(self):

		d00 = self.determinant2x2(self._data[1][1], self._data[1][2], self._data[2][1], self._data[2][2])
		d01 = self.determinant2x2(self._data[0][2], self._data[0][1], self._data[2][2], self._data[2][1])
		d02 = self.determinant2x2(self._data[0][1], self._data[0][2], self._data[1][1], self._data[1][2])
		d10 = self.determinant2x2(self._data[1][2], self._data[1][0], self._data[2][2], self._data[2][0])
		d11 = self.determinant2x2(self._data[0][0], self._data[0][2], self._data[2][0], self._data[2][2])
		d12 = self.determinant2x2(self._data[0][2], self._data[0][0], self._data[1][2], self._data[1][0])
		d20 = self.determinant2x2(self._data[1][0], self._data[1][1], self._data[2][0], self._data[2][1])
		d21 = self.determinant2x2(self._data[0][1], self._data[0][0], self._data[2][1], self._data[2][0])
		d22 = self.determinant2x2(self._data[0][0], self._data[0][1], self._data[1][0], self._data[1][1])

		det = self.determinant()

		inv = Matrix3()
		inv.set(d00, d01, d02, d10, d11, d12, d20, d21, d22)
		inv.multiply_scalar_self(det)

		return inv

	def transpose(self):
		mat = Matrix3()
		for i in xrange(0, 3):
			for j in xrange(0, 3):
				mat._data[i][j] = self._data[j][i]

		return mat

	def equals(self, m):
		return self._data == m._data

	def test(self):

		a = Matrix3()
		a.set(7, -3, -3, -1, 1, 0, -1, 0, 1)

		b = Matrix3()
		b.set(1, 3, 3, 1, 4, 3, 1, 3, 4)

		ident = Matrix3()
		ident.identity()

		c = a.multiply_matrix3(b)

		assert c.equals(ident), "Multiply matrix is incorrect"

		x = Matrix3()
		x.identity()
		y = Matrix3()
		y.set(1,2,3,4,5,6,7,8,9)
		z = Matrix3()
		z.set(2,2,3,4,6,6,7,8,10)

		assert x.add(y).equals(z), "Add matrix is incorrect"

		a.set(5, 10, 20, 88, 75, 41, 7, 8, 9)
		assert a.determinant() == 265, "Determinant is incorrect"


