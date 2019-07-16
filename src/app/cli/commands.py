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
        try:
            parkings = Parking.objects().filter(leave_at='')
            print("Slot No.\tRegistration No\t\tColour")
            for parking in parkings:
                print(
                    "{slot_number}\t\t{registration_number}\t\t{color}".format(
                        slot_number=parking.slot.id,
                        registration_number=parking.vehicle.
                        registration_number.upper(),
                        color=parking.vehicle.color.title()))
        except Exception as e:
            print(e)

    def _park(self, registration_number, color):
        try:
            parking = Parking.is_parking_exists(
                registration_number=registration_number)
            if parking:
                print('Vehicle already parked at slot {}'.format(
                    parking.slot.id))
                return
            vehicle = Vehicle(
                id=0,
                registration_number=registration_number.lower(),
                color=color.lower()).get_or_create()
            slot = Slot.get_empty_slot()
            if not slot:
                print("Sorry, parking lot is full")
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
            slot = Slot(**{'id': parking.slot.id, 'is_empty': True})
            slot.update()
        except Exception as e:
            print(e)
        else:
            print("Slot number {} is free.".format(slot_number))

    def _registration_numbers_for_cars_with_colour(self, color):
        try:
            vehicles = Vehicle.objects().filter(color=color.lower())
            if not vehicles:
                print("No vehicles found with color '{}'".format(color))
                return
            print("{}".format(", ".join([
                vehicle.registration_number.upper() for vehicle in vehicles
            ])))
        except Exception as e:
            print(e)

    def _slot_numbers_for_cars_with_colour(self, color):
        try:
            parkings = Parking.objects().filter(
                vehicle__color=color.lower(), leave_at='')
            if not parkings:
                print("Not Found")
                return
            print("{}".format(", ".join(
                [str(parking.slot.id) for parking in parkings])))
        except Exception as e:
            print(e)

    def _slot_number_for_registration_number(self, registration_number):
        try:
            parking = Parking.objects().get(
                vehicle__registration_number=registration_number.lower(),
                leave_at='')
            if not parking:
                print("No Found")
                return
            print("{}".format(parking.slot.id))
        except Exception as e:
            print(e)
