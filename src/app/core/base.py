

class Singleton:
	__instance = None

	def __new__(cls, *args, **kwargs):
		if Singleton.__instance is None:
			Singleton.__instance = object.__new__(cls)
		return Singleton.__instance
