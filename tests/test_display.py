import unittest
import seaclasses


class DisplayTest(unittest.TestCase):
    
    def setUp(self):
        """Set up the tests"""
        print("DisplayTest:setUp_:begin")
        # put some ships on some grids,
        # use these for all display tests

        cpu_grid = seaclasses.ShipGrid()
        player_grid = seaclasses.ShipGrid()

        cpu_tugboat = {"tugboat", 2}
        cpu_yacht = {"yacht", 4}
        player_ferry = {"ferry", 3}
        player_barge = {"barge", 5}

        cpu_grid.place_ship(cpu_tugboat, 1, 1, True)
        cpu_grid.place_ship(cpu_yacht, 8, 1, False)
        player_grid.place_ship(player_ferry, 1, 1, True)
        player_grid.place_ship(player_barge, 8, 1, False)

        print("DisplayTest:setUp_:end")

    def tearDown(self):
        """Clean up after the test"""
        print("DisplayTest:tearDown_:begin")
        # do stuff
        print("DisplayTest:tearDown_:end")

    def test_redraw_board(self):

