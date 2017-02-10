import logging
import random


def random_placement_coord():

    x_coord = random.randint(0, 9)
    y_coord = random.randint(0, 9)

    # http://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python
    horizontal = random.choice([True, False])

    logging.debug("Generated ({}, {}, {})".format(x_coord, y_coord, horizontal))

    return x_coord, y_coord, horizontal


def select_attack_coordinates(player_grid):
    # right now, just fires at random
    # TODO use some basic strategy
    while True:  # break when a valid cell is targeted
        x_attempt = random.randint(0, 9)
        y_attempt = random.randint(0, 9)
        cell = player_grid.get_cell(x_attempt, y_attempt)
        logging.debug("Checking ({}, {}) for valid attack"
                      .format(x_attempt, y_attempt))
        if not cell.has_miss_marker and not cell.has_hit_marker:
            break   # otherwise, keep picking random cells

    return x_attempt, y_attempt
