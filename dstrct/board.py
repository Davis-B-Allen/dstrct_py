from tile import Tile
from game_settings import Game_Settings
from random import shuffle
from math import ceil


class Board:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.tilegrid = []
        self.played_tiles = []
        self.unplayed_tiles = []
        self.districts = []
        self.vertical_borders = []
        self.horizontal_borders = []
        print("Setting up board...\n")
        self.set_up_board(self.tilegrid)

    def set_up_board(self, tilegrid):
        # Create random distribution of tiles with same number of each type of voter
        pool = []
        for i in range(ceil(((self.rows * self.columns)/2))):
            pool.append(1)
            pool.append(0)
        shuffle(pool)
        for j in range(self.rows):
            row = []
            for k in range(self.columns):
                tile = Tile((j, k), pool.pop())
                row.append(tile)
            tilegrid.append(row)
        # Initialize vertical borders to None
        for count1 in range(self.rows):
            row = []
            for count2 in range(self.columns - 1):
                row.append(None)
            self.vertical_borders.append(row)
        # Initialize horizontal borders to None
        for count3 in range(self.rows - 1):
            row = []
            for count4 in range(self.columns):
                row.append(None)
            self.horizontal_borders.append(row)

    def update_borders(self, map_id, district):
        # check the surrounding tiles
        # find any that share a district with the passed in argument
        # find the borders that join those tiles and the tile represented by map_id
        # update those borders to hold the value of the district passed in in the argument
        coords = Game_Settings.map_id_to_coords(map_id)
        same_district_neighbors = []
        tile = self.tilegrid[coords[0]][coords[1]]
        for i in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            coords_adjacent = (coords[0] + i[0], coords[1] + i[1])
            if 0 <= coords_adjacent[0] < self.rows and 0 <= coords_adjacent[1] < self.columns:
                tile_adjacent = self.tilegrid[coords_adjacent[0]][coords_adjacent[1]]
                if tile_adjacent.district == district:
                    same_district_neighbors.append(tile_adjacent)
        for tile_adjacent in same_district_neighbors:
            # compare tile_adjacent to tile and find their shared border
            # update that border with district argument
            row_index = min([tile.coords[0], tile_adjacent.coords[0]])
            col_index = min([tile.coords[1], tile_adjacent.coords[1]])
            if tile.coords[0] == tile_adjacent.coords[0]:
                self.vertical_borders[row_index][col_index] = district
            elif tile.coords[1] == tile_adjacent.coords[1]:
                self.horizontal_borders[row_index][col_index] = district
            # print("########")
            # print(tile.coords[0])
            # print(tile.coords[1])
            # print(tile_adjacent.coords[0])
            # print(tile_adjacent.coords[1])
            # print("########")
            pass

    def print_board_simple(self):
        header = "   "
        for i in range(self.columns):
            header += (" " + str(i+1))
        print(header + "\n")
        for j in range(len(self.tilegrid)):
            row = self.tilegrid[j]
            line = Tile.num_to_alpha(j) + "  "
            for tile in row:
                line += (" " + tile.voter_preference)
            print(line)

    def print_board(self):
        # Print some initial spacing
        spacing = "    "
        header_row = ""
        header_row += spacing
        for ct1 in range(self.columns):
            header_row += "    "
            header_row += str(ct1 + 1)
            header_row += "   "
        print("\n" + header_row + "\n")
        print(spacing + ("-------" * self.columns) + ("-" * (self.columns + 1)))

        for ct2 in range(self.rows):
            row1 = row2 = row3 = row4 = ""
            row1 += spacing
            row2 = row2 + Game_Settings.num_to_alpha(ct2) + spacing[0:-1]
            row3 += spacing
            row4 += spacing
            # row1
            row1 += "|"
            # row2
            row2 += "|"
            # row3
            row3 += "|"
            for ct3 in range(self.columns):
                # do the voter info and spacing
                row2 += "  "
                tile = self.tilegrid[ct2][ct3]
                row2 += tile.voter_preference
                if tile.district is None:
                    row2 += tile.voter_preference
                else:
                    row2 += str(tile.district)
                row2 += tile.voter_preference
                row2 += "  "
                if ct3 < (self.columns - 1):
                    vert = self.vertical_borders[ct2][ct3]

                    row1 += "       "
                    if vert is not None:
                        row1 += " "
                    else:
                        row1 += "|"

                    if vert is not None:
                        row2 += str(vert)
                    else:
                        row2 += "|"

                    row3 += "       "
                    if vert is not None:
                        row3 += " "
                    else:
                        row3 += "|"
                if ct2 < (self.rows - 1):
                    horizontal = self.horizontal_borders[ct2][ct3]
                    row4 += "-"
                    if horizontal is not None:
                        row4 += "   " + str(horizontal) + "   "
                    else:
                        row4 += "-------"
            if ct2 < (self.rows - 1):
                row4 += "-"

            row1 += "       |"
            row2 += "|"
            row3 += "       |"
            # row3
            print(row1)
            print(row2)
            print(row3)
            if ct2 < (self.rows - 1):
                print(row4)

        print(spacing + ("-------" * self.columns) + ("-" * (self.columns + 1)))
