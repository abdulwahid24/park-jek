import os
import argparse
from collections import namedtuple
from configparser import SafeConfigParser

from app.core import Singleton


DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.ini')
DEFAULT_EXECUTION_LEVEL = 'DEFAULT'


class ApplicationConfiguration(Singleton):
	'''
		ApplicationConfiguration class is designed to have a dynamical way of loading configuration from console and ini file.
	'''

	_argument_parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False)
	config = None

	def __init__(self, *args, **kwargs):
		self._initialize_arguments()
		self._load_config_file()

	def _initialize_arguments(self):
		self._argument_parser.add_argument(
			"--input_file", "-f",
			help="Provide an input file to execute a series of commands.",
			type=str)
		self._argument_parser.add_argument(
			"--config-file", "-c",
			help="Provide a custom config file to configure the application.",
			type=str,
			default=DEFAULT_CONFIG_FILE)
		self._argument_parser.add_argument(
			"--execution-level", "-e",
			help="Set the execution level while executing the application.",
			type=str,
			default=DEFAULT_EXECUTION_LEVEL)

	def _load_config_file(self):
		config_parser = SafeConfigParser()
		args = self._argument_parser.parse_args()
		config_parser.read([args.config_file])
		config_data = {k:v for k,v in config_parser[DEFAULT_EXECUTION_LEVEL].items()}
		if args.execution_level != DEFAULT_EXECUTION_LEVEL:
			config_data.update({k:v for k,v in config_parser[args.execution_level].items()})
		ConfigInstance = namedtuple(self.__class__.__name__, config_data.keys())
		self.config = ConfigInstance(**config_data)
