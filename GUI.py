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
        """
        Initializes the game by setting up the necessary attributes and creating the game window.
        """
        self.paths = [r"images\LightBig.png", r"images\LightSmall.png", r"images\stick-hori.png", r"images\stick.png",
                    r"images\circle_red.png", r"images\circle_blue.png", r"images\blue_won.png", r"images\red_won.png",
                    r"images\slider.png", r"images\slider_active.png", r"images\thru.png", r"images\button_case.png",
                    r"images\button_case_active.png", r"images\light_small_alt.png", r"images\MNKLogo.ico", r"images\#.png", r"images\#_active.png"]
        # Check if running on Windows if so use pyglet font
        if platform.system() == "Windows":
            import pyglet
            pyglet.options['win32_gdi_font'] = True # Necessary for tkinter quirk
            pyglet.font.add_file(r'font\Tr2n.ttf')
        else:
            for idx, path in enumerate(self.paths):
                self.paths[idx] = path.replace("\\", "/")
        # Attributes
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
        # Selection Menu
        self.button_toggle1 = None
        self.button_toggle2 = None
        self.player1 = Player("<p>",1)
        self.player2 = Player("<p>",2)
        # Draw the first frame
        self.draw_pre_frames()
        # Load images
        self.images = [tk.PhotoImage(file=path) for path in self.paths[:-3]]
        self.icons = {str(i): tk.PhotoImage(file=self.paths[-2].replace('#', str(i))) for i in range(8)}
        self.icons_active = {str(i): tk.PhotoImage(file=self.paths[-1].replace('#', str(i))) for i in range(8)}
        # Bind events
        self.root.bind("<1>", self.handle_click)
        # Styles
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
        # Default values
        self.m = 5
        self.n = 5
        self.k = 4
        # Draw the game for selection purposes
        self.draw_slider()
        self.draw_game()
        self.draw_grid()
        self.draw_gamemode_buttons()
        self.playersturn = True
        # Window icon
        self.root.iconbitmap(self.paths[-3])
        # Main loop needed for tkinter to work
        self.root.mainloop()
        
    def delete_rows(self):
        """
        Deletes all the rows in the game canvas by removing the "row" items.
        Returns:
            None
        """
        self.game_canvas.delete("row")
        self.vertical_coords = []
    def delete_cols(self):
        """
        Deletes the columns in the game canvas.
        Returns:
            None
        """
        self.game_canvas.delete("col")
        self.horizontal_coords=[]
    
    def is_in_between(self, a,b,c):
        """
        Checks if a value `a` is between two other values `b` and `c`.

        Parameters:
            a (Any): The value to check.
            b (Any): The lower bound.
            c (Any): The upper bound.

        Returns:
            bool: True if `a` is between `b` and `c`, False otherwise.
        """
        return b <= a <= c
    
    def on_grid(self, event: tk.Event, i: tuple):
        """
        Check if the given event occurs on a specific grid cell.

        Parameters:
            event (tk.Event): The event to check.
            i (tuple): The coordinates of the grid cell (crossing).

        Returns:
            bool: True if the event occurs on the grid cell, False otherwise.
        """
        radius = 20
        return self.is_in_between(event.x, i[0]-7, i[0]+radius) and self.is_in_between(event.y, i[1]-7, i[1]+radius)
    
    def draw_chip(self, results):
        """
        Draws a chip on the game canvas based on the given results.

        Parameters:
            results (list): A list containing the following information:
                - results[0] (bool): Indicates if the chip should be drawn. True meaning the move was valid.
                - results[1] (bool): Indicates which image (blue/red) should be used to draw the chip.
                - results[2] (tuple): Contains the x and y coordinates of the chip on the grid (not the canvas coordinates).

        Returns:
            None
        """
        if results[0]:
            n = (results[2][1])*self.m + results[2][0]
            i = self.cartesian[n]
            self.game_canvas.create_image(i[0]-22, i[1]-22, image=self.images[5] if results[1] else self.images[4], anchor="nw")

    def handle_click(self, event: tk.Event):
        """
        Handle the click event in game. E.g. if the player clicks on a grid cell, call the game's game_move function.

        Parameters:
            event (tk.Event): The click event object.

        Returns:
            None
        """
        if self.game_started and event.widget == self.game_canvas and not self.move_blocked:
            for idx, i in enumerate(self.cartesian):
                if self.on_grid(event, i):
                    results = self.game.game_move(m=idx % self.m, n=idx//self.m)
                    self.move_blocked = True
                    self.draw_chip(results)
                    self.root.after(200, self.toggle_block)
                    self.handle_win(self.game.board.has_won())
                    if self.game.board.is_draw():
                        self.display_draw()
                    elif self.game.is_bot():
                        self.root.after(600, self.draw_chip, self.game.game_move(0,0))
                        self.root.after(601, self.handle_draw, self.game.board.is_draw())
                        self.root.after(601, self.handle_win, self.game.board.has_won())
                        # self.draw_chip(self.game.game_move(0,0)) #DEBUG: Without delay
                        # self.handle_draw(self.game.board.is_draw())
    def handle_win(self, winner):
        if winner:
            self.root.after(1200, self.display_win, winner-1) # winner-1 is basically is_red?
    
    def handle_draw(self, is_draw):
        """
        If the game is a draw, display the draw screen. 
        
        Parameters:
            is_draw (bool): A boolean indicating if the game ended in a draw.
        
        Returns:
            None
        """
        if is_draw:
            self.display_draw()
    
        
    def scale_change_m(self, valstr):
        """
        Delete the columns, get correct value from valstring (need to cast to float then to int),
        update self.m and self.slider_label_m accordingly, and redraw the columns.
        
        Edge case: k is now larger than either m or n then update self.k and self.slider_label_k and configure the self.k_slide accordingly

        Parameters:
            valstr (str): The string representation of the value to be scaled.

        Returns:
            None
        """
        self.delete_cols()
        val = int(float(valstr))
        self.m = val
        self.slider_label_m.configure(text=val)
        max_k = self.m if self.m > self.n else self.n
        self.k_slide.configure(to=max_k)
        if max_k < self.k_slide.get():
            self.k_slide.set(max_k)
            self.slider_label_k.configure(text=int(max_k))
        self.draw_cols()
    
    def scale_change_n(self, valstr):
        """
        Delete the rows, get correct value from valstring (need to cast to float then to int),
        update self.n and self.slider_label_n accordingly, and redraw the rows.
        #Edge case: k is now larger than either m or n then update self.k and self.slider_label_k and configure the self.k_slide accordingly.

        Parameters:
            valstr (str): The input value as a string.

        Returns:
            None
        """
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
        """
        Set the value of self.k to the value that is passed in by tkinter scale.
        Passes a str, therefore need to cast to float to int.

        Parameters:
            valstr (str): A string representing a floating-point number.

        Returns:
            None
        """
        val = int(float(valstr))
        self.k = val
        self.slider_label_k.configure(text=val)
        

        
    def press_play(self):
        """
        Presses play and starts the game.

        This method prompts the players to enter their names using a dialog box.
        The names are then assigned to the respective players. If the names are
        longer than 7 characters, the players are prompted again to enter a name
        within the limit. The game is then initialized with the specified board
        dimensions and players. The slider frame, play button, and selection frame
        are destroyed and the grid is drawn. The game is set to started and the
        statistics canvas is created with the specified dimensions and background
        color. The canvas is divided into two rectangles with different fill colors.
        The player names are displayed along with their respective chips. If no
        player objects are provided, a bot battle is initiated. If only one player
        object is provided, a chip is drawn on the grid using the game move method.
        """
        if type(self.player1) == Player:
            name = simpledialog.askstring("Input", "P1 enter your name: (1-7)", parent=self.root)
            if name is None: return
            elif len(name) > 7:
                name = simpledialog.askstring("Input", "P1 name must be less than 7", parent=self.root)
            self.player1.name = name[:7]
        if type(self.player2) == Player:
            name = simpledialog.askstring("Input", "P2 enter your name: (1-7)", parent=self.root)
            if name == None: return
            elif len(name) > 7:
                name = simpledialog.askstring("Input", "P2 name must be less than 7", parent=self.root)
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
        """
        Executes a bot battle in the game.

        This method is responsible for executing a bot battle in the game. It first checks if the current player is a bot (it should never be not a bot but just in case).
        Using a parameter quirk where the param is executed before the draw_chip method itself, a game_move is mad with dummy values ((0, 0) just needed to fit in the criteria of the game class
        values will be ignored if the current player is bot).
        The move ist then drawn on the game canvas respectively with passing the return values of the game_move to the draw chip method.
        Checks if the game is won or drawn and draws the correct screen,
        if not method calls itself after 600ms. To simulate the bot "thinking"

        Parameters:
            self (object): The instance of the class.
        
        Returns:
            None
        """
        if self.game.is_bot():
            self.draw_chip(self.game.game_move(0,0))
        if winner:=self.game.board.has_won():
            self.root.after(600, self.display_win, winner-1) # winner-1 is basically is_red?
        elif self.game.board.is_draw():
            self.game_frame.after(600, self.display_draw())
        else: self.game_frame.after(600, self.bot_battle)
    
    def create_button(self, frame, bg, image, name, command=None):
        """
        Helper for creating button widget with custom hover effect. Too much of a hussle to make its own class.

        Parameters:
            frame (tk.Frame): The frame in which the button will be placed.
            bg (str): The background color of the button.
            image (tk.Image): The image to be displayed on the button.
            name (str): The name of the button.
            command (function, optional): The function to be executed when the button is pressed.

        Returns:
            tk.Button: The created button widget.
        """
        temp_btn = tk.Button(frame, command=command, bg=bg, bd=0, image=image, name=name)
        temp_btn.bind('<Enter>', self.on_enter)
        temp_btn.bind('<Leave>', self.on_leave)
        return temp_btn
    
    def draw_gamemode_buttons(self):
        """
        Draws the game mode buttons on the screen.

        This function creates and places the game mode buttons on the selection frame.
        It uses the `create_gmbtn` helper function to create each button and assigns the appropriate image and name.
        The buttons are placed on the screen using the `place` method.
        The `change_gamemode` method is bound to the left mouse click event of each button.
        The `button_toggle1` and `button_toggle2` variables are assigned the first 6 and the last 6 buttons respectively.
        The `image` property of these buttons is configured to use the corresponding active icon.
        Finally, the buttons are added to the `btn_lst` list.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """
        OFFSET = 28
        BTN_SIZE = 75
        PADDING = 18
        def create_gmbtn(name):
            """
            Helper for creating game buttons.
            
            Parameters:
                name (str): The name of the gamebtn.
            
            Returns:
                Button: The created gamebtn.
            """
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
        """
        Generates and displays the pre-frames for the game.

        This function creates and configures the game frame, stats frame, slider frame, and selection frame. It sets the background color of each frame to "#434343".
        The game frame is packed with a 64 pixels padding on both sides and a 64 pixels padding on the top and bottom.
        The stats frame is packed with a 64 pixels padding on both sides and a 20 pixels padding on the top and bottom.
        
        Returns:
        - None
        """
        self.game_frame = tk.Frame(self.root, bg="#434343")
        self.game_frame.pack(padx=64, pady=64, side="left", fill="both")

        self.stats_frame = tk.Frame(self.root, bg="#434343")
        self.stats_frame.pack(padx=20, pady=64, side="right", fill="both")

        self.slider_frame = tk.Frame(self.stats_frame, bg="#434343")
        self.slider_frame.pack(padx=20, pady=10, side="top", fill="x")
        self.selection_frame = tk.Frame(self.stats_frame, bg="#434343")
        self.selection_frame.pack(side="top", fill="x")
                        
    def draw_game(self):
        """
        Initializes and draws the game canvas, play button, and statistics canvas.
        
        Returns:
            None
        """
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
        """
        Draws a slider with labels for the values of 'm', 'n', and 'k'.

        Parameters:
            self (object): The instance of the class.
        
        Returns:
            None
        """
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
        """
        Set the image of the widget based on the event.widget.

        Parameters:
            event (Event): The event that fires when the mouse leaves the corresponding widget.
        """
        if event.widget != self.button_toggle1 and event.widget != self.button_toggle2:
            event.widget.config(image=self.icons[event.widget._name[-1]])
    def on_enter(self, event: tk.Event):
        """
        Sets the image of the widget based on the last character of its name. Sets it to the active icon (brighter border).

        Parameters:
            event (tk.Event): The event that fires when the mouse enters the corresponding widget.
        """
        event.widget.config(image=self.icons_active[event.widget._name[-1]])
        
    def change_gamemode(self,event: tk.Event): #PROOF OF CONCEPT
        """
        Change the gamemode based on the event.widget that called the function.
        
        Parameters:
            event (tk.Event): The event that triggered the function.
        """
        modes = {"1-0": Bot0(1),"1-1": Bot1(1), "1-2": Bot2(1), "1-3": Bot3(1), "1-4": Bot0(1), "1-5": Player("<p1>", 1),
                 "2-0": Bot0(2),"2-1": Bot1(2), "2-2": Bot2(2), "2-3": Bot3(2), "2-4": Bot0(2), "2-5": Player("<p2>", 2)}
        if event.widget._name[0] == "1":
            self.player1 = modes[event.widget._name]
        elif event.widget._name[0] == "2":
            self.player2 = modes[event.widget._name]
        for btn in self.btn_lst:
            btn.configure(image=self.icons[btn._name[-1]]) if btn._name[0] == event.widget._name[0] else None
        self.button_toggle1 = event.widget

        event.widget.configure(image=self.icons_active[event.widget._name[-1]])
                        
    def draw_grid(self):
        """
        Generate a grid by drawing rows and columns.
        
        This method is responsible for generating a grid by drawing rows and columns. It initializes the `cartesian` attribute as an empty list for future grid handling.
        It then calls the `draw_rows` and `draw_cols` methods to draw the rows and columns respectively. Finally, it uses the `it.product` function to iterate over
        the `vertical_coords` and `horizontal_coords` attributes using the cartesian product and appends each pair of coordinates to the `cartesian` list.
        
        Parameters:
            self (class): The instance of the class.
        """
        self.cartesian = []
        self.draw_rows()
        self.draw_cols()
        for y,x in it.product(self.vertical_coords, self.horizontal_coords):
            self.cartesian.append((x,y))
            
    def draw_cols(self):
        """
        Draws the columns on the game canvas.
        """
        self.horizontal_coords = []
        self.delete_cols()
        for i in range(1, self.m + 1):
            x = (400/(self.m + 1)) * i  + 29
            self.game_canvas.create_image(x, 36, image=self.images[3], anchor="nw", tags="col")
            self.horizontal_coords.append(x)
    def draw_rows(self):
        """
        Draws the rows on the game canvas.
        """
        self.vertical_coords = []
        self.delete_rows()
        for i in range(1, self.n + 1):
            y = (400/(self.n + 1)) * i  + 29
            self.game_canvas.create_image(36, y, image=self.images[2], anchor="nw", tags="row")
            self.vertical_coords.append(y)
            
    def toggle_block(self):
        """
        Toggles the value of the `move_blocked` attribute.
        """
        self.move_blocked = not self.move_blocked
        
    def display_draw(self):
        """
        Display and draw the canvas.

        This function destroys all the widgets in the root window, creates a new canvas,
        and displays the text "DRAW" in the center of the canvas. It also creates a reset button
        and binds the "reset" method to it.
        """
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
        """
        Display the winner of the game.

        Parameters:
            player: The player who won the game. It can be either player 1 or player 2.
        """
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
        """
        Resets the game to its initial state.

        Parameters:
            event: The event that triggered the reset. Passed automatically by Tkinter.

        Returns:
        None
        """
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