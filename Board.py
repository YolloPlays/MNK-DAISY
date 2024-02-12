import numpy as np
from scipy.signal import convolve

class Board:
    def __init__(self, m: int = 5, n: int = 5, k: int = 4):
        """
        Initialize the class with default values for m, n, and k.
        
        Parameters:
            m (int): The value for the m parameter (default is 5).
            n (int): The value for the n parameter (default is 5).
            k (int): The value for the k parameter (default is 4).
        """
        self.m = m
        self.n = n
        self.k = k
        self.array = np.zeros((n, m))
    
    def display(self):
        """
        Method to display the content of the array.

        """
        print(self.array)
        print()
        
    def has_won(self):
        """
        Check if a player has won the game based on the current state of the board.

        Returns:
            int: The winning player (1 or 2), or 0 if no one has won --> draw or still in progress.
        """
        
        kernel = np.ones(self.k)
        win = 0
        for player in [1, 2]:
            player_array = np.where(self.array == player, 1, 0)
            
            # Horizontal win or vertical win
            for row in range(self.n):
                if np.any(convolve(player_array[row, :], kernel, mode = 'valid') == self.k):
                    win = player
                    break
            for col in range(self.m):
                if np.any(convolve(player_array[: ,col], kernel, mode = 'valid') == self.k):
                    win = player
                    break
                
            # Diagonal win
            # the value for d represents the offset from the main diagonal. negative values are below the main diagonal
            # they are dependent from the number of rows. Positive values are above the main diagonal 
            # and are dependent from the number of columns
            
            for d in range(-self.n + self.k, self.m - self.k + 1):
                diag = np.diagonal(player_array, offset = d)
                if np.any(convolve(diag, kernel, mode = 'valid') == self.k):
                    win = player
                    break
                anti_diag = np.diagonal(np.fliplr(player_array), offset = d)
                if np.any(convolve(anti_diag, kernel, mode = 'valid') == self.k):
                    win = player
                    break
                   
            
        return win

    def is_draw(self):
        """
        Check if the game is a draw by evaluating if the game has been won and the board is full.
        """
        def is_full():
            """
            Check if the entire 2D array is full, returns a boolean.
            """
            for row in range(self.n):
                for col in range(self.m):
                    if self.array[row, col] == 0:
                        return False
            return True
        return self.has_won() == 0 and is_full()
    
    def reset(self):
        """
        Resets the array attribute to a new numpy array of zeros with dimensions (n, m).
        """
        self.array = np.zeros((self.n, self.m))
        
if __name__ == "__main__":
    board = Board(4,4,4)
    player = 2
    
    board.array[0, 0] = 1
    board.array[1, 0] = 2
    board.array[2, 0] = 2
    board.array[3, 0] = 2
  

    
    
    board.array[0, 1] = 2
    board.array[1, 1] = 1
    board.array[2, 1] = 1
    board.array[3, 1] = 2
    
    board.array[0, 2] = 1
    board.array[1, 2] = 2
    board.array[2, 2] = 2
    board.array[3, 2] = 1
    
    board.array[0, 3] = 2
    board.array[1, 3] = 1
    board.array[2, 3] = 1
    board.array[3, 3] = 2
    board.display()
    print(board.has_won())