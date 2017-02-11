
from seaclasses import *
import logging
from constants import *

def redraw_board(enemy_grid, player_grid):
    """

    :param enemy_grid:
    :param player_grid:
    :return:
    """
    # TODO implement nicer GUI

    # each grid is 10x10, with index labels on each side = 12 chars wide
    # 5 char gap in center, 2 char left margin
    game_title = "            SEA BATTLE            "
    title_row = "   ENEMY FLEET      YOUR FLEET "

    x_pos_row = "   0123456789       0123456789 "
    dummy_row = "__A..........A_____A..........A"

    # print header rows
    clear_screen()
    print()
    print(game_title)
    print()
    print(title_row)
    print()
    print(x_pos_row)

    # new row
    # if __name__ == '__main__':  # why was this line here? typo?
    for y in range(10):
        row_string = "  "  # left margin
        row_string += ROWS[y]  # add the index letter

        # step through each column in the row

        # enemy grid
        for x in range(10):
            cell = enemy_grid.get_cell(x, y)
            if cell.has_hit_marker:
                row_string += "*"
            elif cell.has_miss_marker:
                row_string += "o"
            else:
                row_string += "."

        row_string += ROWS[y]  # add an index letter
        row_string += "     "  # column gap
        row_string += ROWS[y]  # add an index letter

        # player grid
        for x in range(10):
            cell = player_grid.get_cell(x, y)
            if cell.contains_ship_segment:
                if cell.has_hit_marker:
                    row_string += "*"
                else:
                    row_string += "#"
            elif cell.has_miss_marker:
                row_string += "o"
            else:
                row_string += "."

        row_string += ROWS[y]  # add an index letter

        # ...and, now that we have built a row, display it
        assert len(row_string) == 31
        print(row_string)

    # print footer rows
    print(x_pos_row)
    print()


def clear_screen():
    """

    :return:
    """
    # https://www.quora.com/Is-there-a-Clear-screen-function-in-Python/answer/Hanno-Behrens-2
    # TODO use curses
    print("\033[H\033[J")

