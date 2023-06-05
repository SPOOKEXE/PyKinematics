
from math import floor, pi, cos, sin
from utility import DrawApp, create_draw_widget

from os import path as os_path
from sys import path as sys_path

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))

sys_path.append( os_path.join(FILE_DIRECTORY, "..") )

from src.fmath.Vector2 import Vector2
from src.fmath.Lerp import Lerp
from src.objects.Segment2D import Segment2D, Tentacle2D

sys_path.pop()

def run_2d_test():
	WIDGET_SIZE = (800, 800)

	TOTAL_SEGMENTS = 3
	SEGMENT_LENGTHS = [200, 200, 150]

	#segment_colors = ['white']
	segment_colors = ["red", "blue", "orange", "white"]
	anchorPoint = Vector2(WIDGET_SIZE[0] / 2, WIDGET_SIZE[1])

	tentacle = Tentacle2D(TOTAL_SEGMENTS, SEGMENT_LENGTHS)
	tentacle.BASE_VECTOR = anchorPoint

	active_angles = None
	target_angles = None
	alpha = 0
	def mouse1_down(self, event) -> None:
		nonlocal active_angles, target_angles, alpha
		target = tentacle.get_angles()
		if active_angles == None:
			active_angles = target
		else:
			target_angles = target
			alpha = 0

	def mouse2_down(self, event) -> None:
		nonlocal active_angles, target_angles, alpha
		active_angles = None
		target_angles = None
		alpha = 0

	def lerp_array( arr0 : list, arr1 : list, alpha : float ) -> list:
		lerped = []
		for index, element in enumerate(arr0):
			lerped.append( Lerp.lerp_n(element, arr1[index], alpha) )
		return lerped

	def pre_update(self : DrawApp):
		nonlocal tentacle, active_angles, target_angles, alpha
		if active_angles != None and target_angles != None:
			alpha = min( alpha + 0.0015, 1 )
			tentacle.set_angles( lerp_array(active_angles, target_angles, alpha) )
			tentacle.shift_segments()
			if alpha == 1:
				active_angles = None
				target_angles = None
				alpha = 0
		else:
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

	app = create_draw_widget(WIDGET_SIZE=WIDGET_SIZE)

	app.set_update_methods(
		pre_update=pre_update,
		post_update=post_update,
		pre_draw=pre_draw,
		post_draw=post_draw
	)

	app._mouse1_down.event(mouse1_down)
	app._mouse2_down.event(mouse2_down)

	app.start()

if __name__ == '__main__':
	run_2d_test()
