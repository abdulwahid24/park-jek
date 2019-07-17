import sys
import os
import logging
from src.app import BASE_DIR
from src.app.core import Singleton
from src.app.cli.commands import ParkingLotCommand
from src.app.cli.exceptions import CommandNotFoundError
from src.app.config import get_config

CLI_BASE_PATH = os.path.join(BASE_DIR, os.path.dirname(__file__))


class CLIConsole(Singleton):

    std_input = ''

    def __init__(self, *args, **kwargs):
        self.appConfig = get_config()
        LOG_DIR_PATH = os.path.join(BASE_DIR, self.appConfig.log_dir)
        if not os.path.exists(LOG_DIR_PATH):
            os.mkdir(LOG_DIR_PATH)

        logging.basicConfig(
            filename=os.path.join(LOG_DIR_PATH, self.appConfig.log_filename),
            filemode='w',
            format='%(asctime)s %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            level=eval(self.appConfig.log_level))

    def __enter__(self, *args):
        if self.appConfig.cli_graphics:
            with open(os.path.join(CLI_BASE_PATH, 'welcome.txt'),
                      'r') as welcome_message_file:
                print(welcome_message_file.read())
        return self

    def __exit__(self, *args, **kwargs):
        print("\nGood Bye")

    def run(self):
        while True:
            try:
                cursor_text = 'park-jek> ' if self.appConfig.cli_graphics else ''
                self.std_input = input(cursor_text)
                if self.std_input:
                    self._process_command(*self.std_input.split())
            except (KeyboardInterrupt, EOFError):
                sys.exit()

    def _process_command(self, *args):
        try:
            command, arguments = args[0], args[1:]
            parking_lot_command = ParkingLotCommand()
            print(parking_lot_command.execute(command, *arguments))
        except Exception as e:
            logging.exception(e)
