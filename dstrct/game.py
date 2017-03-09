from board import Board
from game_settings import Game_Settings


class Game:

    def __init__(self):
        print("\nInitializing game...\n")
        self.rows = 6
        self.columns = 7
        self.max_districts = 6
        self.board = Board(self.rows, self.columns)
        self.whose_turn = 1
        self.num_turns = 0

    def play(self):
        self.turn()

    def is_game_over(self):
        return self.num_turns > 10

    def turn(self):
        self.board.print_board()

        complete_user_turn_input = self.fetch_complete_user_turn_input()

        print("********* " + str(complete_user_turn_input[1]) + " *********")

        if complete_user_turn_input[1] == len(self.board.districts):
            self.board.districts.append([])
        else:
            self.board.update_borders(complete_user_turn_input[0], complete_user_turn_input[1])
            pass
        coords = Game_Settings.map_id_to_coords(complete_user_turn_input[0])
        tile = self.board.tilegrid[coords[0]][coords[1]]
        tile.district = complete_user_turn_input[1]
        self.board.districts[complete_user_turn_input[1]].append(tile)

        self.whose_turn = 2 if (self.whose_turn == 1) else 1
        self.num_turns += 1
        if self.is_game_over():
            print("Game Over !!!")
        else:
            self.turn()

    def fetch_complete_user_turn_input(self):
        map_id = self.capture_player_valid_tile_input()
        available_districts = self.return_available_moves(map_id)
        print("***********************************")
        print("Available districts:")
        print(available_districts)
        print("***********************************")
        player_district_choice = self.capture_player_valid_district_input(available_districts)
        if player_district_choice == -1:
            return self.fetch_complete_user_turn_input()
        else:
            return [map_id, player_district_choice]

    def capture_player_valid_district_input(self, available_districts):
        new_district_available = len(self.board.districts) < self.max_districts
        while True:
            for district in available_districts:
                if district < len(self.board.districts):
                    print("Please enter '" + str(district) + "' to add to district " + str(district))
                else:
                    print("Please enter 'new' to create a new district and add this tile to it.")
            print("If you'd like to go back and choose a different tile, type 'back'")
            player_input = input("> ")
            if player_input.isdigit():
                if int(player_input) in range(len(self.board.districts)):
                    return int(player_input)
            elif new_district_available and player_input.lower() == "new":
                return len(self.board.districts)
            elif player_input.lower() == "back":
                return -1
            else:
                print("Sorry didn't understand that")

    def capture_player_valid_tile_input(self):
        player_choice = ""
        move_is_valid_code = self.check_valid_move(player_choice)
        while move_is_valid_code < 1:
            if move_is_valid_code == -1:
                print("Not a valid tile code")
            elif move_is_valid_code == -2:
                print("Tile already belongs to a district!")
            elif move_is_valid_code == -3:
                print("No available moves for this tile")
            player_choice = input("Player " + str(self.whose_turn) + ", please choose a tile by column letter and row number (e.g. C4): ")
            move_is_valid_code = self.check_valid_move(player_choice)
        return player_choice

    def check_valid_move(self, player_input):
        # return codes key:
        # -2 -> no available moves for this tile
        # -1 -> not a valid tile code
        # 0 -> no input, don't return error message, just prompt again
        # 1 -> valid tile code with available moves
        if len(player_input) == 0:
            return 0
        if len(player_input) != 2:
            return -1
        if not player_input[-1].isdigit():
            return -1
        row_char = player_input[0].upper()
        column_index = int(player_input[1]) - 1
        if row_char not in Game_Settings.num_alpha_alphas[0:self.rows]:
            return -1
        if column_index not in Game_Settings.num_alpha_nums[0:self.columns]:
            return -1
        # map_id = player_input
        coords = Game_Settings.map_id_to_coords(player_input)
        tile = self.board.tilegrid[coords[0]][coords[1]]
        if tile.district is not None:
            return -2
        available_districts = self.return_available_moves(player_input)
        if len(available_districts) <= 0:
            return -3
        return 1

    # return a set of districts
    def return_available_moves(self, valid_map_id):
        available_districts = []
        coords = Game_Settings.map_id_to_coords(valid_map_id)
        for i in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            coords_adjacent = (coords[0] + i[0], coords[1] + i[1])
            print("coords_adjacent 1:" + str(coords_adjacent))
            if 0 <= coords_adjacent[0] < self.rows and 0 <= coords_adjacent[1] < self.columns:
                print("coords_adjacent 2:" + str(coords_adjacent))
                tile_adjacent = self.board.tilegrid[coords_adjacent[0]][coords_adjacent[1]]
                if tile_adjacent.district is not None:
                    if len(self.board.districts[tile_adjacent.district]) < Game_Settings.max_district_size:
                        if tile_adjacent.district not in available_districts:
                            available_districts.append(tile_adjacent.district)
        if len(self.board.districts) < self.max_districts:
            available_districts.append(len(self.board.districts))
        return available_districts
