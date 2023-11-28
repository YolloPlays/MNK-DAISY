"""
 @author jabo
 @create date 18.11.2023
 @desc GUI for MNK
"""

import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from Board import Board
from Game import Game
from MyBot import *
from Player import Player
from PIL import Image,ImageTk
import itertools as it
import platform

class GUI:
    def __init__(self) -> None:
        self.paths = [r"images\LightBig.png", r"images\LightSmall.png", r"images\stick-hori.png", r"images\stick.png",
                    r"images\circle_red.png", r"images\circle_blue.png", r"images\blue_won.png", r"images\red_won.png",
                    r"images\slider.png", r"images\slider_active.png", r"images\thru.png", r"images\button_case.png",
                    r"images\button_case_active.png", r"images\light_small_alt.png", r"images\MNKLogo.ico", r"images\#.png", r"images\#_active.png"]
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
        self.btn_lst = []
        self.BUTTON_COUNT = 6
        self.root = tk.Tk()
        self.root.title("MNK")
        self.root.configure(bg="#434343")
        self.root.geometry("1000x700")
        
        self.button_toggle1 = None
        self.button_toggle2 = None
        self.player1 = Player("<p>",1)
        self.player2 = Player("<p>",2)

        self.draw_pre_frames()
        
        self.images = [tk.PhotoImage(file=path) for path in self.paths[:-3]]
        self.icons = {str(i): tk.PhotoImage(file=self.paths[-2].replace('#', str(i))) for i in range(8)}
        self.icons_active = {str(i): tk.PhotoImage(file=self.paths[-1].replace('#', str(i))) for i in range(8)}

        self.root.bind("<1>", self.handle_click)
        
        self.style = ttk.Style(self.stats_frame)
        self.style.element_create('custom.Scale.trough', 'image', self.images[10])
        self.style.element_create('custom.Horizontal.Scale.slider', 'image', self.images[8],
                     ('active', self.images[9]))
        self.style.layout('custom.Horizontal.TScale', [('custom.Scale.trough', {'sticky': 'we'}),
            ('Horizontal.Scale.trough',
               {'sticky': 'nswe',
                'children': [('custom.Horizontal.Scale.slider',
                              {'side': 'left', 'sticky': ''})]})])
        self.style.configure('custom.Horizontal.TScale', background="#434343")
        
        self.m = 5
        self.n = 5
        self.k = 4
        self.draw_slider()
        self.draw_game()
        self.draw_grid()
        self.draw_gamemode_buttons()
        self.playersturn = True

        self.root.iconbitmap(self.paths[-3])
        self.root.mainloop()
        
    def delete_rows(self, event=None):
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
            self.game_canvas.create_image(i[0]-22, i[1]-22, image=self.images[5] if results[1] else self.images[4], anchor="nw")

    def handle_click(self, event: tk.Event):
        if self.game_started and event.widget == self.game_canvas and not self.move_blocked:
            for idx, i in enumerate(self.cartesian):
                if self.on_grid(event, i):
                    results = self.game.game_move(m=idx % self.m, n=idx//self.m)
                    self.move_blocked = True
                    self.draw_chip(results)
                    self.root.after(200, self.toggle_block)
                    if winner:=self.game.board.has_won():
                        self.root.after(1200, self.display_win, winner-1) # winner-1 is basically is_red?
                    elif self.game.board.is_draw():
                        self.display_draw()
                    elif self.game.is_bot():
                        self.root.after(600, self.draw_chip, self.game.game_move(0,0))
                        self.root.after(601, self.handle_draw, self.game.board.is_draw())
                        # self.draw_chip(self.game.game_move(0,0)) #DEBUG: Without delay
                        # self.handle_draw(self.game.board.is_draw())
    def handle_draw(self, draw):
        if draw:
            self.display_draw()
    
        
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
        if type(self.player1) == Player:
            name = simpledialog.askstring("Input", "P1 enter your name: (1-7)", parent=self.root)
            if name is None: return
            self.player1.name = name[:7]
        if type(self.player2) == Player:
            name = simpledialog.askstring("Input", "P2 enter your name: (1-7)", parent=self.root)
            if name == None: return
            self.player2.name = name[:7]
        self.game = Game(Board(self.m, self.n, self.k), self.player1, self.player2)
        self.slider_frame.destroy()
        self.play_button.destroy()
        self.selection_frame.destroy()
        self.draw_grid()
        self.game_started = True
        self.stats_canvas = tk.Canvas(self.stats_frame, width=347, height=399, bg="#434343", highlightthickness=0)
        self.stats_canvas.pack()
        self.stats_canvas.create_rectangle(35, 35, 311, 190, fill="#393939")
        self.stats_canvas.create_rectangle(35, 208, 311, 363, fill="#393939")
        self.stats_canvas.create_image(0, 0, image=self.images[1], anchor="nw")
        p1_frame = tk.Frame(self.stats_frame, bg="#393939")
        player1_label = tk.Label(p1_frame, text=self.player1.name, font=("TR2N", 40), bg="#393939", fg="white")
        player1_label.pack()
        player1_chip = tk.Label(p1_frame, image=self.images[5], bg="#393939")
        player1_chip.pack(side="bottom")
        p1_frame.place(x=175, y=110, anchor="center")
        p2_frame = tk.Frame(self.stats_frame, bg="#393939")
        player2_label = tk.Label(p2_frame, text=self.player2.name, font=("TR2N", 40), bg="#393939", fg="white")
        player2_label.pack()
        player2_chip = tk.Label(p2_frame, image=self.images[4], bg="#393939")
        player2_chip.pack(side="bottom")
        p2_frame.place(x=175, y=282, anchor="center")
        if type(self.player1) != Player and type(self.player2) != Player:
            self.bot_battle()
        elif type(self.player1) != Player:
            self.game_frame.after(100, self.draw_chip, self.game.game_move(0,0))
        
    def bot_battle(self):
        if self.game.is_bot():
            self.draw_chip(self.game.game_move(0,0))
        if winner:=self.game.board.has_won():
            self.root.after(600, self.display_win, winner-1) # winner-1 is basically is_red?
        elif self.game.board.is_draw():
            self.game_frame.after(600, self.display_draw())
        else: self.game_frame.after(600, self.bot_battle)
    
    def create_button(self, frame, bg, image, name, command=None):
        temp_btn = tk.Button(frame, command=command, bg=bg, bd=0, image=image, name=name)
        temp_btn.bind('<Enter>', self.on_enter)
        temp_btn.bind('<Leave>', self.on_leave)
        return temp_btn
    
    def draw_gamemode_buttons(self):
        OFFSET = 28
        BTN_SIZE = 75
        PADDING = 18
        def create_gmbtn(name):
            return self.create_button(self.selection_frame, bg="#393939", image=self.icons[name[-1]], name=name)
        
        for i in range(self.BUTTON_COUNT*2):
            tmp_btn = create_gmbtn(f"{(i//self.BUTTON_COUNT)+1}-{i%self.BUTTON_COUNT}")
            tmp_btn.place(x=OFFSET+((i%3)*(BTN_SIZE+PADDING)),y=OFFSET+(i//3)*BTN_SIZE+((i//self.BUTTON_COUNT)*32))
            tmp_btn.bind("<1>", self.change_gamemode)
            if i==5:
                self.button_toggle1 = tmp_btn
                tmp_btn.configure(image=self.icons_active[tmp_btn._name[-1]])
            elif i==11:
                self.button_toggle2 = tmp_btn
                tmp_btn.configure(image=self.icons_active[tmp_btn._name[-1]])
            self.btn_lst.append(tmp_btn)
        
        
    def draw_pre_frames(self):
        self.game_frame = tk.Frame(self.root, bg="#434343")
        self.game_frame.pack(padx=64, pady=64, side="left", fill="both")

        self.stats_frame = tk.Frame(self.root, bg="#434343")
        self.stats_frame.pack(padx=20, pady=64, side="right", fill="both")
        
        self.slider_frame = tk.Frame(self.stats_frame, bg="#434343")
        self.slider_frame.pack(padx=20, pady=10, side="top", fill="x")
        self.selection_frame = tk.Frame(self.stats_frame, bg="#434343")
        self.selection_frame.pack(side="top", fill="x")
                        
    def draw_game(self):
        self.game_canvas = tk.Canvas(self.game_frame, width=472, height=472, bg="#434343", highlightthickness=0)
        self.game_canvas.pack()
        self.game_canvas.create_rectangle(35, 35, 436, 436, fill="#393939")
        self.game_canvas.create_image(0, 0, image=self.images[0], anchor="nw")
        self.play_button = self.create_button(self.game_frame, command=self.press_play, bg="#434343", image=self.icons["6"], name="6")
        self.play_button.pack(side="top")
        
        self.stats_canvas = tk.Canvas(self.selection_frame, width=347, height=399, bg="#434343", highlightthickness=0)
        self.stats_canvas.pack()
        self.m_slide = ttk.Scale(self.slider_frame, from_=2, to=10, orient=tk.HORIZONTAL, style="custom.Horizontal.TScale", length=200, value=5, command=self.scale_change_m)
        self.n_slide = ttk.Scale(self.slider_frame, from_=2, to=10, orient=tk.HORIZONTAL, style="custom.Horizontal.TScale", length=200, value=5, command=self.scale_change_n)
        self.k_slide = ttk.Scale(self.slider_frame, from_=2, to=5, orient=tk.HORIZONTAL, style="custom.Horizontal.TScale", length=200, value=4, command=self.scale_change_k)
        self.m_slide.pack()
        self.n_slide.pack()
        self.k_slide.pack()
        self.stats_canvas.create_image(0, 0, image=self.images[13], anchor="nw")
        
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
        if event.widget != self.button_toggle1 and event.widget != self.button_toggle2:
            event.widget.config(image=self.icons[event.widget._name[-1]])
    def on_enter(self, event: tk.Event):
        event.widget.config(image=self.icons_active[event.widget._name[-1]])
        
    def change_gamemode(self,event: tk.Event): #PROOF OF CONCEPT
        modes = {"1-0": Bot(1),"1-1": Bot1(1), "1-2": Bot2(1), "1-3": Bot2(1), "1-4": Bot2(1), "1-5": Player("<p1>", 1),
                 "2-0": Bot(2),"2-1": Bot1(2), "2-2": Bot2(2), "2-3": Bot2(2), "2-4": Bot2(2), "2-5": Player("<p2>", 2)}
        if event.widget._name[0] == "1":
            self.player1 = modes[event.widget._name]
        elif event.widget._name[0] == "2":
            self.player2 = modes[event.widget._name]
        for btn in self.btn_lst:
            btn.configure(image=self.icons[btn._name[-1]]) if btn._name[0] == event.widget._name[0] else None
        self.button_toggle1 = event.widget

        event.widget.configure(image=self.icons_active[event.widget._name[-1]])
                        
    def draw_grid(self):
        self.cartesian = []
        self.draw_rows()
        self.draw_cols()
        for y,x in it.product(self.vertical_coords, self.horizontal_coords):
            self.cartesian.append((x,y))
            
    def draw_cols(self):
        self.horizontal_coords = []
        self.delete_cols()
        for i in range(1, self.m + 1):
            x = (400/(self.m + 1)) * i  + 29
            self.game_canvas.create_image(x, 36, image=self.images[3], anchor="nw", tags="col")
            self.horizontal_coords.append(x)
    def draw_rows(self):
        self.vertical_coords = []
        self.delete_rows()
        for i in range(1, self.n + 1):
            y = (400/(self.n + 1)) * i  + 29
            self.game_canvas.create_image(36, y, image=self.images[2], anchor="nw", tags="row")
            self.vertical_coords.append(y)
            
    def toggle_block(self):
        self.move_blocked = not self.move_blocked
        
    def display_draw(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.end_canvas = tk.Canvas(self.root, bg="#434343")
        self.end_canvas.pack(fill="both", expand=1)
        x = self.root.winfo_width()/2
        y = self.root.winfo_height()/2
        self.end_canvas.create_text(x, y, font=("TR2N",62), text="DRAW", fill="white", anchor="center")
        reset_btn = self.create_button(self.root, bg="#434343", image=self.icons["7"], name="7")
        reset_btn.place(x=x,y=y*2-100,anchor="center")
        reset_btn.bind("<1>", self.reset)
        
            
    def display_win(self, player):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.end_canvas = tk.Canvas(self.root, bg="#434343")
        self.end_canvas.pack(fill="both", expand=1)
        winner_img, winner_txt = (self.images[6], self.game.player1.name) if not player else (self.images[7], self.game.player2.name)
        self.end_canvas.create_image(0, 0, image=winner_img, anchor="nw")
        self.end_canvas.create_text(263, 295, font=("TR2N",62), text=winner_txt, fill="white")
        reset_btn = self.create_button(self.root, bg="#434343", image=self.icons["7"], name="7")
        x = self.root.winfo_width()/2
        y = self.root.winfo_height() -100
        reset_btn.place(x=x, y=y, anchor="center")
        reset_btn.bind("<1>", self.reset)
        
    def reset(self, event):
        self.end_canvas.destroy()
        event.widget.destroy()
        self.draw_pre_frames()
        self.m = 5
        self.n = 5
        self.k = 4
        self.draw_slider()
        self.draw_game()
        self.draw_grid()
        self.draw_gamemode_buttons()
        self.playersturn = True
                
        
    def debug(self, event):
        lsst = [btn._name for btn in self.btn_lst]
        print(lsst)
        
        
if __name__ == "__main__":
    GUI()