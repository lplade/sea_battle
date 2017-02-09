import logging
import random


def random_placement_coord(ship):

    x_coord = random.randint(0, 9)
    y_coord = random.randint(0, 9)

    # http://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python
    horizontal = random.choice([True, False])

    logging.debug("Generated ({}, {}, {})".format(x_coord, y_coord, horizontal))

    return x_coord, y_coord, horizontal
