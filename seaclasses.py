import logging
from constants import *


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
        """
        Lay out ship on the board.
        Return false if placement is invalid

        :param ship: Ship
        :param x: int
        :param y: int
        :param horizontal: bool
        """

        # see if this runs off the board
        if horizontal:
            rightmost = x + ship.size - 1
            if rightmost > 9:
                logging.debug("Hit edge!")
                return False
        else:  # vertical
            bottommost = y + ship.size - 1
            if bottommost > 9:
                logging.debug("Hit edge!")
                return False

        # scan through planned ship footprint to see if anything is there
        if horizontal:
            for i in range(0, ship.size):
                # look at this cell, see if the ship flag is set
                checking_cell = self.get_cell(x + i, y)
                if checking_cell.has_ship():
                    logging.debug("Another ship is there!")
                    return False
        else:  # vertical
            for i in range(0, ship.size):
                checking_cell = self.get_cell(x, y + i)
                if checking_cell.has_ship():
                    logging.debug("Another ship is there!")
                    return False

        # We should be in the clear at this point. Update the data.

        for i in range(0, ship.size):
            if horizontal:
                cell = self.get_cell(x + i, y)
            else:
                cell = self.get_cell(x, y + i)
            cell.contains_ship_segment = True
            cell.contains_ship = ship

        # Update the Ship object
        ship.position = [x, y]
        ship.horizontal = horizontal

        return True

    def check_if_attack_hits(self, x, y):
        cell = self.get_cell(x, y)
        if cell.has_ship():
            logging.info("Hit!")
            ship = cell.get_ship_here()
            ship.damage(x, y)
            return True
        else:
            logging.info("Miss!")
            return False

    def check_if_ship_sinks(self, x, y):
        cell = self.get_cell(x, y)
        ship = cell.get_ship_here()

        logging.debug("Checking if {} sinks".format(ship.name))

        # loop over all segments of ship.
        # A single remaining segment means it's still in play
        all_destroyed = True
        ok_spaces = 0
        for spot in ship.damaged:
            if spot is False:
                ok_spaces += 1
                all_destroyed = False
        if all_destroyed:
            logging.info("Sank that ship")
            return True
        else:
            logging.debug("{} remaining spot".format(ok_spaces))
            return False

    def mark_hit(self, x, y):
        cell = self.get_cell(x, y)
        cell.has_hit_marker = True

    def mark_miss(self, x, y):
        cell = self.get_cell(x, y)
        cell.has_miss_marker = True


# object that stores information about a given ship instance
class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.horizontal = True  # vertical = False
        # position is where cell 0 of the ship sits
        self.position = [-1, -1]  # -1 = not on board
        self.destroyed = False
        # Initialize an array for keeping track of each spot that
        # can be damaged on a ship
        # offset 0 is upper left corner
        self.damaged = [False] * self.size  # collection of bools for each segment of the ship

    # TODO setters for grid position, orientation

    def damage(self, x, y):
        """
        figure out offset of selected coordinate
        from origin coordinate, toggle that bit in the list
        :param x:
        :param y:
        :return: True if succeeds, False if error
        """
        origin_x, origin_y = self.position
        if self.horizontal:
            if y != origin_y:
                logging.warning("Trying to damage coordinates"
                                " outside of ship ({}, {})".format(x, y))
                return False
            dam_offset = x - origin_x
        else:
            if x != origin_x:
                logging.warning("Trying to damage coordinates"
                                " outside of ship ({}, {})".format(x, y))
                return False
            dam_offset = y - origin_y

        if dam_offset < 0 or dam_offset >= self.size:
            logging.warning("Trying to damage coordinates"
                            " outside of ship ({}, {})".format(x, y))
            return False

        self.damaged[dam_offset] = True

        return True


# object that stores game state
class Game:
    def __init__(self):
        # Give player and cpu their standard chips
        self.player_ships = self.create_ships(SHIP_DICT)
        self.cpu_ships = self.create_ships(SHIP_DICT)

        # Let main program populate these
        self.player_grid = None
        self.cpu_grid = None

        self.winner_declared = False
        self.cpu_turn = False

    @staticmethod
    def create_ships(ship_dict):
        """
        Initializes the standard list of ships
        :param ship_dict:
        :return:
        :rtype: list of Ship
        """
        ships = []
        # loop through ship dictionary and create Ship objects
        for key, value in ship_dict.items():
            new_ship = Ship(key, value)
            ships.append(new_ship)
        return ships

    def place_player_ship(self, ship, x_coord, y_coord, horizontal):
        """
        Place a ship onto the player grid.
        Return false if there is a problem.
        :param ship:
        :param x_coord:
        :param y_coord:
        :param horizontal:
        :return:
        """
        return self.player_grid.place_ship(ship, x_coord, y_coord, horizontal)

    def place_cpu_ship(self, ship, x_coord, y_coord, horizontal):
        """
        Place a ship onto the cpu grid.
        Return false if there is a problem.
        :param ship:
        :param x_coord:
        :param y_coord:
        :param horizontal:
        :return:
        """
        return self.cpu_grid.place_ship(ship, x_coord, y_coord, horizontal)




