from board import Board


class Game:

    def __init__(self):
        print("\nInitializing game...\n")
        self.rows = 6
        self.columns = 7
        self.board = Board(self.rows, self.columns)
        self.board.print_board_simple()
        self.board.print_board()
