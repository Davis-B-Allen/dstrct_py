class Game_Settings:

    max_district_size = 7
    num_alpha_nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    num_alpha_alphas = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    num_alpha_map = dict()
    alpha_num_map = dict()
    for i in range(len(num_alpha_nums)):
        num_alpha_map[num_alpha_nums[i]] = num_alpha_alphas[i]
        alpha_num_map[num_alpha_alphas[i]] = num_alpha_nums[i]

    def __init__(self):
        pass

    # TODO Should this be a static method or a class method?
    @staticmethod
    def num_to_alpha(some_int):
        return Game_Settings.num_alpha_map[some_int]

    # TODO Should this be a static method or a class method?
    @staticmethod
    def alpha_to_num(some_str):
        return Game_Settings.alpha_num_map[some_str]

    # TODO Should this be a static method or a class method?
    @staticmethod
    def map_id_to_coords(valid_map_id_str):
        row_char = valid_map_id_str[0].upper()
        row_index = Game_Settings.alpha_num_map[row_char]
        column_index = int(valid_map_id_str[1]) - 1
        return (row_index, column_index)

