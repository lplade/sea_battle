# PROTIP: if displaying A1 coordinates, letter is Y coord, number is X!

import time
import logging

import player_io
import cpu_logic
import display
from seaclasses import *
from constants import *


#############################
# Player specific-methods   #
#############################

def player_place_ships(ship_list):
    """
    Interactively prompts player to place each ship in ship_list
    :type ship_list: list of Ship
    :rtype: ShipGrid
    """

    player_grid = ShipGrid()
    enemy_grid = ShipGrid()
    # we have to initialize a null grid for drawing purposes.
    # this gets discarded.

    message = "For each ship, specify the upper or leftmost coordinate."

    for ship in ship_list:
        while True:  # break on valid placement
            display.redraw_board(enemy_grid=enemy_grid,
                                 player_grid=player_grid,
                                 last_msg=message)

            x_coord, y_coord, horizontal = \
                player_io.interactive_get_placement_coord(ship)

            if player_grid.place_ship(ship, x_coord, y_coord, horizontal):
                message = "Ship placed."
                break
            else:
                message = "Invalid placement! Try again."

    # refresh one more time before returning
    display.redraw_board(enemy_grid=enemy_grid,
                         player_grid=player_grid,
                         last_msg=message)

    # return the populated grid
    return player_grid


def player_select_attack_coordinates():
    """
    Interactively prompts player to input attack coordinates.
    Right now, just wraps player_io.interactive_get_attack_coord()
    :rtype: int, int
    """
    return player_io.interactive_get_attack_coord()


def run_human_turn(gs):
    """
    Main logic for the human player's turn
    :param gs:
    :return:
    """

    message = None

    while True:
        display.redraw_board(enemy_grid=gs.cpu_grid,
                             player_grid=gs.player_grid,
                             last_msg=message)
        # updates will appear on tracking grid
        attack_x, attack_y = player_select_attack_coordinates()
        if gs.cpu_grid.check_if_attack_hits(attack_x, attack_y):
            message = "A hit!"
            gs.cpu_grid.mark_hit(attack_x, attack_y)
            if gs.cpu_grid.check_if_ship_sinks(attack_x, attack_y):
                sunk_ship = \
                    gs.cpu_grid.get_cell(attack_x, attack_y).get_ship_here()
                if sunk_ship.name[0].lower() in "aeiou":
                    message = "You sank an {}!".format(sunk_ship.name)
                else:
                    message = "You sank a {}!".format(sunk_ship.name)
            if not does_player_have_ships(gs.cpu_ships):
                gs.winner_declared = True
                return
        else:  # attack missed
            gs.cpu_grid.mark_miss(attack_x, attack_y)
            message = "You missed."
            display.redraw_board(gs.cpu_grid, gs.player_grid, message)
            gs.cpu_turn = True
            return


############
# Common to player and CPU
##############

def does_player_have_ships(ship_list):
    """
    Checks if there are any un-sunk ships left in ship_list.
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

def cpu_place_ships(ship_list):
    """
    AI to place CPU ship on board.
    Right now, completely random. No strategy.
    :type ship_list: list of Ship
    :rtype: ShipGrid
    """
    cpu_grid = ShipGrid()

    for ship in ship_list:
        while True:
            # exit when all conditions of a valid ship placement are fulfilled

            x_attempt, y_attempt, horizontal = \
                cpu_logic.random_placement_coord()

            logging.info("Trying to put ship size {} at {}, {}, {}"
                         .format(ship.size, x_attempt, y_attempt, horizontal))

            # Use ShipGrid.place_ship logic to do the heavy lifting here
            if cpu_grid.place_ship(ship, x_attempt, y_attempt, horizontal):
                player_io.msg("Enemy has deployed a ship...")
                break
            else:
                logging.debug("Invalid placement, re-trying...")

    return cpu_grid


def cpu_select_attack_coordinates(player_grid):
    """
    AI to select CPU attack coordinates.
    Right now, completely random. No strategy.
    :param player_grid: ShipGrid
    :rtype: int, int
    """
    x_attack, y_attack = cpu_logic.select_attack_coordinates(player_grid)

    logging.info("Attacking ({}, {})".format(x_attack, y_attack))

    return x_attack, y_attack


def run_cpu_turn(gs):
    """
    Main logic for computer player turn.
    :param gs:
    :return:
    """
    message = None
    while True:  # return when attack misses
        display.redraw_board(gs.cpu_grid, gs.player_grid, message)
        # updates will appear on player grid
        attack_x, attack_y = cpu_select_attack_coordinates(gs.player_grid)
        player_io.msg("Enemy is attacking " +
                      ROWS[attack_y] + str(attack_x) + "...")
        # small pause so play can see what is going on
        time.sleep(4)
        if gs.player_grid.check_if_attack_hits(attack_x, attack_y):
            player_io.msg("A hit!")
            gs.player_grid.mark_hit(attack_x, attack_y)
            if gs.player_grid.check_if_ship_sinks(attack_x, attack_y):
                sunk_ship = \
                    gs.cpu_grid.get_cell(attack_x, attack_y).get_ship_here()
                player_io.msg("Enemy sank your {}!".format(sunk_ship.name))
            if not does_player_have_ships(gs.player_ships):
                gs.winner_declared = True
                return
        else:  # attack missed
            player_io.msg("Enemy missed.")
            gs.player_grid.mark_miss(attack_x, attack_y)
            # redraw_board(cpu_grid, player_grid)
            gs.cpu_turn = False
            return  # end CPU turn

