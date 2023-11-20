from random import randint
from Player import Player
from Board import Board

class Bot(Player):
    def __init__(self):
        super().__init__("KI", 2)

    def make_move(self, board):
        empty_cells = []
        for col in range(board.m):
            for row in range(board.n):
                empty_cells.append((row,col)) if board[row][col] == 0 else None
                    
            
            
            m = randint # TODO add numbers
            n = randint
            
            