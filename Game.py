import GUI, Board, Player, MyBot

class Game:
    def __init__(self, board:Board, player1:Player, player2 :Player  = MyBot.Bot()) -> None:
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.bot_game = isinstance(player2, MyBot.Bot)
        self.playerturn = True
        self.gui = None
    
    def game_move(self, m, n):
        # TODO handle real play and player change handle win check
        # print(m, n) # <= Reality: player move # Debug
        current_player_turn = self.playerturn
        current_player = self.player1 if current_player_turn else self.player2
        success = False
        chip_at=None
        if self.board.array[m][n] == 0:
            chip_at = current_player.make_move(self.board, m, n)
            success = True
            self.playerturn = not self.playerturn
        # self.board.display() # DEBUG
        # self.gui.display_win(False) # DEBUG
        return (success, current_player_turn, chip_at) # <= needed for gui to know whos players turn it was True: player1, False: player 2
        
        
        
if __name__ == "__main__":
    Game(Board.Board(3,6), Player.Player("Klaus", 1))