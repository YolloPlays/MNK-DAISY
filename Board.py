import numpy as np

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
        win = 0
        # Horizontal win or vertical win
        for row in range(self.n):
            for col in range(self.m - self.k + 1):
                if all(self.array[row, col + i] ==  1 or self.array.T[row, col + i] ==  1 for i in range(0, self.k)):
                    win = 1
                    break
                if all(self.array[row, col + i] ==  2 or self.array.T[row, col + i] ==  2 for i in range(0, self.k)):
                    win = 2
                    break
        
        # Check diagonal
        for row in range(self.n - self.k + 1):
            for col in range(self.m - self.k + 1):
                if all(self.array[row + i, col + i] ==  1 or self.array[row + i, col + self.k - 1 - i] == 1 for i in range(0, self.k)):
                    win = 1
                    break
                if all(self.array[row + i, col + i] ==  2 or self.array[row + i, col + self.k - 1 - i] == 2 for i in range(0, self.k)):
                    win = 2
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
    board = Board(5,5,4)
    player = 2
    board.array[1, 0] = player
    board.array[2, 1] = player
    board.array[3, 2] = player
    board.array[4, 3] = player
    board.display()
    print(board.has_won())