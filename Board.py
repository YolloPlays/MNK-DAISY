import numpy as np

class Board:
    def __init__(self, m: int = 5, n: int = 5, k: int = 4):
        self.m = m
        self.n = n
        self.k = k
        self.array = np.zeros((n, m))
    
    def display(self):
        print(self.array)
        print()
        
    def has_won(self):
        win = 0
        # Horizontal win
        for row in range(self.n):
            for col in range(self.m - self.k + 1):
                if all(self.array[row, col + i] == self.array[row, col] and self.array[row, col] == 1 for i in range(1, self.k)):
                    win = 1
                if all(self.array[row, col + i] == self.array[row, col] and self.array[row, col] == 2 for i in range(1, self.k)):
                    win = 2
        # Check columns
        for col in range(self.m):
            for row in range(self.n - self.k + 1):
                if all(self.array[row + i, col] == self.array[row, col] and self.array[row, col] == 1 for i in range(1, self.k)):
                    win = 1
                if all(self.array[row + i, col] == self.array[row, col] and self.array[row, col] == 2 for i in range(1, self.k)):
                    win = 2
        
        # Check diagonal
        for row in range(self.n - self.k + 1):
            for col in range(self.m - self.k + 1):
                if all(self.array[row + i, col + i] == self.array[row, col] and self.array[row, col] == 1 for i in range(1, self.k)):
                    win = 1
                if all(self.array[row + i, col + i] == self.array[row, col] and self.array[row, col] == 2 for i in range(1, self.k)):
                    win = 2

        for row in range(self.n - self.k + 1):
            for col in range(self.k - 1, self.m):
                if all(self.array[row + i, col - i] == self.array[row, col] and self.array[row, col] == 1 for i in range(1, self.k)):
                    win = 1
                if all(self.array[row + i, col - i] == self.array[row, col] and self.array[row, col] == 2 for i in range(1, self.k)):
                    win = 2
        
        return win

    def is_draw(self):
        def is_full():
            for row in range(self.n):
                for col in range(self.m):
                    if self.array[row, col] == 0:
                        return False
            return True
        return self.has_won() == 0 and is_full()
    
    def reset(self):
        self.array = np.zeros((self.n, self.m))
            
if __name__ == "__main__":
    board = Board(2,2,2)
    player = 2
    board.array[0, 0] = player
    board.array[1, 0] = player
    board.array[0, 1] = player
    board.array[1, 1] = player
    board.display()
    print(board.is_draw())