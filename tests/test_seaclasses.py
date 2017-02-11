import unittest
import seaclasses
import constants


class GameTest(unittest.TestCase):

    def test_create_ships(self):

        ship_dict = {"dreadnaught": 6}

        ships = seaclasses.Game.create_ships(ship_dict)

        self.assertEqual(ships[0].name, "dreadnaught")
        self.assertEqual(ships[0].size, 6)


class ShipTest(unittest.TestCase):

    def test_damage(self):

        ship = seaclasses.Ship("dreadnaught", 6)
        ship.position = [0, 0]

        self.assertTrue(ship.damage(0, 0))
        self.assertEqual(ship.damaged,
                         [True, False, False, False, False, False])
        self.assertTrue(ship.damage(4, 0))
        self.assertEqual(ship.damaged,
                         [True, False, False, False, True, False])

        self.assertFalse(ship.damage(2, 3))
        self.assertFalse(ship.damage(-1, -1))
        self.assertFalse(ship.damage(30, 30))


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
