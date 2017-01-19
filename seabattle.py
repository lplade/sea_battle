#!/usr/bin/python3

# Based on a popular board game
# TODO implement GUI (PyGame? Turtle graphics?)

import random  # for AI 'decisions'

from seaclasses import *

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


# TODO stick this in a general display-related class?
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
    # if __name__ == '__main__':  # why was this line here? typo?
    for y in range(10):
        row_string = "  "      # left margin
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


def player_interactive_place_ships(ship_list):
    """

    :type ship_list: list of Ship
    :rtype: ShipGrid
    """

    player_grid = ShipGrid()
    enemy_grid = ShipGrid()  # we have to initialize a null grid for drawing purposes. this gets discarded.

    # TODO GUI implementation

    print("For each ship, specify the upper or leftmost coordinate.")

    for ship in ship_list:

        redraw_board(enemy_grid, player_grid)

        # TODO Take a single A-1 style entry?
        # loop until we get valid inputs for row and column
        while True:
            place_row = input("Specify starting row for " + ship.name + " (length: " + str(ship.size) + ") [A-J]: ")
            place_row = place_row.upper()
            if not valid_row_input(place_row):
                print("Please enter a letter from A to J!")
            else:
                break
        while True:
            place_col = input("Specify starting column for " + ship.name + " (length: " + str(ship.size) + ") [0-9]: ")
            if not valid_column_input(place_col):
                print("Please enter a digit from 0 to 9!")
            else:
                break
        while True:
            hor_vert = input("Should ship run Horizontally, or Vertically? [H|V]? ")
            hor_vert = hor_vert.upper()
            if hor_vert == "H":
                horizontal = True
                break
            elif hor_vert == "V":
                horizontal = False
                break
            else:
                print("Please enter H or V!")

        x_coord = int(place_col)
        y_coord = int(row_letter_to_y_coord_int(place_row))

        # print("DEBUG: putting ship size " + str(ship.size) + " at " + str(x_coord) + ", " + str(y_coord))

        player_grid.place_ship(ship, x_coord, y_coord, horizontal)

    # return the populated grid
    return player_grid


def cpu_place_ships(ship_list):
    """

    :type ship_list: list of Ship
    :rtype: ShipGrid
    """

    cpu_grid = ShipGrid()

    # TODO pull this testing stuff into a separate function, then include in player version

    for ship in ship_list:
        while True:  # exit when all conditions of a valid ship placement are fulfilled
            x_attempt = random.randint(0, 9)
            y_attempt = random.randint(0, 9)

            # http://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python
            horizontal = random.choice([True, False])

            # print("DEBUG: trying to put ship size " + str(ship.size) + " at " + str(x_attempt) + ", " + str(y_attempt))

            # see if this runs off the board
            if horizontal:
                rightmost = x_attempt + ship.size - 1
                if rightmost > 9:
                    # print("DEBUG: hit edge!")
                    continue  # failed, restart while loop
            else:  # vertical
                bottommost = y_attempt + ship.size - 1
                if bottommost > 9:
                    # print("DEBUG: hit edge!")
                    continue  # failed, restart while loop

            # scan through planned ship footprint to see if anything is there
            if horizontal:
                for i in range(0, ship.size):
                    # look at this cell, see if the ship flag is set
                    checking_cell = cpu_grid.get_cell(x_attempt + i, y_attempt)
                    if checking_cell.has_ship():
                        # print("DEBUG: another ship is there!")
                        continue  # something in the way, start over
            else:  # vertical
                for i in range(0, ship.size):
                    checking_cell = cpu_grid.get_cell(x_attempt, y_attempt + i)
                    if checking_cell.has_ship():
                        # print("DEBUG: another ship is there!")
                        continue

            cpu_grid.place_ship(ship, x_attempt, y_attempt, horizontal)

            print("Enemy has deployed a ship...")
            break

    return cpu_grid


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
    x_coord = int(col_attack)
    y_coord = int(row_letter_to_y_coord_int(row_attack))

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
    if 0 <= int(col) <= 9:
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


######################
# MAIN PROGRAM LOGIC #
######################


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
                attack_x, attack_y = player_select_attack_coordinates()
                if cpu_grid.check_if_attack_hits(attack_x, attack_y):
                    cpu_grid.check_if_ship_sinks(attack_x, attack_y),
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
                attack_x, attack_y = cpu_select_attack_coordinates()
                if player_grid.check_if_attack_hits(attack_x, attack_y):
                    player_grid.check_if_ship_sinks(attack_x, attack_y)
                    if not does_player_have_ships():
                        winner_declared = True
                        break
                else:  # attack missed
                    redraw_board(cpu_grid, player_grid)
                    cpu_turn = False
                    break  # end CPU turn

    # TODO endgame logic

# Fires main() loop when this file is executed
if __name__ == '__main__':
    main()
