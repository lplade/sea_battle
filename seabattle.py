#!/usr/bin/python3

# Based on a popular board game
# TODO implement GUI (PyGame? Turtle graphics?)

# We'll use this a bunch
# name_of_ship: size_of_ship
SHIP_DICT = {
    'aircraft carrier': 5,
    'battleship': 4,
    'cruiser': 3,
    'submarine': 3,
    'destroyer': 2
}

# list of row labels
ROWS = "ABCDEFGHIJ"


# MAIN PROGRAM LOGIC #
def main():
    print("SEA BATTLE")
    print()

    # initialize some stuff:

    # give both the player and the CPU the starting ships
    player_ships = create_standard_ships()
    cpu_ships = create_standard_ships()

    player_grid = player_interactive_place_ships(player_ships)
    cpu_grid = cpu_place_ships(cpu_ships)

    # attack_coordinates = (-1, -1)

    winner_declared = False
    cpu_turn = False

    # Game loop
    while winner_declared is False:
        # Player turn loop
        if not cpu_turn:
            while True:  # break when attack misses, otherwise keep playing
                redraw_board(cpu_grid, player_grid)  # updates will appear on tracking grid
                attack_coordinates = player_select_attack_coordinates()
                if check_if_attack_hits(cpu_grid, attack_coordinates):
                    check_if_ship_sinks(cpu_grid)
                    if not does_cpu_have_ships():
                        winner_declared = True
                        break
                else:  # attack missed
                    redraw_board(cpu_grid, player_grid)
                    cpu_turn = True
                    break  # end player turn

        # CPU turn loop
        else:
            while True:  # break when attack misses
                redraw_board(cpu_grid, player_grid)  # updates will appear on player grid
                attack_coordinates = cpu_select_attack_coordinates()
                if check_if_attack_hits(player_grid, attack_coordinates):
                    check_if_ship_sinks(player_grid)
                    if not does_player_have_ships():
                        winner_declared = True
                        break
                else:  # attack missed
                    redraw_board(cpu_grid, player_grid)
                    cpu_turn = False
                    break  # end CPU turn

    # TODO endgame logic


def create_standard_ships():
    """
    Initializes the standard list of ships
    :rtype: list of Ship
    """
    ships = []
    # loop through ship dictionary and create Ship objects
    for key, value in SHIP_DICT.items():
        new_ship = Ship(key, value)
        ships.append(new_ship)
    return ships


def redraw_board(enemy_grid, player_grid):
    """
    This refreshes the picture of the board.
    :type player_grid: ShipGrid
    :type enemy_grid: ShipGrid
    """
    # TODO implement nicer GUI

    # each grid is 10x10, with index labels on each side = 12 chars wide
    # 5 char gap in center, 2 char left margin
    dummy_row = "__A..........A_____A..........A"
    title_row = "   ENEMY FLEET      YOUR FLEET "
    x_pos_row = "   0123456789       0123456789 "

    pass


def player_interactive_place_ships(ship_list):
    """

    :type ship_list: list of Ship
    :rtype: ShipGrid
    """
    pass


def cpu_place_ships(ship_list):
    # TODO write this
    """

    :type ship_list: list of Ship
    :rtype: ShipGrid
    """
    pass


def player_select_attack_coordinates():
    """

    :rtype: int, int
    """
    # TODO GUI implementation

    # TODO Take a single A1 style entry?
    # loop until we get valid inputs for row and column
    while True:
        row_attack = input("Which row would you like to attack [A-I]? ")
        row_attack = row_attack.upper()
        if not valid_row_input(row_attack):
            print("Please enter a letter from A to I!")
        else:
            break
    while True:
        col_attack = input("Which column would you like to attack [0-9]? ")
        if not valid_column_input(col_attack):
            print("Please enter a digit from 0 to 9!")
        else:
            break
    x_coord = col_attack
    y_coord = row_letter_to_y_coord_int(row_attack)

    return x_coord, y_coord


def valid_row_input(row):
    """
    Tests if string is single character from A to I
    :type row: str
    :rtype: bool
    """
    if len(row) == 1 and row in ROWS:
        return True
    else:
        return False


def valid_column_input(col):
    """
    Tests if entered digit is within range
    :type col: int
    :rtype: bool
    """
    # TODO handle type mismatch errors
    if 0 <= col <= 9:
        return True
    else:
        return False


def row_letter_to_y_coord_int(row_letter):
    """
    Translates a letter Y position into a numeric one
    :type row_letter: str
    :rtype: int
    """
    # set up a dictionary mapping letters to numbers
    # http://stackoverflow.com/a/14902938/7087237
    row_dict = dict(zip(ROWS, range(0, len(ROWS))))

    y_coord = row_dict[row_letter]
    assert 0 <= y_coord <= 9
    return y_coord


def cpu_select_attack_coordinates():
    """

    :rtype: int, int
    """
    pass


def check_if_attack_hits(grid, coordinates):
    pass


def check_if_ship_sinks(grid):
    pass


def does_cpu_have_ships():
    pass


def does_player_have_ships():
    pass


class GridCell:
    def __init__(self):
        self.has_miss_marker = False
        self.has_hit_marker = False

    def set_miss_marker(self):
        self.has_miss_marker = True

    def set_hit_marker(self):
        self.has_hit_marker = True


class ShipGrid:
    def __init__(self):
        # use "nested comprehension" to set up 10x10 "array" of GridCells
        self.array = [[GridCell() for y in range(10)] for x in range(10)]

    def get_cell(self, x, y):
        """
        This returns a GridCell object at a given x,y coordinate
        :param x: int
        :param y: int
        :rtype: GridCell
        """
        assert 0 <= x < 10 and 0 <= y < 10

        cell = self.array[x][y]
        return cell


# object that stores information about a given ship instance
class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.horizontal = True  # vertical = False
        # position is where cell 0 of the ship sits
        self.position = (-1, -1)  # -1 = not on board
        self.destroyed = False
        # Initialize an array for keeping track of each spot that
        # can be damaged on a ship
        self.damaged = [False] * self.size

    # TODO setters for grid position, orientation


# Fires main() loop when this file is executed
if __name__ == '__main__':
    main()
