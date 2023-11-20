from random import randint
from Player import Player
from Board import Board

class Bot(Player):
    def __init__(self, name: str, player_number: int):
        super().__init__(name, player_number)

    def make_move(self, board):
        for row in range(board.n):
            for col in range(board.m):
                if board[row][col] == 0: # empty cell
            
            
            m = randint # TODO add numbers
            n = randint
            
            