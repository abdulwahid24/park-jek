import unittest
import os
from src.app.tests import TEST_CONFIG_FILE
from src.app.config.config import get_config


class TestParkingLotCommands(unittest.TestCase):
    def setUp(self):
        self.AppConfig = get_config(
            config_file=TEST_CONFIG_FILE, execution_level='test')

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
