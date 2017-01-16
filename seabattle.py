#!/usr/bin/python3

# Based on a popular board game
# TODO implement GUI (PyGame? Turtle graphics?)

# We'll use this a bunch
# name_of_ship: size_of_ship
SHIP_DICT = {
    'carrier': 5,
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

    attack_coordinates = (-1, -1)

    winner_declared = False
    cpu_turn = False

    # Game loop
    while winner_declared is False:
        # Player turn loop
        if not cpu_turn:
            while True:  # break when attack misses, otherwise keep playing
                redraw_board()  # updates will appear on tracking grid
                attack_coordinates = player_select_attack_coordinates()
                if check_if_attack_hits(cpu_grid, attack_coordinates):
                    check_if_ship_sinks(cpu_grid)
                    if not does_cpu_have_ships():
                        winner_declared = True
                        break
                else:  # attack missed
                    redraw_board()
                    cpu_turn = True
                    break  # end player turn

        # CPU turn loop
        else:
            while True:  # break when attack misses
                redraw_board()  # updates will appear on player grid
                attack_coordinates = cpu_select_attack_coordinates()
                if check_if_attack_hits(player_grid, attack_coordinates):
                    check_if_ship_sinks(player_grid)
                    if not does_player_have_ships():
                        winner_declared = True
                        break
                else:  # attack missed
                    redraw_board()
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

def redraw_board():
    """
    This refreshes the picture of the board.
    """
    #TODO implement nicer GUI

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
    pass

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

class ShipGrid:
    def __init__(self):
        pass


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
