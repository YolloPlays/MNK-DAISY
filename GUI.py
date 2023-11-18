"""
 @author jabo
 @create date 18.11.2023
 @desc GUI for MNK
"""
import tkinter as tk
from faafo import Board # TODO. Replace with -import Board- for final merge
from PIL import Image,ImageTk

class GUI:
    
    def is_in_between(self, a,b,c):
        return b <= a <= c

    def handle_click(self, event: tk.Event):
        pass
    
    def draw_grid(self):
        for i in range(1, self.board.m + 1):
            x = (400/(self.board.m + 1)) * i  + 29
            self.game_canvas.create_image(x, 36, image=self.stick_img, anchor="nw")
        for i in range(1, self.board.m + 1):
            y = (400/(self.board.m + 1)) * i  + 29
            self.game_canvas.create_image(36, y, image=self.stick_hori_img, anchor="nw")
    
    def __init__(self, board: Board) -> None:
        self.board = board
        
        self.root = tk.Tk()
        self.root.title("MNK")
        self.root.configure(bg="#434343")
        self.root.geometry("1000x600")

        self.game_frame = tk.Frame(self.root, bg="#434343")
        self.game_frame.pack(padx=64, pady=64, side="left", fill="both")

        self.game_img = tk.PhotoImage(file="images\\LightBig.png")
        self.game_canvas = tk.Canvas(self.game_frame, width=472, height=472, bg="#434343", highlightthickness=0)
        self.game_canvas.pack()
        self.game_canvas.create_rectangle(35, 35, 436, 436, fill="#393939")
        self.game_canvas.create_image(0, 0, image=self.game_img, anchor="nw")

        self.stats_frame = tk.Frame(self.root, bg="#434343")
        self.stats_frame.pack(padx=20, pady=64, side="right", fill="both")

        self.stats_img = tk.PhotoImage(file="images\\LightSmall.png")
        self.stats_canvas = tk.Canvas(self.stats_frame, width=347, height=399, bg="#434343", highlightthickness=0)
        self.stats_canvas.pack()
        self.stats_canvas.create_rectangle(35, 35, 311, 190, fill="#393939")
        self.stats_canvas.create_rectangle(35, 208, 311, 363, fill="#393939")
        self.stats_canvas.create_image(0, 0, image=self.stats_img, anchor="nw")
        
        self.stick_hori_img = tk.PhotoImage(file="images\\stick-hori.png")
        self.stick_img = tk.PhotoImage(file="images\\stick.png")
        
        self.draw_grid()

        self.root.bind("<1>", self.handle_click)

        self.root.mainloop()
        
if __name__ == "__main__":
    GUI(Board.Board())