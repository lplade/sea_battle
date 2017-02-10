# list of row labels
ROWS = "ABCDEFGHIJ"


def msg(string):
    print(string)


def interactive_get_placement_coord(ship):
    """
    Prompts a player to input a row, column, and horiz/vert
    Return integers x, y and bool for horizontal
    :param ship:
    :return:
    """
    # loop until we get valid entry
    while True:
        place_row = input(
            "Specify starting row for " + ship.name + " (length: " + str(
                ship.size) + ") [A-J]: ")
        place_row = place_row.upper()
        if not valid_row_input(place_row):
            print("Please enter a letter from A to J!")
        else:
            break
    while True:
        place_col = input(
            "Specify starting column for " + ship.name + " (length: " + str(
                ship.size) + ") [0-9]: ")
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

    return x_coord, y_coord, horizontal


def interactive_get_attack_coord():
    """
    Prompts player to input row and column
    Returns integers for x and y
    :return:
    """
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


# HELPER FUNCTIONS #

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


def anykey():
    input("- Press any key to continue. -")