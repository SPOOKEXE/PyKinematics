
from math import floor, pi, cos, sin
from utility import DrawApp, run_draw_widget

from os import path as os_path
from sys import path as sys_path

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))

sys_path.append( os_path.join(FILE_DIRECTORY, "..") )

from src.fmath.Vector2 import Vector2
from src.objects.Segment2D import Segment2D, Tentacle2D

sys_path.pop()

def run_2d_test():
	WIDGET_SIZE = (800, 800)

	CENTER_POINT = Vector2(WIDGET_SIZE[0] / 2, WIDGET_SIZE[1] / 2)
	CIRCLE_RADIUS = 160

	TOTAL_SEGMENTS = 8
	SEGMENT_LENGTHS = [30, 20, 10]

	#segment_colors = ['white']
	segment_colors = ["red", "blue", "orange", "white"]
	tentacles_list = []

	step = (pi * 2) / TOTAL_SEGMENTS
	for idx in range(TOTAL_SEGMENTS):
		angle = step * idx

		anchorPoint = Vector2(CENTER_POINT.x + (CIRCLE_RADIUS * cos(angle)), CENTER_POINT.y + (CIRCLE_RADIUS * sin(angle)))
		tentacle = Tentacle2D(TOTAL_SEGMENTS, SEGMENT_LENGTHS)
		tentacle.BASE_VECTOR = anchorPoint
		tentacles_list.append( tentacle )

	def pre_update(self : DrawApp):
		nonlocal tentacles_list
		mx, my = self.get_mouse_xy()
		for t in tentacles_list:
			t.follow(mx, my)

	def post_update(self : DrawApp):
		pass

	def pre_draw(self : DrawApp):
		nonlocal tentacles_list
		self.clear_screen()

		for t in tentacles_list:
			length = len(t.SEGMENTS)
			for index in range(length):
				segment = t.SEGMENTS[index]
				self.draw_line(
					segment.a.x, segment.a.y,
					segment.b.x, segment.b.y,
					fill=segment_colors[index%len(segment_colors)],
					width=max(8 - floor((index * 12) / length), 2)
				)

	def post_draw(self : DrawApp):
		pass

	run_draw_widget(PRE_UPDATE=pre_update, POST_UPDATE=post_update, PRE_DRAW=pre_draw, POST_DRAW=post_draw, WIDGET_SIZE=WIDGET_SIZE)

if __name__ == '__main__':
	run_2d_test()
