"""
 @author jabo
 @create date 18.11.2023
 @desc GUI for MNK
"""

import tkinter as tk
import Board, Game, Player
from PIL import Image,ImageTk
import itertools as it
import pyglet
import platform

# TODO: Let GUI make game. start button needed 

class GUI:
    def __init__(self) -> None:
        if platform.system() == "Windows":
            pyglet.options['win32_gdi_font'] = True # Necessary for tkinter quirk
            pyglet.font.add_file('font\\Tr2n.ttf')
        self.game_started = False
        self.vertical_coords = []
        self.horizontal_coords = []
        self.cartesian = []
        self.root = tk.Tk()
        self.root.title("MNK")
        self.root.configure(bg="#434343")
        self.root.geometry("1000x600")

        self.game_frame = tk.Frame(self.root, bg="#434343")
        self.game_frame.pack(padx=64, pady=64, side="left", fill="both")

        self.game_img = tk.PhotoImage(file="images\\LightBig.png")

        self.stats_frame = tk.Frame(self.root, bg="#434343")
        self.stats_frame.pack(padx=20, pady=64, side="right", fill="both")

        self.stats_img = tk.PhotoImage(file="images\\LightSmall.png")
        
        self.stick_hori_img = tk.PhotoImage(file="images\\stick-hori.png")
        self.stick_img = tk.PhotoImage(file="images\\stick.png")
        self.cricle_red = tk.PhotoImage(file="images\\circle_red.png")
        self.cricle_blue = tk.PhotoImage(file="images\\circle_blue.png")
        self.win_blue = tk.PhotoImage(file="images\\blue_won.png")
        self.win_red = tk.PhotoImage(file="images\\red_won.png")
        
        self.start_button = tk.Button(self.root, bg="blue", command=self.init_game, text="Start")
        self.start_button.pack(padx=100, pady=100, fill="both")
        # self.init_game() # Debug

        self.root.bind("<1>", self.handle_click)

        self.root.mainloop()
        
    def init_game(self):
        self.game_started = True
        self.game: Game = Game.Game(Board.Board(), Player.Player("Ric", 1), Player.Player("Jannis", 2))
        self.m = self.game.board.m
        self.n = self.game.board.n
        self.game.gui = self
        self.game.playermode = False
        self.playersturn = True
        self.start_button.destroy()
        self.draw_game()
        self.draw_grid()    
    
    def is_in_between(self, a,b,c):
        return b <= a <= c
    
    def in_boundaries(self, x, y):
        return self.is_in_between(x,self.game_canvas.winfo_rootx(), self.game_canvas.winfo_rootx() + self.game_canvas.winfo_width()) and self.is_in_between(y, self.game_canvas.winfo_rooty(), self.game_canvas.winfo_rooty() + self.game_canvas.winfo_height())
    
    def on_grid(self, event: tk.Event, i: tuple):
        radius =30
        return self.is_in_between(event.x, i[0]-radius, i[0]+radius) and self.is_in_between(event.y, i[1]-radius, i[1]+radius)
    
    def draw_chip(self, results):
        if results[0]:
            n = (results[2][1])*5 + results[2][0]
            i = self.cartesian[n]
            self.game_canvas.create_image(i[0]-22, i[1]-22, image=self.cricle_blue if results[1] else self.cricle_red, anchor="nw")

    def handle_click(self, event: tk.Event):
        if self.game_started and self.in_boundaries(event.x_root, event.y_root):
            for idx, i in enumerate(self.cartesian):
                if self.on_grid(event, i):
                    results = self.game.game_move(idx % self.m, int(idx/self.m))
                    self.draw_chip(results)
                    if winner:=self.game.board.has_won():
                        self.display_win(winner-1)
                    if self.game.bot_game and (results_bot:=self.game.player2.make_move()):
                        self.draw_chip((True, True, results_bot))
                        
    def draw_game(self):
        self.game_canvas = tk.Canvas(self.game_frame, width=472, height=472, bg="#434343", highlightthickness=0)
        self.game_canvas.pack()
        self.game_canvas.create_rectangle(35, 35, 436, 436, fill="#393939")
        self.game_canvas.create_image(0, 0, image=self.game_img, anchor="nw")
        
        self.stats_canvas = tk.Canvas(self.stats_frame, width=347, height=399, bg="#434343", highlightthickness=0)
        self.stats_canvas.pack()
        self.stats_canvas.create_rectangle(35, 35, 311, 190, fill="#393939")
        self.stats_canvas.create_rectangle(35, 208, 311, 363, fill="#393939")
        self.stats_canvas.create_image(0, 0, image=self.stats_img, anchor="nw")
        
        
                        
    def draw_grid(self):
        for i in range(1, self.m + 1):
            x = (400/(self.m + 1)) * i  + 29
            self.game_canvas.create_image(x, 36, image=self.stick_img, anchor="nw")
            self.horizontal_coords.append(x)
        for i in range(1, self.n + 1):
            y = (400/(self.n + 1)) * i  + 29
            self.game_canvas.create_image(36, y, image=self.stick_hori_img, anchor="nw")
            self.vertical_coords.append(y)
        for i in it.product(self.vertical_coords, self.horizontal_coords):
            self.cartesian.append(i)
            
    def display_win(self, player):
        for widget in self.root.winfo_children():
            widget.pack_forget()
        winner_canvas = tk.Canvas(self.root, bg="#434343")
        winner_canvas.pack(fill="both", expand=1)
        winner_img, winner_txt = (self.win_blue, self.game.player1.name) if not player else (self.win_red, self.game.player2.name)
        winner_canvas.create_image(0, 0, image=winner_img, anchor="nw")
        winner_canvas.create_text(263, 295, font=("TR2N",62), text=winner_txt, fill="white")
        
        
        
if __name__ == "__main__":
    # Game.Game(Board.Board(), Player.Player("Klaus", 1), Player.Player("Peter", 2))
    GUI()