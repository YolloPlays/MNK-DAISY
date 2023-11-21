from random import choice
from Player import Player
from Board import Board

class Bot(Player):
    def __init__(self):
        super().__init__("KI", 2)

    def make_move(self, board, m=None, n=None):
        # Check on board if human player has 2 or more in a row, col oder diag
        
        # Check empty cells on board
        empty_cells = []
        check_for = 2
        
        
        for col in range(board.m):
            for row in range(board.n):
                empty_cells.append((row,col)) if board.array[row][col] == 0 else None
        
        #print(empty_cells)
        cells_to_set = []
        # Check horizontal for 2 in a row
        for row in range(board.n):
            for col in range(board.m - check_for+1):
                if all(board.array[row][col + i] == board.array[row][col] and board.array[row][col] == 1 for i in range(1, check_for)):
                    cells_to_set.append((row, col-1)) if (row, col-1) in empty_cells else None
                    cells_to_set.append((row, col+board.k-check_for)) if (row, col+board.k-check_for) in empty_cells else None
                        
        # Check vertical for 2 in a row
        for col in range(board.m):
            for row in range(board.n - check_for + 1):
                if all(board.array[row + i][col] == board.array[row][col] and board.array[row][col] == 1 for i in range(1, check_for)):
                    cells_to_set.append((row-1, col)) if (row, col-1) in empty_cells else None
                    cells_to_set.append((row+board.k-check_for, col)) if (row+board.k-check_for, col) in empty_cells else None
        
        
        # Check diagonal for 2 in a row
        for row in range(board.n - check_for + 1):
            for col in range(board.m - check_for + 1):
                if all(board.array[row + i][col + i] == board.array[row][col] and board.array[row][col] == 1 for i in range(1, check_for)):
                    cells_to_set.append((row-1, col-1)) if (row-1, col-1) in empty_cells else None
                    cells_to_set.append((row+board.k-check_for, col+board.k-check_for)) if (row+board.k-check_for, col+board.k-check_for) in empty_cells else None
        

        for row in range(board.n - check_for + 1):
            for col in range(check_for - 1, board.m):
                if all(board.array[row + i][col - i] == board.array[row][col] and board.array[row][col] == 1 for i in range(1, check_for)):
                    cells_to_set.append((row-1, col+1)) if (row-1, col+1) in empty_cells else None
                    cells_to_set.append((row+board.k-check_for, col-board.k+check_for)) if (row+board.k-check_for, col-board.k+check_for) in empty_cells else None
                    
        
        if len(cells_to_set) == 0:
            cells_to_set = empty_cells       
        
        
        
        
        # Randomly select a cell to place the disc
        m, n = choice(cells_to_set)
        return super().make_move(board, m, n)



if __name__ == "__main__":

    board = Board()
    board.array[0][0] = 1
    board.array[0][1] = 1
    board.array[0][2] = 1
    board.display()
    bot = Bot()
    print(bot.make_move(board))