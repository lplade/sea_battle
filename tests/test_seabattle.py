import unittest
from unittest.mock import Mock, patch
import seaclasses
import game
import constants
import player_io
import display
import __init__


def mock_redraw(enemy_grid, player_grid, last_msg=None):
    """
    Reduced to only display value of "message" string
    :param enemy_grid:
    :param player_grid:
    :param last_msg:
    :return:
    """
    if last_msg:
        player_io.msg(last_msg)


class SeaBattleTest(unittest.TestCase):
    def setUp(self):
        self.gs = seaclasses.Game()

    @patch("display.redraw_board", mock_redraw)
    @patch("player_io.msg")
    def test_player_place_ships(self, mock_msg):
        print("Testing player place ships")
        input_list = [
            'j', '9', 'v',  # this should error
            'a', '0', 'h',
            'b', '0', 'h',
            'c', '0', 'h',
            'd', '0', 'h',
            'a', '0', 'v',  # this should error
            'e', '0', 'h',
        ]

        with patch("player_io.get_input",
                   side_effect=input_list):
            game.player_place_ships(self.gs.player_ships)
            # need to do one more "redraw"
            display.redraw_board(self.gs.cpu_grid, self.gs.player_grid)

            # Get the args that were sent to player_io.msg()
            msg_calls = mock_msg.call_args_list

            # Here is the output we expect for the above keystrokes
            expected_out_strings = [
                "For each ship, specify the upper or leftmost coordinate.",
                "Invalid placement! Try again.",
                "Ship placed.",
                "Ship placed.",
                "Ship placed.",
                "Ship placed.",
                "Invalid placement! Try again.",
                "Ship placed."
            ]

            # loop over these
            for i in range(len(expected_out_strings)):
                # note the second parameter must be a 1-tuple
                self.assertEqual(msg_calls[i][0], (expected_out_strings[i],))

            print("Test end")

    # def test_cpu_place_ships(self):
    #     coord_list = [
    #         [9, 9, False],  # this should error
    #         [0, 0, True],
    #         [0, 1, True],
    #         [0, 2, True],
    #         [0, 3, True],
    #         [0, 0, False],
    #         [0, 4, True]  # this should error
    #     ]
    #
    #     with patch("cpu_logic.random_placement_coord",
    #                side_effect=coord_list):
    #         game.cpu_place_ships(self.gs.cpu_ships)
