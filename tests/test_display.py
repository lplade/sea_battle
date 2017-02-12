import unittest
import seaclasses
import display


class DisplayTest(unittest.TestCase):
    
    def setUp(self):
        """Set up the tests"""
        print("DisplayTest:setUp_:begin")
        # put some ships on some grids,
        # use these for all display tests

        self.cpu_grid = seaclasses.ShipGrid()
        self.player_grid = seaclasses.ShipGrid()

        cpu_tugboat = seaclasses.Ship("tugboat", 2)
        cpu_yacht = seaclasses.Ship("yacht", 4)
        player_ferry = seaclasses.Ship("ferry", 3)
        player_barge = seaclasses.Ship("barge", 5)

        self.cpu_grid.place_ship(cpu_tugboat, 1, 1, True)
        self.cpu_grid.place_ship(cpu_yacht, 8, 1, False)
        self.player_grid.place_ship(player_ferry, 1, 1, True)
        self.player_grid.place_ship(player_barge, 8, 1, False)

        print("DisplayTest:setUp_:end")

    def tearDown(self):
        """Clean up after the test"""
        print("DisplayTest:tearDown_:begin")
        # do stuff
        print("DisplayTest:tearDown_:end")

    def test_redraw_board(self):
        """
        This just lets us preview the output.
        Doesn't do any assertions yet.
        :return:
        """
        display.redraw_board(self.cpu_grid, self.player_grid)

