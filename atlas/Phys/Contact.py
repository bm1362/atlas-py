"""
Contact.py: A Contact represents some form of contact between two rigid_bodies.
"""

class Contact(object):
	def ___init__(self, b1, b2):
		super(Contact, self).__init__()
		self.b1 = b1
		self.b2 = b2

	def solve(self):
		return "Unimplemented"
