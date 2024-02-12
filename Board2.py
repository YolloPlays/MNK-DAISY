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
        
            
        def check_vert_hor(self, row: int, col: int, player: int):
            """
            Check if there are k consecutive occurrences of the player's number in the given row or column.

            Parameters:
            row (int): The row index to start checking from.
            col (int): The column index to start checking from.
            player (int): The player's number.
            
            Returns: 
            bool: True if there are k consecutive occurrences of the player's symbol in the given row or column, else False.
            """
            
            return all(self.array[row, col + i] ==  player or self.array.T[row, col + i] ==  player for i in range(0, self.k))
        
        
        def check_main_diagonal(self, row: int, col: int, player: int):
            """
            Check the main diagonal for a win for the given player.

            Parameters:
                row (int): The row index to start checking from.
                col (int): The column index to start checking from.
                player (int): The player's number.

            Returns:
                bool: True if there are k consecutive occurrences of the player's symbol on the main diagonal.
            """
            
            return all(self.array[row + j, col + j] == player  for j in range(self.k))


        def check_anti_diagonal(self, row: int, col: int, player: int):
            """
            Check the anti diagonal for a win for the given player.
            
            Parameters:
                row (int): The row index to start checking from.
                col (int): The column index to start checking from.
                player (int): The player's number.

            Returns:
                bool: True if there are k consecutive occurrences of the player's symbol on the main diagonal.
            """
            
            return all(np.fliplr(self.array)[row + i, col + i] == player for i in range(self.k))
        
        # initialize win to 0 --> no one has won
        win = 0
        
        # Horizontal win or vertical win
        for row in range(self.n):
            for col in range(self.m - self.k + 1):
                if check_vert_hor(self, row, col, 1) or check_vert_hor(self, row, col, 1):
                    win = 1
                    break
                if check_vert_hor(self, row, col, 2) or check_vert_hor(self, row, col, 2):
                    win = 2
                    break
                   
        # Check diagonal
        for row in range(self.n - self.k + 1):
            for col in range(self.m - self.k + 1): 
                if check_main_diagonal(self, row, col, 1) or check_anti_diagonal(self, row, col, 1):
                    win = 1
                    break
                if check_main_diagonal(self, row, col, 2) or check_anti_diagonal(self, row, col, 2):
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
    board.array[1, 1] = 2
    board.array[2, 2] = 2
    board.array[3, 3] = 2
    board.array[4, 4] = 2

    
    
    # board.array[0, 1] = 2
    # board.array[1, 1] = 1
    # board.array[2, 1] = 1
    # board.array[3, 1] = 2
    
    # board.array[0, 2] = 1
    # board.array[1, 2] = 2
    # board.array[2, 2] = 2
    # board.array[3, 2] = 1
    
    # board.array[0, 3] = 2
    # board.array[1, 3] = 1
    # board.array[2, 3] = 1
    # board.array[3, 3] = 2
    board.display()
    print(board.has_won())