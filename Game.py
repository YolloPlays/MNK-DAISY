import GUI, Board, Player

class Game:
    def __init__(self, board:Board, player1:Player, player2:Player) -> None:
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.gui = GUI.GUI(self)
        
    def game_move(self, m, n):
        # TODO handle real play and player change
        print(m, n) # <= Reality do board manipulation
        return True # <= needed for gui to now whos players turn it was True: player1, False: player 2
        
        
        
if __name__ == "__main__":
    Game(Board.Board(), Player.Player("Klaus", 1), Player.Player("Peter", 1))