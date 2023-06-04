
from fmath.Vector2 import Vector2

class Lerp:
	@staticmethod
	def lerp_n(start : float, goal : float, alpha : float) -> float:
		if alpha <= 0:
			return start
		if alpha >= 1:
			return goal
		return ((1-alpha) * start) + (alpha * goal)

	@staticmethod
	def lerp_vec2(vecA : Vector2, vecB : Vector2, alpha : float) -> Vector2:
		return Vector2( Lerp.lerp_n(vecA.x, vecB.x, alpha), Lerp.lerp_n(vecA.y, vecB.y, alpha) )

