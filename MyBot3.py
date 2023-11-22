from random import choice
from Player import Player
from Board import Board
from MyBot import Bot

class Bot(Player):
    def __init__(self):
        super().__init__("KI", 2)
        self.is_bot = True

    def make_move(self, board, m=None, n=None):
        # Check on board if human player has 2 or more in a row, col oder diag
        
        # Check empty cells on board
        empty_cells = []
        check_for = 2
        
        
        for col in range(board.m):
            for row in range(board.n):
                empty_cells.append((row,col)) if board.array[row][col] == 0 else None
        
    
        # TODO add offense to Bot
        
        smaller_dimension = min(board.m, board.n)
        
        
        
        
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
        

        
        # Randomly select a cell to place the disc
        m, n = choice(cells_to_set)
        return super().make_move(board, m, n)

    
    
    def find_center_points(self, board):
        """Based on the dimensions of and type of the dimensions (even/uneven) of the board the function calculates the most inner
        ring of points. In the case of board.m and board.n being even the board just has one point in the most inner ring

        Args:
            board (Board): board-Object

        Returns:
            list(Tuple): List of tuples with (n, m)
        """
        if board.m % 2 != 0 and board.n % 2 != 0: # m and n uneven
            points_in_row_1 = [(board.n//2, board.m//2)]
        elif board.m % 2 == 0 and board.n % 2 == 0: # m and n even
            points_in_row_1 = [(board.n/2-1, board.m/2-1),(board.m/2, board.n/2-1),(board.n/2-1, board.m/2),(board.n/2, board.m/2)]
        elif board.m % 2 != 0 and board.n % 2 == 0: # m uneven,  n even
            points_in_row_1 = [(board.n/2-1, board.m//2),(board.n/2, board.m//2)]
        elif board.m % 2 == 0 and board.n % 2 != 0: # m even, n uneven
            points_in_row_1 = [(board.n//2, board.m/2-1),(board.n//2, board.m/2)]
        
        return points_in_row_1


    def calculate_next_row(self, points: list):
        next_row = []
        for point in points:
            next_row_point = [(point[0]-1, point[1]),(point[0]-1, point[1]+1),(point[0], point[1]+1),(point[0]+1, point[1]+1), (point[0]+1, point[1]), (point[0]+1, point[1]-1), (point[0], point[1]-1), (point[0]-1, point[1]-1)] # Abfolge: oben, oben rechts, rechts, unten rechts
            next_row.extend(next_row_point)
        next_row = set(next_row)
        return next_row

    def calculate_number_of_circles(self, board):
        if board.m % 2 == 0 and board.n % 2 == 0:
            number_of_circles = min(board.m, board.n) # aufrunden
    
    
    
    def list_of_rows(self):
        center = self.find_center_points(board)
        
        pass

if __name__ == "__main__":

    board = Board(6,8)
    bot = Bot()
    middle = bot.find_center_points(board)
    print(middle)
    #print(bot.calculate_next_row(middle))
    
    