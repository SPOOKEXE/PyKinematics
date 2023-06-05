from os import path as os_path
from sys import path as sys_path

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))

sys_path.append( os_path.join(FILE_DIRECTORY, "..") )

from fmath.Vector2 import Vector2

sys_path.pop()

class Lerp:
	@staticmethod
	def lerp_n(start : float, goal : float, alpha : float) -> float:
		if alpha <= 0:
			return start
		if alpha >= 1:
			return goal
		return (1-alpha) * start + alpha * goal

	@staticmethod
	def lerp_vec2(vecA : Vector2, vecB : Vector2, alpha : float) -> Vector2:
		return Vector2( Lerp.lerp_n(vecA.x, vecB.x, alpha), Lerp.lerp_n(vecA.y, vecB.y, alpha) )

