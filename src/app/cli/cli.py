import sys
import os
import logging
from app import BASE_DIR
from app.core import Singleton
from app.cli.commands import ParkingLotCommand
from app.cli.exceptions import CommandNotFoundError
from app.config import AppConfig

CLI_BASE_PATH = os.path.join(BASE_DIR, os.path.dirname(__file__))


class CLIConsole(Singleton):

    std_input = ''

    def __init__(self, *args, **kwargs):
        if not os.path.exists(AppConfig.log_dir):
            os.mkdir(AppConfig.log_dir)
        logging.basicConfig(
            filename=os.path.join(AppConfig.log_dir, AppConfig.log_filename),
            filemode='w',
            format='%(asctime)s %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            level=eval(AppConfig.log_level))

    def __enter__(self, *args):
        with open(os.path.join(CLI_BASE_PATH, 'welcome.txt'),
                  'r') as welcome_message_file:
            print(welcome_message_file.read())
        return self

    def __exit__(self, *args, **kwargs):
        print("\nGood Bye")

    def run(self):
        while True:
            try:
                self.std_input = input("park-a-lot> ")
                if self.std_input:
                    self._process_command(*self.std_input.split())
            except (KeyboardInterrupt, EOFError):
                sys.exit()

    def _process_command(self, *args):
        try:
            command, arguments = args[0], args[1:]
            parking_lot_command = ParkingLotCommand()
            parking_lot_command.execute(command, *arguments)
        except Exception as e:
            logging.exception(e)
