import unittest
from unittest.mock import Mock, patch
import seaclasses
import constants
import player_io
import display
import __init__


class SeaBattleTest(unittest.TestCase):

    def setUp(self):
        self.gs = seaclasses.Game()


    def test_player_place_ships(self):
        input_list = [
            'j', '9', 'v', # this should error
            'a', '0', 'h',
            'b', '0', 'h',
            'c', '0', 'h',
            'd', '0', 'h',
            'a', '0', 'v', # this should error
            'e', '0', 'h',
        ]
        with patch("player_io.get_input",
                   side_effect=input_list):
            __init__.player_place_ships(self.gs.player_ships)