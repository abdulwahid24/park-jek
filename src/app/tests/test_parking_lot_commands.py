import unittest
import os
from app.tests import TEST_CONFIG_FILE
from app.config.config import get_config
from app.cli.commands import ParkingLotCommand


class TestParkingLotCommands(unittest.TestCase):
    def setUp(self):
        self.AppConfig = get_config(
            config_file=TEST_CONFIG_FILE, execution_level='test')
        self.parking_lot_command = ParkingLotCommand()

    def test_create_parking_lot(self):
        expected_result = "Created a parking lot with 2 slots"
        actual_result = self.parking_lot_command.execute(
            'create_parking_lot', 2)
        self.assertEqual(expected_result, actual_result)
