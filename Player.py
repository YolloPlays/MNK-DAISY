from Board import Board
class Player():
    def __init__(self, name: str, player_number: int):
        self.name = name
        self.player_number = player_number

    
    def make_move(self, board, m = None, n = None):
        while True:
            n = (int(input(f"{self.name}, bitte geben Sie die Zeile an: ")) - 1) \
                if n is None else n
            m = (int(input(f"{self.name}, bitte geben Sie die Spalte an: ")) - 1) \
                if m is None else m
            if 0 <= m < board.m and 0 <= n < board.n:
                if board.array[n, m] == 0: # <= Only necessary for raw input. GUI and Game handles this excption already
                    board.array[n, m] = self.player_number # Set methode im Board
                    return (m,n)
                else:
                    print('Dieser Punkt ist bereits besetzt!')
                    m = None
                    n = None
            else:
                print ("Diese Position ist außerhalb des Spielfelds.")
                m = None
                n = None
        
                
if __name__ == "__main__":
    # Aufruf der Methoden zum Spielen
    board = Board()
    player1 = Player("Klaus", 1)
    player1.make_move(board, 1 ,2)
    board.display()