import sys
import re
import logging
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
            self._slot_number_for_registration_number,
            "help":
            self._help,
            "exit":
            self._exit
        }

    def execute(self, command, *args, **kwargs):
        try:
            if command not in self._commands:
                raise CommandNotFoundError(
                    "CommandNotFoundError:command '{0}' not found. Available options are : {1}"
                    .format(command, ', '.join(self._commands.keys())))
            return self._commands[command](*args, **kwargs)
        except CommandNotFoundError as e:
            return (
                "Command not found. Enter 'help' command to list available commands"
            )
        except TypeError as e:
            return (re.sub(r'_%s\(\)' % command, '%s command' % command,
                           str(e)))

    def _help(self):
        commands_string = """
_______________________
< Available commands >
_______________________
- {}
_______________________
"""
        return (commands_string.format('\n- '.join(self._commands.keys())))

    def _exit(self):
        sys.exit()

    def _create_parking_lot(self, slot_size):
        try:
            for _i in range(int(slot_size)):
                slot = Slot(**{'id': 0, 'is_empty': True})
                slot.save()
        except Exception as e:
            logging.exception(e)
        else:
            return ("Created a parking lot with {} slots".format(slot_size))

    def _status(self):
        try:
            parkings = Parking.objects().filter(leave_at='')
            status_message = "Slot No.\tRegistration No\t\tColour\n"
            for parking in parkings:
                status_message += "{slot_number}\t\t{registration_number}\t\t{color}\n".format(
                    slot_number=parking.slot.id,
                    registration_number=parking.vehicle.registration_number.
                    upper(),
                    color=parking.vehicle.color.title())
            return status_message
        except Exception as e:
            logging.exception(e)

    def _park(self, registration_number, color):
        try:
            parking = Parking.is_parking_exists(
                registration_number=registration_number)
            if parking:
                return ('Vehicle already parked at slot {}'.format(
                    parking.slot.id))
            vehicle = Vehicle(
                id=0,
                registration_number=registration_number.lower(),
                color=color.lower()).get_or_create()
            slot = Slot.get_empty_slot()
            if not slot:
                return ("Sorry, parking lot is full")

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
            logging.exception(e)
        else:
            return ("Allocated slot number: {}".format(slot.id))

    def _leave(self, slot_number):
        try:
            parking = Parking.objects().get(
                slot__id=int(slot_number), leave_at="")
            if not parking:
                return ("Slot number {} is already empty.".format(slot_number))
            parking = parking._asdict()
            parking['leave_at'] = datetime.now().timestamp()
            parking = Parking(**parking)
            parking.update()
            slot = Slot(**{'id': parking.slot.id, 'is_empty': True})
            slot.update()
        except Exception as e:
            logging.exception(e)
        else:
            return ("Slot number {} is free.".format(slot_number))

    def _registration_numbers_for_cars_with_colour(self, color):
        try:
            vehicles = Vehicle.objects().filter(color=color.lower())
            if not vehicles:
                return ("Not Found")
            return ("{}".format(", ".join([
                vehicle.registration_number.upper() for vehicle in vehicles
            ])))
        except Exception as e:
            logging.exception(e)

    def _slot_numbers_for_cars_with_colour(self, color):
        try:
            parkings = Parking.objects().filter(
                vehicle__color=color.lower(), leave_at='')
            if not parkings:
                return ("Not Found")
            return ("{}".format(", ".join(
                [str(parking.slot.id) for parking in parkings])))
        except Exception as e:
            logging.exception(e)

    def _slot_number_for_registration_number(self, registration_number):
        try:
            parking = Parking.objects().get(
                vehicle__registration_number=registration_number.lower(),
                leave_at='')
            if not parking:
                return ("No Found")
            return ("{}".format(parking.slot.id))
        except Exception as e:
            logging.exception(e)
