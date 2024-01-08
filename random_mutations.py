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
    if game.board.has_won() == 1:
        return (chip_at, board_at)
    
def move_paths(game):
    for _ in range(rand.randint(2, max(game.board.array.size-4,3))):
            game.game_move(0,0)
            if game.board.has_won() or game.board.is_draw():
                return
    game_copy = game.copy()
    chip_at = None
    tmp_count = np.inf
    while not game_copy.board.has_won() and not game_copy.board.is_draw():
        res = game_copy.game_move(0,0)
        tmp_count+=1
        if game_copy.board.has_won() == 1:
            if tmp_count < moves_needed:
                moves_needed = tmp_count
                tmp_at = res[2]
        elif not game_copy.board.is_draw(): game.game_move(0,0)
    return (tmp_at, board_at)
    
        
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

i = 0
for _ in range(1000000):
    if i % 500 == 0:
        print(i)
        i+=1
    mv = move(Game(Board(5, 5, 4), Bot2(1), Bot2(2)))
    log(mv)
    if mv:
        i += 1