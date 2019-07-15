from app.core import Singleton
from app.storage.models import Vehicle, Slot, Parking
from app.cli.exceptions import CommandNotFoundError


class ParkingLotCommand(Singleton):
    def __init__(self):
        self._commands = {
            "create_parking_lot":
            self._create_parking_lot,
            "status":
            self._status,
            "park":
            self._park,
            "leave":
            self._leave,
            "registration_numbers_for_cars_with_colour":
            self._registration_numbers_for_cars_with_colour,
            "slot_numbers_for_cars_with_colour":
            self._slot_numbers_for_cars_with_colour,
            "slot_number_for_registration_number":
            self._slot_number_for_registration_number
        }

    def execute(self, command, *args, **kwargs):
        try:
            if command not in self._commands:
                raise CommandNotFoundError(
                    "CommandNotFoundError:command '{0}' not found. Available options are : {1}"
                    .format(command, ', '.join(self._commands.keys())))
            self._commands[command](*args, **kwargs)
        except CommandNotFoundError as e:
            print(e)
        except Exception as e:
            print(e)

    def _create_parking_lot(self, slot_size):
        try:
            for _i in range(int(slot_size)):
                slot = Slot()
                slot.save()
        except Exception as e:
            print(e)
		else:
			print("Created a parking lot with {} slots".format(slot_size))

    def _status(self):
        pass

    def _park(self, registration_number, color):
        pass

    def _leave(self):
        pass

    def _registration_numbers_for_cars_with_colour(self):
        pass

    def _slot_numbers_for_cars_with_colour(self):
        pass

    def _slot_number_for_registration_number(self):
        pass
