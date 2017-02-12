#!/usr/bin/python3

# Based on a popular board game
# TODO implement GUI (PyGame? Turtle graphics?)

from seaclasses import *
import logging
import game
import file_io

######################
# MAIN PROGRAM LOGIC #
######################


def main():
    # change to get more detail
    logging.basicConfig(level=logging.WARNING)

    print("SEA BATTLE")
    print()

    # initialize some stuff:

    gs = Game()  # game state

    gs.player_grid = game.player_place_ships(gs.player_ships)
    gs.cpu_grid = game.cpu_place_ships(gs.cpu_ships)

    # Game loop
    while gs.winner_declared is False:

        # Player turn loop
        if not gs.cpu_turn:
            game.run_human_turn(gs)
            game.player_io.anykey()
        # CPU turn loop
        else:
            game.run_cpu_turn(gs)
            game.player_io.anykey()

    # Endgame
    if gs.cpu_turn:
        game.player_io.msg("Sorry, you lost")
    else:
        game.player_io.msg("You are the winner")

    # Dump a copy of both boards when we're done
    file_io.dump_board(gs.cpu_grid, gs.player_grid, "dump.txt")


#######################
# program entry point #
#######################

# Fires main() loop when this file is executed
if __name__ == '__main__':
    main()
