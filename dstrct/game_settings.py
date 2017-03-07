class Game_Settings:

    def __init__(self):
        pass

    # TODO Should this be a static method or a class method?
    @staticmethod
    def num_to_alpha(some_int):
        num_alpha_map = {
            0  : "A",
            1  : "B",
            2  : "C",
            3  : "D",
            4  : "E",
            5  : "F",
            6  : "G",
            7  : "H",
            8  : "I",
            9  : "J"
        }
        return num_alpha_map[some_int]
