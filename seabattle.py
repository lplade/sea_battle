#!/usr/bin/python3

# Based on a popular board game
# TODO implement GUI (PyGame? Turtle graphics?)

import random  # for AI 'decisions'
import time
import logging

import player_io
import cpu_logic
from seaclasses import *


#################
# 'constants'   #
#################

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


#############################
# Player specific-methods   #
#############################

def player_place_ships(ship_list):
    """

    :type ship_list: list of Ship
    :rtype: ShipGrid
    """

    player_grid = ShipGrid()
    enemy_grid = ShipGrid()
    # we have to initialize a null grid for drawing purposes.
    # this gets discarded.

    player_io.msg("For each ship, specify the upper or leftmost coordinate.")

    for ship in ship_list:
        while True:  # break on valid placement
            redraw_board(enemy_grid, player_grid)

            x_coord, y_coord, horizontal = \
                player_io.interactive_get_placement_coord(ship)

            if player_grid.place_ship(ship, x_coord, y_coord, horizontal):
                player_io.msg("Ship placed.")
                break
            else:
                player_io.msg("Invalid placement! Try again.")

    # return the populated grid
    return player_grid


def player_select_attack_coordinates():
    """

    :rtype: int, int
    """
    return player_io.interactive_get_attack_coord()


############
# Common to player and CPU
##############

def does_player_have_ships(ship_list):
    """

    :type ship_list: list of Ship
    :rtype: bool
    """
    # loop over all ships. if any are left, set flag.
    ships_left = False
    for ship in ship_list:
        if not ship.destroyed:
            ships_left = True

    if ships_left:
        return True
    else:
        return False


########################
# CPU functions        #
########################
# TODO re-write so these are all instance methods of a CPU class

def cpu_place_ships(ship_list):
    """

    :type ship_list: list of Ship
    :rtype: ShipGrid
    """
    cpu_grid = ShipGrid()

    for ship in ship_list:
        while True:  # exit when all conditions of a valid ship placement are fulfilled

            x_attempt, y_attempt, horizontal = cpu_logic.random_placement_coord(ship)

            logging.info("Trying to put ship size {} at {}, {}, {}".format(ship.size, x_attempt, y_attempt, horizontal))

            # Use ShipGrid.place_ship logic to do the heavy lifting here
            if cpu_grid.place_ship(ship, x_attempt, y_attempt, horizontal):
                player_io.msg("Enemy has deployed a ship...")
                break
            else:
                logging.debug("Invalid placement, re-trying...")

    return cpu_grid


def cpu_select_attack_coordinates(player_grid):
    """

    :param player_grid: ShipGrid
    :rtype: int, int
    """
    # right now, just fires at random
    # TODO use some basic strategy
    while True:  # break when a valid cell is targeted
        x_attempt = random.randint(0, 9)
        y_attempt = random.randint(0, 9)
        cell = player_grid.get_cell(x_attempt, y_attempt)
        if not cell.has_miss_marker and not cell.has_hit_marker:
            break  # otherwise, keep picking random cells

    logging.debug("attacking " + str(x_attempt) + ", " + str(y_attempt))
    return x_attempt, y_attempt


#####################
# Display functions #
#####################

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


def clear_screen():
    # https://www.quora.com/Is-there-a-Clear-screen-function-in-Python/answer/Hanno-Behrens-2
    # TODO use curses
    print("\033[H\033[J")


def dump_board(enemy_grid, player_grid, filename):

    # based on screen display
    # TODO isolate common code into own functions

    try:
        f = open(filename, 'w')
        try:

            game_title = "            SEA BATTLE            "
            title_row = "   ENEMY FLEET      YOUR FLEET "

            x_pos_row = "   0123456789       0123456789 "
            dummy_row = "__A..........A_____A..........A"

            # print header rows
            clear_screen()
            f.write("\n")
            f.write(game_title + "\n")
            f.write("\n")
            f.write(title_row + "\n")
            f.write("\n")
            f.write(x_pos_row + "\n")

            # new row
            for y in range(10):
                row_string = "  "  # left margin
                row_string += ROWS[y]  # add the index letter

                # step through each column in the row

                # enemy grid
                for x in range(10):
                    cell = enemy_grid.get_cell(x, y)
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
                row_string += "\n"  # add a linefeed

                # ...and, now that we have built a row, display it
                # assert len(row_string) == 31
                f.write(row_string)

            # print footer rows
            f.write(x_pos_row + "\n")
            print("\n")
        finally:
            f.close()

    except IOError:
        print("Trouble dumping grids to " + filename + "!")


def run_human_turn(gs):
    while True:
        redraw_board(gs.cpu_grid, gs.player_grid)
        # updates will appear on tracking grid
        attack_x, attack_y = player_select_attack_coordinates()
        if gs.cpu_grid.check_if_attack_hits(attack_x, attack_y):
            print("A hit!")
            gs.cpu_grid.mark_hit(attack_x, attack_y)
            gs.cpu_grid.check_if_ship_sinks(attack_x, attack_y),
            if not does_player_have_ships(gs.cpu_ships):
                gs.winner_declared = True
                return
        else:  # attack missed
            gs.cpu_grid.mark_miss(attack_x, attack_y)
            print("You missed.")
            redraw_board(gs.cpu_grid, gs.player_grid)
            gs.cpu_turn = True
            return


def run_cpu_turn(gs):
    while True:  # return when attack misses
        redraw_board(gs.cpu_grid,
                     gs.player_grid)  # updates will appear on player grid
        attack_x, attack_y = cpu_select_attack_coordinates(gs.player_grid)
        print("Enemy is attacking " + ROWS[attack_x] + str(attack_y) + "...")
        # small pause so play can see what is going on
        time.sleep(5)
        if gs.player_grid.check_if_attack_hits(attack_x, attack_y):
            print("A hit!")
            gs.player_grid.mark_hit(attack_x, attack_y)
            gs.player_grid.check_if_ship_sinks(attack_x, attack_y)
            if not does_player_have_ships(gs.player_ships):
                gs.winner_declared = True
                return
        else:  # attack missed
            print("Enemy missed.")
            gs.player_grid.mark_miss(attack_x, attack_y)
            # redraw_board(cpu_grid, player_grid)
            gs.cpu_turn = False
            return  # end CPU turn


######################
# MAIN PROGRAM LOGIC #
######################


def main():
    print("SEA BATTLE")
    print()

    # initialize some stuff:

    gs = Game()  # game state

    gs.player_grid = player_place_ships(gs.player_ships)
    gs.cpu_grid = cpu_place_ships(gs.cpu_ships)

    # Game loop
    while gs.winner_declared is False:

        # Player turn loop
        if not gs.cpu_turn:
            run_human_turn(gs)

        # CPU turn loop
        else:
            run_cpu_turn(gs)

    # Endgame
    if gs.cpu_turn:
        print("Sorry, you lost")
    else:
        print("You are the winner")

    # Dump a copy of both boards when we're done
    dump_board(gs.cpu_grid, gs.player_grid, "dump.txt")


#######################
# program entry point #
#######################

# Fires main() loop when this file is executed
if __name__ == '__main__':
    main()
