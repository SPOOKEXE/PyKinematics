
from math import floor
from utility import DrawApp, run_draw_widget

from os import path as os_path
from sys import path as sys_path

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))

sys_path.append( os_path.join(FILE_DIRECTORY, "..") )

from src.fmath.Vector2 import Vector2
from src.objects.Segment2D import Segment2D

sys_path.pop()

def run_2d_test():

	WIDGET_SIZE = (800, 800)
	TOTAL_SEGMENTS = 80
	SEGMENT_LENGTH = 8

	segments : list[Segment2D] = []
	baseVector = Vector2( WIDGET_SIZE[0] / 2, WIDGET_SIZE[1] )

	baseSegment = Segment2D(0, 0, SEGMENT_LENGTH, 1)
	for _ in range(TOTAL_SEGMENTS):
		seg_next = Segment2D(baseSegment.b.x, baseSegment.b.y, SEGMENT_LENGTH, 1)
		seg_next.parent = baseSegment
		baseSegment.child = seg_next
		segments.append(seg_next)
		baseSegment = seg_next

	def pre_update(self : DrawApp):
		nonlocal baseSegment, baseVector
		mx, my = self.get_mouse_xy()

		length = len(segments)
		endd = segments[length-1]
		endd.follow_target(mx, my)
		endd.update()
		for i in range(length-2, -1, -1):
			segments[i].follow_segment(segments[i+1])
			segments[i].update()

		segments[0].setA(baseVector)
		segments[0].calculate_b()
		for i in range(1, length, 1):
			segments[i].setA( segments[i-1].b )
			segments[i].calculate_b()

	def post_update(self : DrawApp):
		pass

	def pre_draw(self : DrawApp):
		nonlocal baseSegment
		self.clear_screen()

		c, color = 0, ["red", "blue", "orange", "white"]
		next_seg = baseSegment
		while next_seg != None:
			c += 1
			weight = max(8 - floor((c * 12) / TOTAL_SEGMENTS), 2)
			col = color[c%len(color)]
			self.draw_line(next_seg.a.x, next_seg.a.y, next_seg.b.x, next_seg.b.y, fill=col, width= weight)
			next_seg = next_seg.parent

	def post_draw(self : DrawApp):
		pass

	run_draw_widget(PRE_UPDATE=pre_update, POST_UPDATE=post_update, PRE_DRAW=pre_draw, POST_DRAW=post_draw, WIDGET_SIZE=WIDGET_SIZE)

if __name__ == '__main__':
	run_2d_test()
