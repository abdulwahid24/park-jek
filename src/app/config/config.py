import os
import argparse
from collections import namedtuple
from configparser import SafeConfigParser

from app.core import Singleton

DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.ini')
DEFAULT_EXECUTION_LEVEL = 'default'


class ApplicationConfiguration(Singleton):
    '''
		ApplicationConfiguration class is designed to have a dynamical way of loading configuration from console and ini file.
	'''

    config = None

    def __init__(self, *args, **kwargs):
        if not self.config and not kwargs:
            self._initialize_arguments()
        self._load_config_file(**kwargs)

    def _initialize_arguments(self):
        argument_parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        argument_parser.add_argument(
            "--input_file",
            help="Provide an input file to execute a series of commands.",
            type=str,
            default='')
        argument_parser.add_argument(
            "--config-file",
            "-c",
            help="Provide a custom config file to configure the application.",
            type=str,
            default=DEFAULT_CONFIG_FILE)
        argument_parser.add_argument(
            "--execution-level",
            "-e",
            help="Set the execution level while executing the application.",
            type=str,
            default=DEFAULT_EXECUTION_LEVEL)

        self.args = argument_parser.parse_args()

    def _load_config_file(self, config_file=None, execution_level=None):
        config_file = config_file if config_file else self.args.config_file
        execution_level = execution_level if execution_level else self.args.execution_level
        config_parser = SafeConfigParser()
        config_parser.read([config_file])
        config_data = {
            k: v
            for k, v in config_parser[DEFAULT_EXECUTION_LEVEL].items()
        }
        config_data.update(
            {k: v
             for k, v in config_parser[execution_level].items()})
        ConfigInstance = namedtuple(self.__class__.__name__,
                                    config_data.keys())
        self.config = ConfigInstance(**config_data)


def get_config(*args, **kwargs):
    AppConfing = ApplicationConfiguration(*args, **kwargs).config
    return AppConfing
