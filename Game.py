import GUI, Board, Player

class Game:
    def __init__(self, board:Board, player1:Player, player2:Player) -> None:
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.playerturn = True
        GUI.GUI(self)
    
    def game_move(self, m, n):
        # TODO handle real play and player change handle win check
        # print(m, n) # <= Reality: player move # Debug
        current_player_turn = self.playerturn
        current_player = self.player1 if current_player_turn else self.player2
        success = False
        if self.board.array[m][n] == 0:
            current_player.make_move(self.board, m, n)
            success = True
            self.playerturn = not self.playerturn
        # self.board.display() # DEBUG
        self.gui.display_win(True) # DEBUG
        return (success, current_player_turn) # <= needed for gui to know whos players turn it was True: player1, False: player 2
        
        
        
if __name__ == "__main__":
    Game(Board.Board(), Player.Player("Klaus", 1), Player.Player("Peter", 2))