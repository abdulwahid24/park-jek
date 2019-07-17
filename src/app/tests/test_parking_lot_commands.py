import unittest
import os
import shutil
from app.tests import TEST_DIR, TEST_CONFIG_FILE
from app.config.config import get_config
from app.cli.commands import ParkingLotCommand


class TestParkingLotCommands(unittest.TestCase):
    def setUp(self):
        self.AppConfig = get_config(
            config_file=TEST_CONFIG_FILE, execution_level='test')
        self.parking_lot_command = ParkingLotCommand()

    # def tearDown(self):
    #     shutil.rmtree(os.path.join(TEST_DIR, 'db'))

    def test_01_create_parking_lot(self):
        expected_result = "Created a parking lot with 1 slots"
        actual_result = self.parking_lot_command.execute(
            'create_parking_lot', 1)
        self.assertEqual(expected_result, actual_result)

    def test_02_status(self):
        expected_result = 'Slot No.\tRegistration No\t\tColour\n'
        actual_result = self.parking_lot_command.execute('status')
        self.assertIn(expected_result, actual_result)

    def test_03_park(self):
        expected_result = "Allocated slot number:"
        actual_result = self.parking_lot_command.execute(
            'park', 'mh-14-az-6658', 'white')
        self.assertIn(expected_result, actual_result)

    def test_04_slot_numbers_for_cars_with_colour(self):
        expected_result = "1"
        actual_result = self.parking_lot_command.execute(
            'slot_numbers_for_cars_with_colour', 'white')
        self.assertIn(expected_result, actual_result)

    def test_05_registration_numbers_for_cars_with_colour(self):
        expected_result = "MH-14-AZ-6658"
        actual_result = self.parking_lot_command.execute(
            'registration_numbers_for_cars_with_colour', 'white')
        self.assertIn(expected_result, actual_result)

    def test_06_slot_number_for_registration_number(self):
        expected_result = "1"
        actual_result = self.parking_lot_command.execute(
            'slot_number_for_registration_number', 'mh-14-az-6658')
        self.assertIn(expected_result, actual_result)
