import os
import argparse
from collections import namedtuple
from configparser import SafeConfigParser

from src.app.core import Singleton

DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.ini')
DEFAULT_EXECUTION_LEVEL = 'default'


class ApplicationConfiguration(Singleton):
    '''
		ApplicationConfiguration class is designed to have a dynamical way of loading configuration from console and ini file.
	'''

    config = None

    def __init__(self, *args, **kwargs):
        if not self.config:
            if not kwargs:
                sys_args = self._initialize_arguments()
                kwargs.update(sys_args._get_kwargs())
            self._load_config_file(**kwargs)

    def _initialize_arguments(self):
        argument_parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        argument_parser.add_argument(
            "input_file",
            help="Provide an input file to execute list of commands.",
            nargs='?',
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

        return argument_parser.parse_args()

    def _load_config_file(self, **kwargs):
        config_parser = SafeConfigParser()
        config_parser.read([kwargs['config_file']])
        config_data = {
            k: v
            for k, v in config_parser[DEFAULT_EXECUTION_LEVEL].items()
        }
        config_data.update({
            k: v
            for k, v in config_parser[kwargs['execution_level']].items()
        })
        config_data.update(kwargs)
        ConfigInstance = namedtuple(self.__class__.__name__,
                                    config_data.keys())
        self.config = ConfigInstance(**config_data)


def get_config(*args, **kwargs):
    AppConfing = ApplicationConfiguration(*args, **kwargs).config
    return AppConfing
