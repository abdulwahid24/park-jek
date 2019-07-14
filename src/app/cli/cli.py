import sys
from app.core import Singleton


class CLIConsole(Singleton):

	std_input = ''

	def __init__(self, config, *args, **kwargs):
		self.config = config

	def __enter__(self, *args):
		print("Welcome")
		return self

	def __exit__(self, *args, **kwargs):
		print("Good Bye")

	def run(self):
		while True:
			self.std_input = input("park-a-lot> ")
			if self.std_input == 'exit':
				sys.exit()

