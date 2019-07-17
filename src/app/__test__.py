import sys
import os
import shutil
from src.app import BASE_DIR
from src.app.cli.commands import ParkingLotCommand
from src.app.cli import CLIConsole
from src.app.config import get_config


def main():
    appConfig = get_config(execution_level='test')
    parking_commmand = ParkingLotCommand()

    # Reset DB with different test suites
    DB_DIR = os.path.join(BASE_DIR, appConfig.database_dir)
    if os.path.exists(DB_DIR):
        shutil.rmtree(DB_DIR)

    if appConfig.input_file:
        with open(appConfig.input_file, 'r') as input_file:
            input_command = input_file.readline()
            while input_command:
                print(parking_commmand.execute(*input_command.split()))
                input_command = input_file.readline()
    else:
        with CLIConsole() as cli:
            cli.run()


if __name__ == '__main__':
    main()
