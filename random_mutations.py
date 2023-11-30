from Game import Game
from MyBot import *
from Board import Board
import random as rand
import numpy as np

file = open("data5x5.csv", "a")

def move(game):
    for _ in range(rand.randint(2, max(game.board.array.size-4,3))):
            game.game_move(0,0)
            if game.board.has_won() or game.board.is_draw():
                return
    board_at = game.board.array
    _,_, chip_at = game.game_move(0,0)
    if game.board.has_won():
        return (chip_at, board_at)
    # for _ in range(rand.randint(2, max(game.board.array.size-4,3))):
    #         game.game_move(0,0)
    #         if game.board.has_won():
    #             return (chip_at, board_at)
    #         elif game.board.is_draw():
    #             return
def log(tup):
    if tup:
        for i in np.nditer(tup[1]):
            file.write(f"{i},")
        file.write(f"{5},{5},{4},{tup[0][0]*5+tup[0][1]}\n")
        
for i in range(1000000):
    if i % 500 == 0:
        print(i)
    log(move(Game(Board(5, 5, 4), Bot2(1), Bot2(2))))