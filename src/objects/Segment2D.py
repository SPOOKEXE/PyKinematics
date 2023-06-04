
from math import cos, sin

from os import path as os_path
from sys import path as sys_path

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))

sys_path.append( os_path.join(FILE_DIRECTORY, "..") )

from fmath.Lerp import lerp_n, lerp_vec2
from fmath.Vector2 import Vector2

sys_path.pop()

class Segment2D:
	a : Vector2 = None
	angle : float = None
	length : float = None
	b : Vector2 = None

	parent = None
	child = None
	anchored = False

	def calculate_b(self):
		dx = self.length * cos(self.angle)
		dy = self.length * sin(self.angle)
		self.b.set( self.a.x + dx, self.a.y + dy )
		return self

	def setA(self, position : Vector2):
		self.a.set( position.x, position.y )

	def follow_segment(self, segment):
		self.follow_target( segment.a.x, segment.a.y )

	def follow_target(self, tx : float, ty : float):
		_dir = Vector2( tx - self.a.x, ty - self.a.y )
		_angle = _dir.heading()
		self.angle = _angle

		_dir.setMag(-self.length)
		self.a = Vector2( tx + _dir.x, ty + _dir.y )
		return self

	def update(self):
		self.calculate_b()
		return self

	def __init__(self, x, y, length_, angle_):
		self.a = Vector2(x=x, y=y)
		self.length = length_
		self.angle = angle_
		self.b = Vector2()
		self.calculate_b()
