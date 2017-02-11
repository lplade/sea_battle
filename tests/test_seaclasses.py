import unittest
import seaclasses
import constants

class GameTest(unittest.TestCase):

    def test_create_standard_ships(self):

        ships = seaclasses.Game.create_standard_ships()

        assert ships


class ShipGridTest(unittest.TestCase):

    def setUp(self):
        """Set up the tests"""
        print("ShipGridTest:setUp_:begin")
        # do stuff
        print("ShipGridTest:setUp_:end")

    def tearDown(self):
        """Clean up after the test"""
        print("ShipGridTest:tearDown_:begin")
        # do stuff
        print("ShipGridTest:tearDown_:end")
