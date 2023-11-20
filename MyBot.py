from random import choice
from Player import Player
from Board import Board

class Bot(Player):
    def __init__(self):
        super().__init__("KI", 2)

    def make_move(self, board):
        empty_cells = []
        for col in range(board.m):
            for row in range(board.n):
                empty_cells.append((row,col)) if board.array[row][col] == 0 else None
        
        # Randomly select a cell to place the disc
        return choice(empty_cells)

if __name__ == "__main__":

    board = Board()
    board.array[0][1] = 1
    board.display()
    bot = Bot()
    print(bot.make_move(board))