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
                    check_if_ship_sinks(cpu_grid, attack_coordinates)
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
                    check_if_ship_sinks(player_grid, attack_coordinates)
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
    if __name__ == '__main__':
        for y in range(10):
            row_string = "  "      # left margin
            row_string += ROWS[y]  # add the index letter

            #step through each column in the row

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


def player_interactive_place_ships(ship_list):
    """

    :type ship_list: list of Ship
    :rtype: ShipGrid
    """

    # TODO GUI implementation

    for ship in ship_list:
        # TODO Take a single A-1 style entry?
        # loop until we get valid inputs for row and column
        while True:
            row_attack = input("Which row would you like to attack [A-J]? ")
            row_attack = row_attack.upper()
            if not valid_row_input(row_attack):
                print("Please enter a letter from A to J!")
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

    # TODO Take a single A-1 style entry?
    # loop until we get valid inputs for row and column
    while True:
        row_attack = input("Which row would you like to attack [A-J]? ")
        row_attack = row_attack.upper()
        if not valid_row_input(row_attack):
            print("Please enter a letter from A to J!")
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


def does_cpu_have_ships():
    pass


def does_player_have_ships():
    pass


def clear_screen():
    # https://www.quora.com/Is-there-a-Clear-screen-function-in-Python/answer/Hanno-Behrens-2
    # TODO use curses
    print("\033[H\033[J")


class GridCell:
    def __init__(self):
        self.contains_ship_segment = False  # boolean whether or not a ship is here
        self.contains_ship = None  # Ship object
        self.has_miss_marker = False  # like the white peg
        self.has_hit_marker = False  # like the red peg

    def set_miss_marker(self):
        self.has_miss_marker = True

    def set_hit_marker(self):
        self.has_hit_marker = True

    def has_ship(self):  # redundant when we could just get .contains_ship?
        """
        Returns true if there is a segment of a ship in this cell
        :rtype: bool
        """
        return self.contains_ship_segment

    def get_ship_here(self):
        """
        Returns the Ship object that crosses this cell
        :rtype: Ship
        """
        return self.contains_ship


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
        assert 0 <= x <= 9 and 0 <= y <= 9

        cell = self.array[x][y]
        return cell

    def place_ship(self, ship, x, y, horizontal):

        # TODO tests for legit placement: not running off edge of board, not overlapping existing ship

        # Lay out ship on the board
        for i in range(0, ship.size):
            if horizontal:
                cell = self.get_cell(x + i, y)
            else:
                cell = self.get_cell(x, y + i)
            cell.contains_ship_segment = True
            cell.contains_ship = ship

        # Update the Ship object
        ship.position = (x, y)
        ship.horizontal = horizontal

    def check_if_attack_hits(self, x, y):
        cell = self.get_cell(x, y)
        if cell.has_ship():
            # Hit!
            ship = cell.get_ship_here()

            return True
        else:
            # Miss!
            return False

    def check_if_ship_sinks(self, x, y):
        cell = self.get_cell(x, y)
        ship = cell.get_ship_here()


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
        # offset 0 is upper left corner
        self.damaged = [False] * self.size

    # TODO setters for grid position, orientation


# Fires main() loop when this file is executed
if __name__ == '__main__':
    main()
