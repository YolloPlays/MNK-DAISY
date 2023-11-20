from random import randint
from Player import Player

class Bot(Player):
    pass

    def make_move(self, board):
        while True:
            m = randint # TODO add numbers
            n = randint
            if 0 <= m < board.m and 0 <= n < board.n:
                if board.array[m][n] == 0:
                    board.array[m][n] = self.player_number
                    return board.array[m][n]
                else:
                    print('Dieser Punkt ist bereits besetzt!')
            else:
                print ("Diese Position ist außerhalb des Spielfelds.")