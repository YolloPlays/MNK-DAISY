import numpy as np

class Board:
    def __init__(self, m: int = 5, n: int = 5, k: int = 4):
        self.m = m
        self.n = n
        self.k = k
        self.array = np.zeros((self.n, self.m))
    
    def display(self):
        print(self.array)
        
    def has_won(self):
        win = False
        # Horizontal win
        for row in range(self.n):
            for col in range(self.m - self.k + 1):
                if all(self.array[row][col + i] == self.array[row][col] and self.array[row][col] != 0 for i in range(1, self.k)):
                    win = True

        # Check columns
        for col in range(self.m):
            for row in range(self.n - self.k + 1):
                if all(self.array[row + i][col] == self.array[row][col] and self.array[row][col] != 0 for i in range(1, self.k)):
                    win = True
        
        # Check diagonal
        for row in range(self.n - self.k + 1):
            for col in range(self.m - self.k + 1):
                if all(self.array[row + i][col + i] == self.array[row][col] and self.array[row][col] != 0 for i in range(1, self.k)):
                    win = True

        for row in range(self.n - self.k + 1):
            for col in range(self.k - 1, self.m):
                if all(self.array[row + i][col - i] == self.array[row][col] and self.array[row][col] != 0 for i in range(1, self.k)):
                    win = True
        
        return win
