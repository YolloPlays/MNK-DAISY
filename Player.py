from Board import Board
class Player():
    def __init__(self, name: str, player_number: int):
        self.name = name
        self.player_number = player_number

    
    def make_move(self, board, m = None, n = None):
        """
        A function to prompt the player to make a move on the board and update the board accordingly.

        Parameters:
            self: The object instance
            board: The game board
            m: The column index, default is None (needed for compatibility)
            n: The row index, default is None (needed for compatibility)

        Returns:
            A tuple representing the coordinates of the move (m, n)
        """
        while True:
            if n is None:
                try:
                    n = (int(input(f"{self.name}, bitte geben Sie die Zeile an: ")) - 1)
                except ValueError:
                    continue
            else: n
            if m is None:
                try:
                    m = (int(input(f"{self.name}, bitte geben Sie die Spalte an: ")) - 1)
                except ValueError:
                    continue
            else: m
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
    player1.make_move(board)
    board.display()