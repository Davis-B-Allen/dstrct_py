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
        self.congress_points_r = 0
        self.congress_points_d = 0
        self.player_names = []
        self.p1_affiliation = ""
        self.p2_affiliation = ""
        self.player_affiliations = []

    def play(self):
        self.print_rules()
        self.get_player_names_and_party()

        self.turn()

    def print_rules(self):
        print("Welcome to DSTRCT\n\n"
              "DSTRCT is a game about gerrymandering.\n\n"
              "The game board is a " + str(self.rows) + " by " + str(self.columns) + " grid "
              "of voters, each with a political preference: Democrat or Republican.\n"
              "Each player will assume the role of a political party (Democrat or Republican) and will take turns "
              "to divide up the game board into " + str(self.max_districts) + " districts, each with a "
              "maximum of " + str(Game_Settings.max_district_size) + " voters.\n"
              "There are exactly the same number of Democratic voters as Republican voters. However, with "
              "some clever choice of district boundaries, you can obtain more political power than your opponent.\n"
              "Within each district the party with the most votes will win the 'Congress Point' for that district.\n"
              "A full district of " + str(Game_Settings.max_district_size) + " voters will earn 1 Congress Point.\n"
              "A district of fewer than " + str(Game_Settings.max_district_size) + " voters will earn proportionally "
              "less than 1 Congress Point.\n"
              "If there is a tie within a district, the congress points will be split.")
        pass

    def get_player_names_and_party(self):
        p1_name = ""
        p2_name = ""
        p1_has_affiliation = False
        p2_has_affiliation = False
        while p1_name == "":
            p1_name = input("\nPlayer 1, please enter your name: ")
            self.player_names.append(p1_name)
        while not p1_has_affiliation:
            print("\nPlayer 1, please choose your party.")
            print("For Democrat, enter 'D'")
            print("For Republican, enter 'R'")
            print("To choose a third party, enter 'other'")
            self.p1_affiliation = input("> ")
            self.p1_affiliation = self.p1_affiliation.lower()
            if self.p1_affiliation == "d":
                p1_has_affiliation = True
                self.player_affiliations.append(0)
            elif self.p1_affiliation == "r":
                p1_has_affiliation = True
                self.player_affiliations.append(1)
            elif self.p1_affiliation == "other":
                print("Sorry, DSTRCT does not support victory for third parties, please choose either Democrat or Republican")
            else:
                print("Sorry, didn't understand that")
        while p2_name == "":
            p2_name = input("\nPlayer 2, please enter your name: ")
            self.player_names.append(p2_name)
        while not p2_has_affiliation:
            print("\nPlayer 2, please choose your party.")
            if self.p1_affiliation == "d":
                print("For Republican, enter 'R'")
            elif self.p1_affiliation == "r":
                print("For Democrat, enter 'D'")
            print("To choose a third party, enter 'other'")
            self.p2_affiliation = input("> ")
            self.p2_affiliation = self.p2_affiliation.lower()
            if self.p2_affiliation == "d" and self.p1_affiliation != "d":
                p2_has_affiliation = True
                self.player_affiliations.append(0)
            elif self.p2_affiliation == "r" and self.p1_affiliation != "r":
                p2_has_affiliation = True
                self.player_affiliations.append(1)
            elif self.p2_affiliation == "other":
                print("Sorry, DSTRCT does not support victory for third parties, please choose either Democrat or Republican")
            else:
                print("Sorry, didn't understand that")
        print()

    def is_game_over(self):
        # if self.num_turns > 13:
        #     return True
        # else:
        #     return False
        if len(self.board.districts) < self.max_districts:
            return False
        for tile in self.board.unplayed_tiles:
            if len(self.return_available_moves(tile.map_id)) > 0:
                return False
        return True

    def evaluate_game_and_print_result(self):
        while len(self.board.unplayed_tiles) > 0:
            tile = self.board.unplayed_tiles.pop()
            self.board.remnants.append(tile)
            empty_remnant_set = set()
            remnant_set = self.find_all_contiguous_undistricted_tiles(tile, empty_remnant_set)
            remnant_group = list(remnant_set)
            self.board.remnant_groups.append(remnant_group)
        print("\nRESULTS\n-------\n")
        self.board.print_board()
        for district in self.board.districts:
            d_sum = sum([t.voter_preference_int for t in district])
            d_len = len(district)
            d_cong_pt = d_len / Game_Settings.max_district_size
            if (d_sum / d_len) > 0.5:
                self.congress_points_r += d_cong_pt
            elif (d_sum / d_len) == 0.5:
                self.congress_points_r += (d_cong_pt / 2.0)
                self.congress_points_d += (d_cong_pt / 2.0)
            else:
                self.congress_points_d += d_cong_pt
        for rg in self.board.remnant_groups:
            r_sum = sum([t.voter_preference_int for t in rg])
            r_len = len(rg)
            r_cong_pt = r_len / Game_Settings.max_district_size
            if (r_sum / r_len) > 0.5:
                self.congress_points_r += r_cong_pt
            elif (r_sum / r_len) == 0.5:
                self.congress_points_r += (r_cong_pt / 2.0)
                self.congress_points_d += (r_cong_pt / 2.0)
            else:
                self.congress_points_d += r_cong_pt
        print("\nThe Democrats won " + str(self.congress_points_d) + " congress points")
        print("The Republicans won " + str(self.congress_points_r) + " congress points\n")
        if self.congress_points_d > self.congress_points_r:
            print("The Democrats win!\n")
        elif self.congress_points_d == self.congress_points_r:
            print("It's a tie!\n")
        else:
            print("The Republicans win!\n")

    def find_all_contiguous_undistricted_tiles(self, tile, remnant_group):
        remnant_group.add(tile)
        # look at adjacent tiles. if any of them are unplayed, include them in the
        coords = tile.coords
        for i in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            coords_adjacent = (coords[0] + i[0], coords[1] + i[1])
            if 0 <= coords_adjacent[0] < self.rows and 0 <= coords_adjacent[1] < self.columns:
                tile_adjacent = self.board.tilegrid[coords_adjacent[0]][coords_adjacent[1]]
                if tile_adjacent in self.board.unplayed_tiles:
                    self.board.unplayed_tiles.remove(tile_adjacent)
                    self.board.remnants.append(tile_adjacent)
                    recursive_remnant = self.find_all_contiguous_undistricted_tiles(tile_adjacent, remnant_group)
                    remnant_group = remnant_group | recursive_remnant
        return remnant_group

    def turn(self):
        self.board.print_board()
        complete_user_turn_input = self.fetch_complete_user_turn_input()
        if complete_user_turn_input[1] == len(self.board.districts):
            self.board.districts.append([])
        else:
            self.board.update_borders(complete_user_turn_input[0], complete_user_turn_input[1])
        coords = Game_Settings.map_id_to_coords(complete_user_turn_input[0])
        tile = self.board.tilegrid[coords[0]][coords[1]]
        self.board.unplayed_tiles.remove(tile)
        self.board.played_tiles.append(tile)
        tile.district = complete_user_turn_input[1]
        self.board.districts[complete_user_turn_input[1]].append(tile)
        self.whose_turn = 2 if (self.whose_turn == 1) else 1
        self.num_turns += 1
        if self.is_game_over():
            self.evaluate_game_and_print_result()
        else:
            self.turn()

    def fetch_complete_user_turn_input(self):
        map_id = self.capture_player_valid_tile_input()
        available_districts = self.return_available_moves(map_id)
        player_district_choice = self.capture_player_valid_district_input(available_districts)
        if player_district_choice == -1:
            return self.fetch_complete_user_turn_input()
        else:
            return [map_id, player_district_choice]

    def capture_player_valid_district_input(self, available_districts):
        new_district_available = len(self.board.districts) < self.max_districts
        while True:
            print("")
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
            player_choice = input(str(self.player_names[self.whose_turn - 1]) + " (Player " + str(self.whose_turn)
                                  + "), please choose a tile by column letter and row number (e.g. C4): ")
            move_is_valid_code = self.check_valid_move(player_choice)
        return player_choice

    def check_valid_move(self, player_input):
        # return codes key:
        # -3 -> cannot add district, and cannot add tile to existing district
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
        if len(available_districts) == 0:
            return -3
        return 1

    # return a set of districts
    def return_available_moves(self, valid_map_id):
        available_districts = []
        coords = Game_Settings.map_id_to_coords(valid_map_id)
        for i in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            coords_adjacent = (coords[0] + i[0], coords[1] + i[1])
            if 0 <= coords_adjacent[0] < self.rows and 0 <= coords_adjacent[1] < self.columns:
                tile_adjacent = self.board.tilegrid[coords_adjacent[0]][coords_adjacent[1]]
                if tile_adjacent.district is not None:
                    if len(self.board.districts[tile_adjacent.district]) < Game_Settings.max_district_size:
                        if tile_adjacent.district not in available_districts:
                            available_districts.append(tile_adjacent.district)
        if len(self.board.districts) < self.max_districts:
            available_districts.append(len(self.board.districts))
        return available_districts
