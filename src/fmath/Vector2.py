
from math import atan2, nan, sqrt

class Vector2:
	x = y = 0

	def heading(self) -> float:
		return atan2(self.y, self.x)

	def mag(self):
		return sqrt( (self.x * self.x) + (self.y * self.y) )

	def zero(self):
		self.x = self.y = 0
	
	def nan(self):
		self.x = self.y = nan

	def unit(self):
		m = self.mag()
		if m == 0:
			self.nan()
		else:
			self.x /= m
			self.y /= m
		return self

	def mult(self, m : float):
		self.x *= m
		self.y *= m
		return self

	def setMag(self, mag : float):
		m = self.mag()
		# if mag == 0 or m == 0:
		# 	self.zero()
		# else:
		self.mult( mag / m )
		return self

	def set(self, x : float, y : float) -> None:
		self.x = x
		self.y = y
		return self

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
