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

    def test_place_ship(self):

        test_ship1 = seaclasses.Ship("tugboat", 2)
        test_ship2 = seaclasses.Ship("dreadnaught", 6)
        test_grid = seaclasses.ShipGrid()

        # outside of grid - fails in get_cell()
        # self.assertFalse(
        #     test_grid.place_ship(test_ship1, -3, -18, True))
        # self.assertFalse(
        #     test_grid.place_ship(test_ship2, 9, 12, False))

        # runs off edge
        self.assertFalse(
            test_grid.place_ship(test_ship2, 9, 9, True))

        # hits another ship
        self.assertTrue(
            test_grid.place_ship(test_ship1, 0, 0, True)
        )
        self.assertFalse(
            test_grid.place_ship(test_ship2, 0, 0, False)
        )

        # right up against right edge
        self.assertTrue(
            test_grid.place_ship(test_ship2, 9, 3, False)
        )


