
from math import cos, sin
from typing import Union

from os import path as os_path
from selectors import BaseSelector
from sys import path as sys_path

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))

sys_path.append( os_path.join(FILE_DIRECTORY, "..") )

from fmath.Lerp import Lerp
from fmath.Bezier import Bezier
from fmath.Vector2 import Vector2

sys_path.pop()

class Segment2D:
	a : Vector2 = None
	angle : float = None
	length : float = None
	b : Vector2 = None

	parent = None
	child = None

	def calculate_b(self):
		dx = self.length * cos(self.angle)
		dy = self.length * sin(self.angle)
		self.b.set( self.a.x + dx, self.a.y + dy )
		return self

	def setA(self, position : Vector2):
		self.a.set( position.x, position.y )

	def follow_target(self, tx : float, ty : float):
		_dir = Vector2( tx - self.a.x, ty - self.a.y )
		_angle = _dir.heading()
		self.angle = _angle

		_dir.setMag(-self.length)
		self.a = Vector2( tx + _dir.x, ty + _dir.y )
		return self

	def follow_segment(self, segment):
		self.follow_target( segment.a.x, segment.a.y )

	def update(self):
		self.calculate_b()
		return self

	def __init__(self, x, y, length_, angle_):
		self.a = Vector2(x=x, y=y)
		self.length = length_
		self.angle = angle_
		self.b = Vector2()
		self.calculate_b()

class Tentacle2D:
	SEGMENTS : list[Segment2D] = []
	TOTAL_SEGMENTS = 0
	BASE_VECTOR = None

	def get_angles(self) -> list:
		coords = []
		for seg in self.SEGMENTS:
			coords.append( seg.angle )
		return coords

	def set_angles(self, angles : list) -> list:
		for index, seg in enumerate(self.SEGMENTS):
			seg.angle = angles[index]
		for seg in self.SEGMENTS:
			seg.update()

	def shift_segments(self):
		self.SEGMENTS[0].calculate_b()
		for i in range(1, len(self.SEGMENTS), 1):
			self.SEGMENTS[i].setA( self.SEGMENTS[i-1].b )
			self.SEGMENTS[i].calculate_b()

	def follow(self, tx : float, ty : float):
		length = len(self.SEGMENTS)
		endd = self.SEGMENTS[length-1]
		endd.follow_target(tx, ty)
		endd.update()
		for i in range(length-2, -1, -1):
			self.SEGMENTS[i].follow_segment(self.SEGMENTS[i+1])
			self.SEGMENTS[i].update()

		# check if there is a base vector
		if self.BASE_VECTOR == None:
			return

		self.SEGMENTS[0].setA(self.BASE_VECTOR)
		self.shift_segments()

	def __init__(self, total_segments : int, segment_length : Union[int, list]):
		self.TOTAL_SEGMENTS = total_segments
		self.SEGMENTS : list[Segment2D] = []

		if type(segment_length) == int:
			segment_length = [segment_length]

		# generate all the segments
		if type(segment_length) == list:
			length = len(segment_length)
			baseSegment = Segment2D(0, 0, segment_length[0], 1)
			for idx in range(total_segments):
				seg_next = Segment2D(baseSegment.b.x, baseSegment.b.y, segment_length[ min(idx, length)-1 ], 1)
				seg_next.parent = baseSegment
				baseSegment.child = seg_next
				self.SEGMENTS.insert(-1, seg_next)
				baseSegment = seg_next
		else:
			raise ValueError
