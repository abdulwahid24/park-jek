import unittest
from src.app.tests.test_parking_lot_commands import TestParkingLotCommands


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestParkingLotCommands())
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
