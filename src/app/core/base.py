

class Singleton:

	def __new__(cls, *args, **kwargs):
		self = "__self__"
		if not hasattr(cls, self):
			instance = object.__new__(cls)
			setattr(cls, self, instance)
		return getattr(cls, self)
