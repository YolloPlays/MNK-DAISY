from Board import Board
from Player import Player
from MyBot import *
from MyBot2 import *

class Game:
    def __init__(self, board:Board, player1:Player, player2 :Player  = Bot()) -> None:
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.bot_game = type(player2) != Player
        self.playerturn = True
        self.gui = None
        self.game_started = False
    
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
        if self.gui == None: # <= Backwards compatibility for raw input
            self.game_loop()
        
    def game_loop(self):
        while self.game_started and not self.board.has_won():
            player = self.player1 if self.playerturn else self.player2
            player.make_move(self.board)
            self.board.display()
            self.playerturn = not self.playerturn
        winner = self.player2 if self.board.has_won()-1 else self.player1
        print(f"{winner.name} has won")
            
        
        
if __name__ == "__main__":
    game = Game(Board(), Player("Klaus", 1))
    game.start()