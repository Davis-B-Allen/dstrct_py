from tile import Tile
from game_settings import Game_Settings
from random import shuffle


class Board:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.tilegrid = []
        self.districts = []
        self.vertical_borders = []
        self.horizontal_borders = []
        print("Setting up board...\n")
        self.set_up_board(self.tilegrid)

    def set_up_board(self, tilegrid):
        # Create random distribution of tiles with same number of each type of voter
        pool = []
        for i in range(self.rows * self.columns):
            pool.append(1)
            pool.append(0)
        shuffle(pool)
        for j in range(self.rows):
            row = []
            for k in range(self.columns):
                tile = Tile((j,k), pool.pop())
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
            row1 = row2 = row3 = ""
            row1 += spacing
            row2 = row2 + Game_Settings.num_to_alpha(ct2) + spacing[0:-1]
            row3 += spacing
            #row1
            row1 += "|"
            #row2
            row2 += "|"
            #row3
            row3 += "|"
            for ct3 in range(self.columns):
                #do the voter info and spacing
                row2 += "  "
                tile = self.tilegrid[ct2][ct3]
                row2 += tile.voter_preference
                if tile.district == None:
                    row2 += tile.voter_preference
                else:
                    row2 += str(tile.district)
                row2 += tile.voter_preference
                row2 += "  "
                if ct3 < (self.columns - 1):
                    vert = self.vertical_borders[ct2][ct3]

                    row1 += "       "
                    if vert != None:
                        row1 += " "
                    else:
                        row1 += "|"

                    if vert != None:
                        row2 += vert
                    else:
                        row2 += "|"

                    row3 += "       "
                    if vert != None:
                        row3 += " "
                    else:
                        row3 += "|"

            row1 += "       |"
            row2 += "|"
            row3 += "       |"
            #row3
            print(row1)
            print(row2)
            print(row3)

            # TODO update this so that it prints the horizontal borders properly

            print(spacing + ("-------" * self.columns) + ("-" * (self.columns + 1)))
