
import tkinter as tk

from utility.Event import VEvent

def clamp_v(value, minn, maxx):
	return max(min(value, maxx), minn)

def default_pass(self):
	pass

class DrawApp(tk.Tk):
	WIDGET_SIZE = (800,800)
	pre_update = post_update = pre_draw = post_draw = default_pass
	mouse_x = mouse_y = 0

	_mouse_entered = VEvent()
	_mouse_left = VEvent()
	_mouse1_down = VEvent()
	_mouse2_down = VEvent()
	_mouse_scroll_down = VEvent()

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

	def set_update_methods(self, pre_update=default_pass, post_update=default_pass, pre_draw=default_pass, post_draw=default_pass) -> None:
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

	def _mouse_motion(self, event):
		self.mouse_x = event.x
		self.mouse_y = event.y

	def start(self) -> None:
		# exit widget update loop when closed
		window_alive = True
		def on_widget_close():
			nonlocal window_alive
			window_alive = False
			print("Canvas window has been closed.")
		self.protocol("WM_DELETE_WINDOW", on_widget_close)

		# widget update loop
		while window_alive:
			try:
				self.update()
			except KeyboardInterrupt:
				break

		# kill the widget
		print("App has been closed.")
		self.destroy()

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.canvas = tk.Canvas(width=self.WIDGET_SIZE[0], height=self.WIDGET_SIZE[1])
		self.canvas.bind('<Motion>', self._mouse_motion)
		self.canvas.bind('<Button-1>', self._mouse1_down.fire)
		self.canvas.bind('<Button-2>', self._mouse_scroll_down.fire)
		self.canvas.bind('<Button-3>', self._mouse2_down.fire)
		self.canvas.bind('<Enter>', self._mouse_entered.fire)
		self.canvas.bind('<Leave>', self._mouse_left.fire)
		self.canvas.pack(fill="both", expand=True)
		self.clear_screen()

def create_draw_widget( WIDGET_SIZE=(800,800) ) -> DrawApp:
	print("App is being started.")

	# create app with widget size
	DrawApp.WIDGET_SIZE = WIDGET_SIZE
	root = DrawApp("Draw Canvas")

	# return the root
	return root
