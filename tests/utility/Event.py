
from _thread import start_new_thread

class VConnection:
	parentEvent = None
	callback = None

	def _call(self, *args, **kwargs) -> None:
		self.callback(*args, **kwargs)

	def disconnect(self):
		if type(self.parent) == VEvent:
			self.parent.__remove_connection()
		self.callback = None
		self.parent = None
	
	def __init__(self, parentEvent=None, callback=None):
		self.callback = callback
		self.parentEvent = parentEvent

class VEvent:
	callbacks = None
	_threaded = False

	def __remove_connection(self, connection : VConnection):
		while self.callbacks.count(connection) != 0:
			self.callbacks.remove(connection)

	def fire(self, *args, **kwargs):
		for connection in self.callbacks:
			try:
				if self._threaded:
					start_new_thread(connection._call, args, kwargs)
				else:
					connection._call(args, kwargs)
			except Exception as exception:
				print("Callback has reached an exception for VEvent. ", exception)

	def event(self, callback) -> VConnection:
		connection = VConnection(parentEvent=self, callback=callback)
		self.callbacks.append( connection )
		return connection

	def disconnect(self) -> None:
		for connection in self.callbacks:
			connection.callback = None
			connection.parent = None
		self.callbacks = []

	def __init__(self):
		self.callbacks = []
