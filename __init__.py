#!/usr/bin/python3

# Based on a popular board game
# TODO implement GUI (PyGame? Turtle graphics?)

import random  # for AI 'decisions'
import time
import logging


import player_io
import cpu_logic
import display
import file_io
from seaclasses import *
from constants import *


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
            display.redraw_board(enemy_grid=enemy_grid, player_grid=player_grid)

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

    :param player_grid: ShipGrid
    :rtype: int, int
    """
    x_attack, y_attack = cpu_logic.select_attack_coordinates(player_grid)

    logging.info("Attacking ({}, {})".format(x_attack, y_attack))

    return x_attack, y_attack


def run_human_turn(gs):
    while True:
        display.redraw_board(enemy_grid=gs.cpu_grid, player_grid=gs.player_grid)
        # updates will appear on tracking grid
        attack_x, attack_y = player_select_attack_coordinates()
        if gs.cpu_grid.check_if_attack_hits(attack_x, attack_y):
            print("A hit!")
            gs.cpu_grid.mark_hit(attack_x, attack_y)
            if gs.cpu_grid.check_if_ship_sinks(attack_x, attack_y):
                sunk_ship = \
                    gs.cpu_grid.get_cell(attack_x, attack_y).get_ship_here()
                print("You sank a {}!".format(sunk_ship.name))
            if not does_player_have_ships(gs.cpu_ships):
                gs.winner_declared = True
                return
        else:  # attack missed
            gs.cpu_grid.mark_miss(attack_x, attack_y)
            print("You missed.")
            display.redraw_board(gs.cpu_grid, gs.player_grid)
            gs.cpu_turn = True
            return


def run_cpu_turn(gs):
    while True:  # return when attack misses
        display.redraw_board(gs.cpu_grid, gs.player_grid)
        # updates will appear on player grid
        attack_x, attack_y = cpu_select_attack_coordinates(gs.player_grid)
        print("Enemy is attacking " + ROWS[attack_x] + str(attack_y) + "...")
        # small pause so play can see what is going on
        time.sleep(4)
        if gs.player_grid.check_if_attack_hits(attack_x, attack_y):
            print("A hit!")
            gs.player_grid.mark_hit(attack_x, attack_y)
            if gs.player_grid.check_if_ship_sinks(attack_x, attack_y):
                sunk_ship = \
                    gs.cpu_grid.get_cell(attack_x, attack_y).get_ship_here()
                print("Enemy sank your {}!".format(sunk_ship.name))
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
    logging.basicConfig(level=logging.WARNING)
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
            player_io.anykey()
        # CPU turn loop
        else:
            run_cpu_turn(gs)
            player_io.anykey()

    # Endgame
    if gs.cpu_turn:
        print("Sorry, you lost")
    else:
        print("You are the winner")

    # Dump a copy of both boards when we're done
    file_io.dump_board(gs.cpu_grid, gs.player_grid, "dump.txt")


#######################
# program entry point #
#######################

# Fires main() loop when this file is executed
if __name__ == '__main__':
    main()
