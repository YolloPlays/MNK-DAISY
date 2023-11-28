import tkinter as tk
from Game import Game
from Board import Board
from Player import Player
from MyBot import *
import random as rand
import numpy as np
import itertools as it
import pandas as pd

np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=np.inf)

root = tk.Tk()
root.title("MNKDATA")
root.geometry("400x426")

vertical_coords = []
horizontal_coords = []
cartesian = []

file = open("data.csv", "a")
frame = tk.Frame(root)
frame.pack(side="top")
label = tk.Label(frame)
label.pack(side="left")
btn = tk.Button(frame, text="Skip", command=lambda: draw_board())
btn.pack(side="left")
canvas = tk.Canvas(root, bg="lightgray")
canvas.pack(expand=True, fill="both")
canvas.bind("<1>", lambda event: handle_click(event))
def draw_board():
    
    global vertical_coords, horizontal_coords, cartesian, board
    b_m = rand.randint(3, 10)
    b_n = rand.randint(3, 10)
    b_k = rand.randint(2, max(b_m-1, b_n-1))
    board = Board(b_m, b_n, b_k,)
    vertical_coords = []
    horizontal_coords = []
    cartesian = []
    canvas.delete("all")
    label.configure(text=f"{board.n}x{board.m}x{board.k}")
    game = Game(board, Bot(1), Bot2(2))
    for row in range(1, board.n+1):
        y = (400/(board.n + 1)) * row
        vertical_coords.append(y)
        canvas.create_rectangle(0, y-1, 400, y+1, fill="black")
    for col in range(1, board.m+1):
        x = (400/(board.m + 1)) * col
        horizontal_coords.append(x)
        canvas.create_rectangle(x-1, 0, x+1, 400, fill="black")
    for y,x in it.product(vertical_coords, horizontal_coords):
            cartesian.append((x,y))
    for _ in range(rand.randint(2, board.array.size-1)):
        result = game.game_move(0,0)
        if game.board.has_won():
            return
        draw_chip(result)
        
    # for i in np.nditer(board.array):
    #     print(i)
    
def handle_click(event):
    radius = 30
    for idx, i in enumerate(cartesian):
        if i[0]-7 < event.x < i[0]+radius and i[1]-7 < event.y < i[1]+radius:
            log(idx,board.array, board.m, board.n, board.k)
            draw_board()
            
def draw_chip(results):
    global cartesian, canvas
    if results[0]:
        n = (results[2][1])*board.m + results[2][0]
        i = cartesian[n]
        canvas.create_oval(i[0]-10, i[1]-10, i[0]+10, i[1]+10, fill="blue" if results[1] else "red")

def log(idx, array: np.array, m, n, k):
    file.write(f"{array.flatten()};{m};{n};{k};{idx}\n")

draw_board()
root.mainloop()