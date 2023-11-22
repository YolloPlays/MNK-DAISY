from random import choice
from Player import Player
from Board import Board

class Bot(Player):
    def __init__(self):
        super().__init__("KI", 2)
        self.is_bot = True

    def make_move(self, board, m=None, n=None):
        # Check on board if human player has 2 or more in a row, col oder diag
        
        # Check empty cells on board
        empty_cells = []
        for col in range(board.m):
            for row in range(board.n):
                empty_cells.append((row,col)) if board.array[row][col] == 0 else None

        
        check_for = 2
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
                    cells_to_set.append((row-1, col)) if (row-1, col) in empty_cells else None
                    cells_to_set.append((row+board.k-check_for, col)) if (row+board.k-check_for, col) in empty_cells else None
        
        
        # # Check diagonal for 2 in a row
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

        print(cells_to_set)
        # Randomly select a cell to place the disc from all cells or just cells nearby opponent
        n,m = choice(cells_to_set)
        print(f'Spalte {m+1} , Zeile {n+1}')
        return super().make_move(board, m, n)



if __name__ == "__main__":

    board = Board(3,5)
    board.display()
    #bot = Bot()
    #print(bot.make_move(board))