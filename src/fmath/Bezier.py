
from fmath.Lerp import Lerp

class Bezier:
	@staticmethod
	def Quad(alpha, p0, p1, p2):
		l1 = Lerp.lerp_n(p0, p1, alpha)
		l2 = Lerp.lerp_n(p1, p2, alpha)
		return Lerp.lerp_n(l1, l2, alpha)

	@staticmethod
	def Cubic(alpha, p0, p1, p2, p3):
		l1 = Lerp.lerp_n(p0, p1, alpha)
		l2 = Lerp.lerp_n(p1, p2, alpha)
		l3 = Lerp.lerp_n(p2, p3, alpha)
		a = Lerp.lerp_n(l1, l2, alpha)
		b = Lerp.lerp_n(l2, l3, alpha)
		return Lerp.lerp_n(a, b, alpha)

	@staticmethod
	def Recursive(alpha : float, points : list):
		if len(points) == 3:
			return Bezier.Quad(alpha, points[0], points[1], points[2])
		elif len(points) == 2:
			return Lerp.lerp_n(points[0], points[1], alpha)
		depth = []
		for index in range( 0, len(points) - 3, 1 ):
			p0 = points[index]
			p1 = points[index+1]
			p2 = points[index+2]
			depth.append(Bezier.Quad(alpha, p0, p1, p2))
		return Bezier.Recursion(alpha, depth)
