class Tile:

    def __init__(self, coords, voter_preference_int):
        self.coords = coords
        self.voter_preference_int = voter_preference_int
        self.map_id = self.convert_coords_to_map_id(coords)
        self.voter_preference = "D" if voter_preference_int == 0 else "R"
        self.district = None

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

    # TODO maybe turn this into static method
    def convert_coords_to_map_id(self, coords):
        return Tile.num_to_alpha(coords[0]) + str(coords[1] + 1)

