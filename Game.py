from Board import Board
from Player import Player
from MyBot import *
from MyAi import BotAI
import random as rr

class Game:
    def __init__(self, board:Board, player1:Player, player2:Player  = Bot(2), **kwargs) -> None:
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.shuffle = kwargs.get("shuffle")
        self.starting_player = bool(rr.getrandbits(1)) if self.shuffle else True
        self.playerturn = self.starting_player
        self.gui = False
        self.game_started = False
        self.should_log = kwargs.get("should_log") if kwargs.get("should_log") != None else False
        self.repeat = a if (a:=kwargs.get("repeat")) else 1
        self.should_print = kwargs.get("should_print") if kwargs.get("should_print") != None else True
        if self.should_log:
            try:
                with open("log.csv", "x") as f:
                    f.write("starting player,winning number\n")
            except Exception:
                print("File already created, beginning to append")
            self.f = open("log.csv", "a")
        
    def game_move(self, m, n):
        # TODO handle real play and player change handle win check
        # print(m, n) # <= Reality: player move # Debug
        current_player_turn = self.playerturn
        current_player = self.player1 if current_player_turn else self.player2
        success = False
        chip_at=None
        if self.board.array[n][m] == 0 or type(current_player) != Player:
            chip_at = current_player.make_move(self.board, m, n)
            success = True
            self.playerturn = not self.playerturn
        # self.board.display() # DEBUG
        # self.gui.display_win(False) # DEBUG
        return (success, current_player_turn, chip_at) # <= needed for gui to know whos players turn it was True: player1, False: player 2
    
    def is_bot(self):
        current_player = self.player1 if self.playerturn else self.player2
        return type(current_player) != Player
        
     
    def start(self):
        self.game_started = True
        if not self.gui: # <= Backwards compatibility for raw input
            self.game_loop()
        
    def game_loop(self):
        for i in range(self.repeat):
            while self.game_started and not self.board.has_won() and not self.board.is_draw():
                player = self.player1 if self.playerturn else self.player2
                player.make_move(self.board)
                self.board.display() if self.should_print else None
                self.playerturn = not self.playerturn
            if self.board.has_won():
                winner = self.player2 if self.board.has_won()-1 else self.player1
                print(f"{winner.name} has won") if self.should_print else None
                self.board.display() if self.should_print else None
                self.log(f"{int(not self.starting_player)+1},{winner.player_number}")
            else: 
                print("Full board! It's a draw") if self.should_print else None
                self.log(f"{int(not self.starting_player)+1},0")
            self.board.reset()
            if self.shuffle:
                self.starting_player = bool(rr.getrandbits(1))
                self.playerturn = self.starting_player
            print("\n\n\n\n\n") if self.should_print else None
        print(i) # <= Debug
    
    def log(self, string):
        if self.should_log:
            self.f.write(f"{string}\n")
        
if __name__ == "__main__":
    game = Game(Board(), Bot(1), Bot(2), should_log=True, repeat=10000, shuffle=True, should_print=False)
    game.start()