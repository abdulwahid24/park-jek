import sys
import os
import shutil
from src.app import BASE_DIR
from src.app.cli.commands import ParkingLotCommand
from src.app.config import get_config
from src.app.cli import CLIConsole


def main():
    appConfig = get_config()
    parking_commmand = ParkingLotCommand()

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
