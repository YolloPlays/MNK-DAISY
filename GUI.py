"""
 @author jabo
 @create date 18.11.2023
 @desc GUI for MNK
"""

import tkinter as tk
import Board, Game, Player
from PIL import Image,ImageTk
import itertools as it
import platform

# TODO: Let GUI make game. start button needed 

class GUI:
    def __init__(self) -> None:
        paths = [r"images\LightBig.png", r"images\LightSmall.png", r"images\stick-hori.png", r"images\stick.png",
                    r"images\circle_red.png", r"images\circle_blue.png", r"images\blue_won.png", r"images\red_won.png"]
        if platform.system() == "Windows":
            import pyglet
            pyglet.options['win32_gdi_font'] = True # Necessary for tkinter quirk
            pyglet.font.add_file(r'font\Tr2n.ttf')
        else:
            for idx, path in enumerate(paths):
                paths[idx] = path.replace("\\", "/")
            
        self.game_started = False
        self.move_blocked = False
        self.vertical_coords = []
        self.horizontal_coords = []
        self.cartesian = []
        self.root = tk.Tk()
        self.root.title("MNK")
        self.root.configure(bg="#434343")
        self.root.geometry("1000x600")

        self.game_frame = tk.Frame(self.root, bg="#434343")
        self.game_frame.pack(padx=64, pady=64, side="left", fill="both")

        self.game_img = tk.PhotoImage(file=paths[0])

        self.stats_frame = tk.Frame(self.root, bg="#434343")
        self.stats_frame.pack(padx=20, pady=64, side="right", fill="both")

        self.stats_img = tk.PhotoImage(file=paths[1])
        
        self.stick_hori_img = tk.PhotoImage(file=paths[2])
        self.stick_img = tk.PhotoImage(file=paths[3])
        self.cricle_red = tk.PhotoImage(file=paths[4])
        self.cricle_blue = tk.PhotoImage(file=paths[5])
        self.win_blue = tk.PhotoImage(file=paths[6])
        self.win_red = tk.PhotoImage(file=paths[7])
        
        self.start_button = tk.Button(self.root, bg="blue", command=self.init_game, text="Start")
        self.start_button.pack(padx=100, pady=100, fill="both", expand=1)
        # self.init_game() # Debug

        self.root.bind("<1>", self.handle_click)
        self.root.bind("<space>", self.delete_rows) #DEBUG

        self.root.mainloop()
        
    def delete_rows(self, event): #DEBUG
        self.game_canvas.delete("row")
    def delete_cols(self, event):
        self.game_canvas.delete("col")
        
    def init_game(self):
        self.game_started = True
        self.game: Game = Game.Game(Board.Board(), Player.Player("Jannis", 1)) # DEBUG: Will later be replaced by buttons
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
    
    def on_grid(self, event: tk.Event, i: tuple):
        radius = 20
        return self.is_in_between(event.x, i[0]-7, i[0]+radius) and self.is_in_between(event.y, i[1]-7, i[1]+radius)
    
    def draw_chip(self, results):
        if results[0]:
            n = (results[2][1])*self.m + results[2][0]
            i = self.cartesian[n]
            self.game_canvas.create_image(i[0]-22, i[1]-22, image=self.cricle_blue if results[1] else self.cricle_red, anchor="nw")

    def handle_click(self, event: tk.Event):
        if self.game_started and event.widget == self.game_canvas and not self.move_blocked:
            for idx, i in enumerate(self.cartesian):
                if self.on_grid(event, i):
                    results = self.game.game_move(m=idx % self.m, n=int(idx/self.m))
                    self.move_blocked = True
                    self.draw_chip(results)
                    self.root.after(700, self.toggle_block)
                    if winner:=self.game.board.has_won():
                        self.root.after(1200, self.display_win, winner-1) # winner-1 is basically is_red?
                        # self.display_win(winner-1)
                    elif self.game.is_bot():
                        self.root.after(600, self.draw_chip, self.game.game_move(0,0))
                        # self.draw_chip(self.game.game_move(0,0)) DEBUG: Without delay
                        
                        
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
        self.draw_rows()
        self.draw_cols()
        for y,x in it.product(self.vertical_coords, self.horizontal_coords):
            self.cartesian.append((x,y))
        # for i in self.cartesian: #DEBUG
        #     self.game_canvas.create_rectangle(i[0]-7,i[1]-7,i[0]+20,i[1]+20)
        # print(self.cartesian)
            
    def draw_cols(self):
        for i in range(1, self.m + 1):
            x = (400/(self.m + 1)) * i  + 29
            self.game_canvas.create_image(x, 36, image=self.stick_img, anchor="nw", tags="col")
            self.horizontal_coords.append(x)
    def draw_rows(self):
        for i in range(1, self.n + 1):
            y = (400/(self.n + 1)) * i  + 29
            self.game_canvas.create_image(36, y, image=self.stick_hori_img, anchor="nw", tags="row")
            self.vertical_coords.append(y)
            
    def toggle_block(self):
        self.move_blocked = not self.move_blocked
            
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