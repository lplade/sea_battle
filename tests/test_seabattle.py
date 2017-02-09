import unittest
import seabattle
from seaclasses import *

class TestSeaBattle(unittest.TestCase):

    def test_player_interactive_place_ships(self):

        # invalid placement condition to test:
        # - runs off the edge of the board
        # - overlaps another ship

        # test with two big ships
        ship_list = [
            Ship("aircraft carrier", 5),
            Ship("battleship", 4)
        ]

        test_coord_set = [
            # valid
            [["a", "0", "h"], ["c", "0", "h"]],
            # runs off the edge
            [["j", "0", "h"], ["c", "0", "h"]],
            # ship overlap
            [["b", "0", "h"], ["a", "1", "v"]]
        ]

        for coordinate_set in test_coord_set:



