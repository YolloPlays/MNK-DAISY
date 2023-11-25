from random import choice
from Player import Player
from Board import Board

class Bot(Player):
    """
    Random Bot. Places randomly on free cells

    """
    def __init__(self, number):
        super().__init__("KI", number)

    def make_move(self, board, m=None, n=None):
        """_summary_

        Returns:
            Tuple: (m,n)
        """
        empty_cells = []
        for col in range(board.m):
            for row in range(board.n):
                empty_cells.append((row,col)) if board.array[row, col] == 0 else None
        
        # Randomly select a cell to place the disc
        n, m = choice(empty_cells)
        return super().make_move(board, m, n)


class Bot1(Player):
    """
    Blocker bot. Reacts when opponent has two or more in a row, in a col or diagonal.

    """
    def __init__(self, number):
        super().__init__("KI", number)

    def make_move(self, board, m=None, n=None):
        # Check on board if human player has 2 or more in a row, col oder diag
        
        # Check empty cells on board
        empty_cells = []
        for col in range(board.m):
            for row in range(board.n):
                empty_cells.append((row,col)) if board.array[row, col] == 0 else None

        
        check_for = 2
        cells_to_set = []
        
        # Check horizontal for 2 in a row
        for row in range(board.n):
            for col in range(board.m - check_for+1):
                if all(board.array[row, col + i] == board.array[row, col] and board.array[row, col] == 1 for i in range(1, check_for)):
                    cells_to_set.append((row, col-1)) if (row, col-1) in empty_cells else None
                    cells_to_set.append((row, col+board.k-check_for)) if (row, col+board.k-check_for) in empty_cells else None
        
        
        # Check vertical for 2 in a row
        for col in range(board.m):
            for row in range(board.n - check_for + 1):
                if all(board.array[row + i, col] == board.array[row, col] and board.array[row, col] == 1 for i in range(1, check_for)):
                    cells_to_set.append((row-1, col)) if (row-1, col) in empty_cells else None
                    cells_to_set.append((row+board.k-check_for, col)) if (row+board.k-check_for, col) in empty_cells else None
        
        
        # # Check diagonal for 2 in a row
        for row in range(board.n - check_for + 1):
            for col in range(board.m - check_for + 1):
                if all(board.array[row + i, col + i] == board.array[row, col] and board.array[row, col] == 1 for i in range(1, check_for)):
                    cells_to_set.append((row-1, col-1)) if (row-1, col-1) in empty_cells else None
                    cells_to_set.append((row+board.k-check_for, col+board.k-check_for)) if (row+board.k-check_for, col+board.k-check_for) in empty_cells else None
        

        for row in range(board.n - check_for + 1):
            for col in range(check_for - 1, board.m):
                if all(board.array[row + i, col - i] == board.array[row, col] and board.array[row, col] == 1 for i in range(1, check_for)):
                    cells_to_set.append((row-1, col+1)) if (row-1, col+1) in empty_cells else None
                    cells_to_set.append((row+board.k-check_for, col-board.k+check_for)) if (row+board.k-check_for, col-board.k+check_for) in empty_cells else None
        
        if len(cells_to_set) == 0:
            cells_to_set = empty_cells       
            
        # Randomly select a cell to place the disc from all cells or just cells nearby opponent
        n,m = choice(cells_to_set)
        print(f'Spalte {m+1} , Zeile {n+1}')
        return super().make_move(board, m, n)


class Bot2(Player):
    """
    Blocker Bot with new features. 
    """
    def __init__(self, number):
        super().__init__("KI", number)

    def make_move(self, board, m=None, n=None):
        # Check on board if human player has 2 or more in a row, col oder diag
        # Check empty cells on board
        empty_cells = self.find_empty_cells(board)
        empty_cells_higher_prob = self.cells_increase_probability(empty_cells, board)
        check_for = 2
        
        
        cells_to_set = []
        # Check horizontal for 2 in a row
        for row in range(board.n):
            for col in range(board.m - check_for+1):
                if all(board.array[row, col + i] == board.array[row, col] and board.array[row, col] == 1 for i in range(1, check_for)):
                    cells_to_set.append((row, col-1)) if (row, col-1) in empty_cells else None
                    cells_to_set.append((row, col+board.k-check_for)) if (row, col+board.k-check_for) in empty_cells else None
        
        
        # Check vertical for 2 in a row
        for col in range(board.m):
            for row in range(board.n - check_for + 1):
                if all(board.array[row + i, col] == board.array[row, col] and board.array[row, col] == 1 for i in range(1, check_for)):
                    cells_to_set.append((row-1, col)) if (row-1, col) in empty_cells else None
                    cells_to_set.append((row+board.k-check_for, col)) if (row+board.k-check_for, col) in empty_cells else None
        
        
        # Check diagonal for 2 in a row (left to right)
        for row in range(board.n - check_for + 1):
            for col in range(board.m - check_for + 1):
                if all(board.array[row + i, col + i] == board.array[row, col] and board.array[row, col] == 1 for i in range(1, check_for)):
                    cells_to_set.append((row-1, col-1)) if (row-1, col-1) in empty_cells else None
                    cells_to_set.append((row+board.k-check_for, col+board.k-check_for)) if (row+board.k-check_for, col+board.k-check_for) in empty_cells else None
        
        # Check diagonal for 2 in a row (right to left)
        for row in range(board.n - check_for + 1):
            for col in range(check_for - 1, board.m):
                if all(board.array[row + i, col - i] == board.array[row, col] and board.array[row, col] == 1 for i in range(1, check_for)):
                    cells_to_set.append((row-1, col+1)) if (row-1, col+1) in empty_cells else None
                    cells_to_set.append((row+board.k-check_for, col-board.k+check_for)) if (row+board.k-check_for, col-board.k+check_for) in empty_cells else None
        

        #  set_list consists of all cells that are both in empty_cells_higher_prob and cells_to_set
        # if the opponent has less than two in a row/ col or diag set_list is empty
        set_list = []
        for empty_cell in empty_cells_higher_prob:
            if empty_cell in cells_to_set:
                set_list.append(empty_cell) 
        
        
        # If set_list is empty the Bot chooses from all empty cells, but from the list with a higher probability
        # for the middle cells
        if len(set_list) == 0:
            set_list = empty_cells_higher_prob      
        
        print(set_list)
        # Randomly select a cell to place the disc
        n, m = choice(set_list)
        print(f'Spalte {m+1} , Zeile {n+1}')
        return super().make_move(board, m, n)

    
    def find_empty_cells(self, board):
        """function that locates the empty spots on the board

        Returns:
            list: list with tuples of empty cells in the format (n,m) = (row, col)
        """
        
        empty_cells = []
        for col in range(board.m):
                for row in range(board.n):
                    empty_cells.append((row,col)) if board.array[row, col] == 0 else None
        return empty_cells
    
    
    def cells_increase_probability(self, cells, board):
        """function that takes all the free cells on the board and appends them min(row+1/col+1) times to the list.
        This inceases the probability of the Bot placing a ring in the center of the field.

        Args:
            cells (list): free cells on the board

        Returns:
            list: list of free spots on the board. If the cell is closer to the middle of the board the cell will appear more
            frequent
        """
        
        cells_to_pick = []
        for cell in cells:
            row = min(min(cell[0], cell[1]), min(board.n-cell[0]-1, board.m-cell[1]-1))
            if row == 0:
                for _ in range(row+1):
                    cells_to_pick.append(cell)
            if row  == 1:
               for _ in range(row+1):
                    cells_to_pick.append(cell)
            if row  > 1:
               for _ in range(row+3):
                    cells_to_pick.append(cell)
        
        return cells_to_pick
        



if __name__ == "__main__":

    board = Board(6,6)
    board.array[2, 2] = 1
    board.array[1, 1] = 1
    bot = Bot2()
    bot.make_move(board)
    board.display()