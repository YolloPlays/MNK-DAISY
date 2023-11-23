"""
 @author jabo
 @create date 18.11.2023
 @desc GUI for MNK
"""

import tkinter as tk
from tkinter import ttk
from Board import Board
from Game import Game
from MyBot import *
from Player import Player
from PIL import Image,ImageTk
import itertools as it
import platform

# TODO: Let GUI make game. start button needed 

class GUI:
    def __init__(self) -> None:
        self.paths = [r"images\LightBig.png", r"images\LightSmall.png", r"images\stick-hori.png", r"images\stick.png",
                    r"images\circle_red.png", r"images\circle_blue.png", r"images\blue_won.png", r"images\red_won.png", r"images\button_case.png",
                    r"images\button_case_active.png", r"images\slider.png", r"images\slider_active.png", r"images\thru.png"]
        if platform.system() == "Windows":
            import pyglet
            pyglet.options['win32_gdi_font'] = True # Necessary for tkinter quirk
            pyglet.font.add_file(r'font\Tr2n.ttf')
        else:
            for idx, path in enumerate(self.paths):
                self.paths[idx] = path.replace("\\", "/")
            
        self.game_started = False
        self.move_blocked = False
        self.vertical_coords = []
        self.horizontal_coords = []
        self.cartesian = []
        self.root = tk.Tk()
        self.root.title("MNK")
        self.root.configure(bg="#434343")
        self.root.geometry("1000x700")

        self.game_frame = tk.Frame(self.root, bg="#434343")
        self.game_frame.pack(padx=64, pady=64, side="left", fill="both")

        self.game_img = tk.PhotoImage(file=self.paths[0])

        self.stats_frame = tk.Frame(self.root, bg="#434343")
        self.stats_frame.pack(padx=20, pady=64, side="right", fill="both")
        
        self.slider_frame = tk.Frame(self.stats_frame, bg="#434343")
        self.slider_frame.pack(padx=20, pady=10, side="top", fill="x")
        self.place_holder1 = tk.Canvas(self.slider_frame, width=1, height=20, bg="#434343", highlightthickness=0)
        self.place_holder1.pack()
        self.selection_frame = tk.Frame(self.stats_frame, bg="#434343")
        self.selection_frame.pack(side="top", fill="x")
        
        self.stats_img = tk.PhotoImage(file=self.paths[1])
        
        self.stick_hori_img = tk.PhotoImage(file=self.paths[2])
        self.stick_img = tk.PhotoImage(file=self.paths[3])
        self.cricle_red = tk.PhotoImage(file=self.paths[4])
        self.cricle_blue = tk.PhotoImage(file=self.paths[5])
        self.win_blue = tk.PhotoImage(file=self.paths[6])
        self.win_red = tk.PhotoImage(file=self.paths[7])
        self.button_case = tk.PhotoImage(file=self.paths[8])
        self.button_case_active = tk.PhotoImage(file=self.paths[9])
        

        self.root.bind("<1>", self.handle_click)
        
        self.img_slider = tk.PhotoImage(file=self.paths[10])
        self.img_slider_active = tk.PhotoImage(file=self.paths[11])
        self.trough = tk.PhotoImage(file=self.paths[12])
        self.style = ttk.Style(self.stats_frame)
        self.style.element_create('custom.Scale.trough', 'image', self.trough)
        self.style.element_create('custom.Horizontal.Scale.slider', 'image', self.img_slider,
                     ('active', self.img_slider_active))
        self.style.layout('custom.Horizontal.TScale', [('custom.Scale.trough', {'sticky': 'we'}),
            ('Horizontal.Scale.trough',
               {'sticky': 'nswe',
                'children': [('custom.Horizontal.Scale.slider',
                              {'side': 'left', 'sticky': ''})]})])
        self.style.configure('custom.Horizontal.TScale', background="#434343")
                
        #Move to start
        self.game: Game = Game(Board(), Player("Jannis", 1), Player("John",2)) # DEBUG: Will later be replaced by buttons
        self.m = self.game.board.m
        self.n = self.game.board.n
        self.k = self.game.board.k
        self.root.bind("<space>", self.debug) #DEBUG
        self.draw_slider()
        self.draw_game()
        self.draw_grid()
        self.draw_gamemode_buttons()
        self.game.gui = self
        self.playersturn = True

        self.root.mainloop()
        
    def delete_rows(self, event=None): #DEBUG
        self.game_canvas.delete("row")
        self.vertical_coords = []
    def delete_cols(self, event=None):
        self.game_canvas.delete("col")
        self.horizontal_coords=[]
    
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
    
        
    def scale_change_m(self, valstr):
        self.delete_cols()
        val = int(float(valstr))
        val_label = str(val)
        self.m = val
        self.slider_label_m.configure(text=val)
        max_k = self.m if self.m > self.n else self.n
        self.k_slide.configure(to=max_k)
        if max_k < self.k_slide.get():
            self.k_slide.set(max_k)
            self.slider_label_k.configure(text=int(max_k))
        self.draw_cols()
    
    def scale_change_n(self, valstr):
        self.delete_rows()
        val = int(float(valstr))
        self.n = val
        self.slider_label_n.configure(text=val)
        max_k = self.m if self.m > self.n else self.n
        self.k_slide.configure(to=max_k)
        if max_k < self.k_slide.get():
            self.k = max_k
            self.k_slide.set(max_k)
            self.slider_label_k.configure(text=int(max_k))
        self.draw_rows()
        
    def scale_change_k(self, valstr):
        val = int(float(valstr))
        self.k = val
        self.slider_label_k.configure(text=val)
        

        
    def press_play(self):
        self.slider_frame.destroy()
        self.play_button.destroy()
        self.cartesian = []
        for y,x in it.product(self.vertical_coords, self.horizontal_coords):
            self.cartesian.append((x,y))
        self.game_started = True
        self.stats_canvas.create_rectangle(35, 35, 311, 190, fill="#393939")
        self.stats_canvas.create_rectangle(35, 208, 311, 363, fill="#393939")
        self.stats_canvas.create_image(0, 0, image=self.stats_img, anchor="nw")
        self.game.board.array = Board.make_array(self.m, self.n)
        self.game.board.k = self.k
        self.game.board.n = self.n
        self.game.board.m = self.m
        
    def create_button(self, frame, command, bg, image, name):
        temp_btn = tk.Button(frame, command=command, bg=bg, bd=0, image=image, name=name)
        temp_btn.bind('<Enter>', self.on_enter)
        temp_btn.bind('<Leave>', self.on_leave)
        return temp_btn
    
    def draw_gamemode_buttons(self):
        def create_gmbtn(name):
            return self.create_button(self.selection_frame, command=self.change_gamemode, bg="#393939", image=self.button_case, name=name)
            
        self.bot_btn = create_gmbtn("bot")
        self.bot_btn.place(x=50,y=50)
        self.bot1_btn = create_gmbtn("bot1")
        self.bot2_btn = create_gmbtn("bot2")
        
                        
    def draw_game(self):
        self.game_canvas = tk.Canvas(self.game_frame, width=472, height=472, bg="#434343", highlightthickness=0)
        self.game_canvas.pack()
        self.game_canvas.create_rectangle(35, 35, 436, 436, fill="#393939")
        self.game_canvas.create_image(0, 0, image=self.game_img, anchor="nw")
        self.play_button = self.create_button(self.game_frame, command=self.press_play, bg="#434343", image=self.button_case, name="play")
        self.play_button.pack(side="top")
        
        self.stats_canvas = tk.Canvas(self.selection_frame, width=347, height=399, bg="#434343", highlightthickness=0)
        self.stats_canvas.pack(side="top")
        self.m_slide = ttk.Scale(self.slider_frame, from_=2, to=10, orient=tk.HORIZONTAL, style="custom.Horizontal.TScale", length=200, value=5, command=self.scale_change_m)
        self.n_slide = ttk.Scale(self.slider_frame, from_=2, to=10, orient=tk.HORIZONTAL, style="custom.Horizontal.TScale", length=200, value=5, command=self.scale_change_n)
        self.k_slide = ttk.Scale(self.slider_frame, from_=2, to=5, orient=tk.HORIZONTAL, style="custom.Horizontal.TScale", length=200, value=4, command=self.scale_change_k)
        self.m_slide.pack()
        self.n_slide.pack()
        self.k_slide.pack()
        self.stats_canvas.create_rectangle(35, 35, 311, 190, fill="#393939")
        self.stats_canvas.create_rectangle(35, 208, 311, 363, fill="#393939")
        self.stats_canvas.create_image(0, 0, image=self.stats_img, anchor="nw")
        
    def draw_slider(self):
        self.slider_label_frame = tk.Frame(self.slider_frame, bg="#434343")
        self.slider_label_frame.pack(side="right", fill="x")
        self.sname_label_frame = tk.Frame(self.slider_frame, bg="#434343")
        self.sname_label_frame.pack(side="left", fill="x")
        PADY = 5
        self.slider_label_m = tk.Label(self.slider_label_frame, text=5, font=("TR2N",22), bg="#434343",fg="white")
        self.slider_label_m.pack(side="top",pady=PADY)
        self.slider_label_n = tk.Label(self.slider_label_frame, text=5, font=("TR2N",22), bg="#434343", fg="white")
        self.slider_label_n.pack(side="top",pady=PADY)
        self.slider_label_k = tk.Label(self.slider_label_frame, text=4, font=("TR2N",22), bg="#434343", fg="white")
        self.slider_label_k.pack(side="top",pady=PADY)
        self.sname_label_m = tk.Label(self.sname_label_frame, text="m", font=("TR2N",22), bg="#434343", fg="white")
        self.sname_label_m.pack(side="top",pady=PADY)
        self.sname_label_n = tk.Label(self.sname_label_frame, text="n", font=("TR2N",22), bg="#434343", fg="white")
        self.sname_label_n.pack(side="top",pady=PADY)
        self.sname_label_k = tk.Label(self.sname_label_frame, text="k", font=("TR2N",22), bg="#434343", fg="white")
        self.sname_label_k.pack(side="top",pady=PADY)
        
    def on_leave(self, event):
        event.widget.config(image=self.button_case)
    def on_enter(self, event: tk.Event):
        event.widget.config(image=self.button_case_active)
        
    def change_gamemode(self,event: tk.Event): #PROOF OF CONCEPT
        modes = {"bot": Bot(), "bot1": Bot1(), "bot2": Bot2()}
        self.player1 = modes[event.widget._name]
        pass
                        
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
        
    def debug(self, event):
        print(f"GUI: m: {self.m} n: {self.n} k: {self.k}")
        print(f"Board: m: {self.game.board.m} n: {self.game.board.n} k: {self.game.board.k}")
        
        
if __name__ == "__main__":
    # Game.Game(Board.Board(), Player.Player("Klaus", 1), Player.Player("Peter", 2))
    GUI()