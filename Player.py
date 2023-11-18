from Board import Board
class Player(Board):
    def __init__(self, name: str, player_number: int, board):
        self.name = name
        self.player_number = player_number
        self.board = board

    
    def make_move(self):
        while True:
            m = int(input(f"{self.name}, bitte geben Sie die Zeile an: ")) - 1
            n = int(input(f"{self.name}, bitte geben Sie die Reihe an: ")) - 1
            if 0 <= m < self.board.m and 0 <= n < self.board.n:
                if self.board.array[m][n] == 0:
                    self.board.array[m][n] = self.player_number
                    return self.board.array[m][n]
                else:
                    print('Dieser Punkt ist bereits besetzt!')
            else:
                print ("Diese Position ist außerhalb des Spielfelds.")
                
# Aufruf der Methoden zum Spielen
board = Board()
player1 = Player("Klaus", 1, board)
player1.make_move()
board.display()