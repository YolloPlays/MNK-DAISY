import numpy as np

class Board:
    def __init__(self, m: int = 5, n: int = 5, k: int = 4):
        self.m = m
        self.n = n
        self.k = k
        self.array = np.zeros((self.m, self.n))
    
    def display(self):
        print(self.array)
        
    def has_won(self):
        # Horizontal win
        for row in range(self.m):
            if self.array[row][0] == self.array[row][1] == self.array[row][2] == self.array[row][3]\
                and (self.array[row][0] and self.array[row][1] and self.array[row][2] and self.array[row][3]) != 0:
                return True, f"col win in column {row+1}"
            if self.array[row][1] == self.array[row][2] == self.array[row][3] == self.array[row][4]\
                and (self.array[row][1] and self.array[row][2] and self.array[row][3] and self.array[row][4]) != 0:
                return True, f"col win in column {row+1}"
        
        # Vertical win
        for col in range(self.n):
            if self.array[0][col] == self.array[1][col] == self.array[2][col] == self.array[3][col]\
                and (self.array[0][col] and self.array[1][col] and self.array[2][col] and self.array[3][col]) != 0:
                return True, f"col win in column {col+1}"
            if self.array[1][col] == self.array[2][col] == self.array[row][3] == self.array[row][4]\
                and (self.array[1][col] and self.array[2][col] and self.array[3][col] and self.array[4][col]) != 0:
                return True, f"col win in column {col+1}"
        
        # Diagonal win
        for col in range(self.n-3):
            if self.array[col][col] == self.array[col+1][col+1] == self.array[col+2][col+2] == self.array[col+3][col+3]\
                and (self.array[col][col] and self.array[col+1][col+1] and self.array[col+2][col+2] and self.array[col+3][col+3]) != 0:
                return True, "diag win"
        for col in range(3, self.n):
            if self.array[col][col] == self.array[col-1][col-1] == self.array[col-2][col-2] == self.array[col-3][col-3] \
                and (self.array[col][col] and self.array[col-1][col-1] and self.array[col-2][col-2] and self.array[col-3][col-3]) != 0:
                return True, "diag win"
        
        return False
        
