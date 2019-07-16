from datetime import datetime
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
                slot = Slot(**{'id': 0, 'is_empty': True})
                slot.save()
        except Exception as e:
            print(e)
        else:
            print("Created a parking lot with {} slots".format(slot_size))

    def _status(self):
        pass

    def _park(self, registration_number, color):
        try:
            parking = Parking.is_parking_exists(
                registration_number=registration_number)
            if parking:
                print('Vehicle already parked at slot {}'.format(
                    parking.slot.id))
                return
            vehicle = Vehicle(
                id=0, registration_number=registration_number,
                color=color).get_or_create()
            slot = Slot.get_empty_slot()
            if not slot:
                print("Parking FULL !!!")
                return

            # Update slot status
            slot = slot._asdict()
            slot['is_empty'] = False
            slot = Slot(**slot)
            slot.update()

            # add parking details
            parking = Parking(
                id=0,
                vehicle=vehicle,
                slot=slot,
                parked_at=datetime.now().timestamp(),
                leave_at='')
            parking.save()

        except Exception as e:
            print(e)
        else:
            print("Allocated slot number: {}".format(slot.id))

    def _leave(self, slot_number):
        try:
            parking = Parking.objects().get(
                slot__id=int(slot_number), leave_at="")
            if not parking:
                print("Slot number {} is already empty.".format(slot_number))
                return
            parking = parking._asdict()
            parking['leave_at'] = datetime.now().timestamp()
            parking = Parking(**parking)
            parking.update()

            slot = parking.slot._asdict()
            slot['is_empty'] = True
            slot = Slot(**slot)
            slot.update()
        except Exception as e:
            print(e)
        else:
            print("Slot number {} is free.".format(slot_number))

    def _registration_numbers_for_cars_with_colour(self):
        pass

    def _slot_numbers_for_cars_with_colour(self):
        pass

    def _slot_number_for_registration_number(self):
        pass
