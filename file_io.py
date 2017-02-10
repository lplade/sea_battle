import logging

# list of row labels
ROWS = "ABCDEFGHIJ"


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