import logging
from constants import *

# define chr for display elements
BLANK = '.'
HIT_MARKER = '*'
MISS_MARKER = 'o'
SHIP = '#'


class CharGrid:

    def __init__(self, ship_grid, hidden=False):
        # use "nested comprehension" to set up 10x10 "array" of '.'
        self.array = [[BLANK for y in range(10)] for x in range(10)]
        self.hidden = hidden  # hides ship positions from player
        self.set_state(ship_grid)

    def set_hit(self, x, y):
        self.array[x][y] = HIT_MARKER

    def set_miss(self, x, y):
        self.array[x][y] = MISS_MARKER

    def set_ship(self, x, y):
        if self.hidden:
            self.array[x][y] = BLANK
        else:
            self.array[x][y] = SHIP

    def set_empty(self, x, y):
        self.array[x][y] = BLANK

    def get_chr(self, x, y):
        # Convert the contents of the cell to a Unicode decimal, then
        # cast it back to a chr, just in case
        return chr(ord((self.array[x][y])))

    def set_state(self, ship_grid):
        # check grid from upper left to lower right,
        # update chr in each array position
        for y in range(10):
            for x in range(10):
                cell = ship_grid.get_cell(x, y)
                if cell.contains_ship_segment():
                    if cell.has_hit_marker():
                        self.set_hit(x, y)
                    else:
                        self.set_ship(x, y)
                elif cell.has_miss_marker():
                    self.set_miss(x, y)
                else:
                    self.set_empty(x, y)

    def get_row_string(self, y):

        row_string = ""
        for x in range(10):
            row_string += self.get_chr(x, y)

        return row_string


def redraw_board(enemy_grid, player_grid, last_msg=None):
    """

    :param last_msg:
    :param enemy_grid:
    :param player_grid:
    :return:
    """
    # TODO implement nicer GUI

    cpu_char_grid = CharGrid(enemy_grid, hidden=True)
    player_char_grid = CharGrid(player_grid)

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
    for y in range(10):
        row_string = "  "  # left margin
        row_string += ROWS[y]  # add the index letter

        # step through each column in the row

        # enemy grid
        row_string += cpu_char_grid.get_row_string(y)

        row_string += ROWS[y]  # add an index letter
        row_string += "     "  # column gap
        row_string += ROWS[y]  # add an index letter

        # player grid
        row_string += player_char_grid.get_row_string(y)

        row_string += ROWS[y]  # add an index letter

        # ...and, now that we have built a row, display it
        assert len(row_string) == 31
        print(row_string)

    # print footer rows
    print(x_pos_row)
    print()
    print(last_msg)  # since we just cleared the screen
    print()


def clear_screen():
    """

    :return:
    """
    # https://www.quora.com/Is-there-a-Clear-screen-function-in-Python/answer/Hanno-Behrens-2
    # TODO use curses
    print("\033[H\033[J")

