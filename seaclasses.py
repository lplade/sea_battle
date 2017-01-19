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

        # TODO test for legit placement! not running off edge of board, not overlapping existing ship

        # Lay out ship on the board
        """

        :param ship: Ship
        :param x: int
        :param y: int
        :param horizontal: bool
        """
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
        # TODO finish this


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
        self.damaged = [False] * self.size  # collection of bools for each segment of the ship

    # TODO setters for grid position, orientation

    def damage(self, x, y):

        # figure out offset of selected coordinate from origin coordinate, toggle that bit in the list
        origin_x, origin_y = self.position
        if self.horizontal:
            dam_offset = x - origin_x
        else:
            dam_offset = y - origin_y
        self.damaged[dam_offset] = True
