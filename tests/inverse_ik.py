
from math import floor
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

	segment_colors = ["red", "blue", "orange", "white"]
	tentacle = Tentacle2D(3, [200, 150, 100])
	tentacle.BASE_VECTOR = Vector2( WIDGET_SIZE[0] / 2, WIDGET_SIZE[1] )

	def pre_update(self : DrawApp):
		nonlocal tentacle
		mx, my = self.get_mouse_xy()
		tentacle.follow(mx, my)

	def post_update(self : DrawApp):
		pass

	def pre_draw(self : DrawApp):
		nonlocal tentacle
		self.clear_screen()

		length = len(tentacle.SEGMENTS)
		for index in range(length):
			segment = tentacle.SEGMENTS[index]
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
