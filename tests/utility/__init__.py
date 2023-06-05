
import tkinter as tk

from typing import Any

def clamp_v(value, minn, maxx):
	return max(min(value, maxx), minn)

def default_pass(self):
	pass

class VConnection:
	parent = None
	callback = None

	def call_callback(self, *args, **kwargs) -> None:
		self.callback(*args, **kwargs)

	def disconnect(self):
		if type(self.parent) == VEvent:
			self.parent._remove_connection()
		self.parent = None
	
	def __init__(self):
		pass

class VEvent:
	callbacks = None

	def _remove_connection(self, connection : VConnection):
		while self.callbacks.count(connection) != 0:
			self.callbacks.remove(connection)

	def fire(self, *args, **kwargs):
		pass

	def on_event(self, callback):
		pass

	def __init__(self):
		self.callbacks = []

class DrawApp(tk.Tk):
	WIDGET_SIZE = (800,800)
	pre_update = post_update = pre_draw = post_draw = default_pass
	mouse_x = mouse_y = 0

	mouse_entered = VEvent()
	mouse_left = VEvent()
	mouse1_down = VEvent()
	mouse2_down = VEvent()
	mouse_scroll_down = VEvent()

	def draw_line(self, x0, y0, x1, y1, **kwargs) -> None:
		x0 = clamp_v(x0, 0, self.WIDGET_SIZE[0])
		x1 = clamp_v(x1, 0, self.WIDGET_SIZE[0])
		y0 = clamp_v(y0, 0, self.WIDGET_SIZE[1])
		y1 = clamp_v(y1, 0, self.WIDGET_SIZE[1])
		self.canvas.create_line( (x0), (y0), (x1), (y1), **kwargs)

	def clear_screen(self):
		self.canvas.delete("all")
		self.canvas.create_rectangle(0, 0, self.WIDGET_SIZE[0], self.WIDGET_SIZE[1], fill="black")

	def get_mouse_xy(self):
		return self.mouse_x, self.mouse_y

	def set_pre_update(self, func):
		if func != None:
			self.pre_update = func
	def set_post_update(self, func):
		if func != None:
			self.post_update = func
	def set_pre_draw(self, func):
		if func != None:
			self.pre_draw = func
	def set_post_draw(self, func):
		if func != None:
			self.post_draw = func

	def set_update_methods(self, pre_update=None, post_update=None, pre_draw=None, post_draw=None) -> None:
		self.set_pre_update(pre_update)
		self.set_post_update(post_update)
		self.set_pre_draw(pre_draw)
		self.set_post_draw(post_draw)

	def update(self):
		if self.pre_update != None:
			self.pre_update(self)
		if self.post_update != None:
			self.post_update(self)
		if self.pre_draw != None:
			self.pre_draw(self)
		super().update()
		if self.post_draw != None:
			self.post_draw(self)

	def _mouse_entered(self, event):
		self.mouse_entered.fire(event.x, event.y)

	def _mouse_left(self, event):
		self.mouse_left.fire(event.x, event.y)

	def _mouse1_press(self, event):
		self.mouse1_down.fire(event.x, event.y)

	def _mouse2_press(self, event):
		self.mouse2_down.fire(event.x, event.y)

	def _mouse_scroll_press(self, event):
		self.mouse_scroll_down.fire(event.x, event.y)

	def _mouse_motion(self, event):
		self.mouse_x = event.x
		self.mouse_y = event.y

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.canvas = tk.Canvas(width=self.WIDGET_SIZE[0], height=self.WIDGET_SIZE[1])
		self.canvas.bind('<Motion>', self._mouse_motion)
		self.canvas.bind('<Button-1>', self._mouse1_press)
		self.canvas.bind('<Button-2>', self._mouse_scroll_press)
		self.canvas.bind('<Button-3>', self._mouse2_press)
		self.canvas.bind('<Enter>', self._mouse_entered)
		self.canvas.bind('<Leave>', self._mouse_left)
		self.canvas.pack(fill="both", expand=True)
		self.clear_screen()

def run_draw_widget( WIDGET_SIZE=(800,800) ) -> DrawApp:
	print("App is being started.")

	# create app with widget size
	DrawApp.WIDGET_SIZE = WIDGET_SIZE
	root = DrawApp("Draw Canvas")

	# exit widget update loop when closed
	window_alive = True
	def on_widget_close():
		nonlocal window_alive
		window_alive = False
		print("Canvas window has been closed.")
	root.protocol("WM_DELETE_WINDOW", on_widget_close)

	# widget update loop
	while window_alive:
		try:
			root.update()
		except KeyboardInterrupt:
			break

	# kill the widget
	print("App has been closed.")
	root.destroy()
