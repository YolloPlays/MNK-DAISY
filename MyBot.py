from random import choice, shuffle
from itertools import combinations
from Player import Player
from Board import Board
import numpy as np
from scipy.signal import convolve

class Bot0(Player):
    """
    Random Bot. Places randomly on free cells

    """
    def __init__(self, number):
        """
        Initialize the Bot as an instance of the Player Class

        Parameters:
            number (int): The player number of the bot.
        """
        super().__init__("KI"+str(number), number)

    def make_move(self, board, m=None, n=None):
        """
        Generates the next move for the bot

        Parameters:
            board (Board): The current game board.
            m (int, optional): Needed for compatibility.
            n (int, optional): Needed for compatibility.

        Returns:
            tuple: A tuple representing the row and column indices of the move to be made.

        This function generates a move for the current player by selecting a random empty cell on the board. 
        It first finds all the empty cells on the board and then randomly selects one of them. 
        The coordinates of the selected cell are returned as a tuple (n, m).
        """
        
        empty_board_cells = list(zip(*np.where(board.array == 0)))
        
        # Randomly select a cell to place the disc
        n, m = choice(empty_board_cells)
        return super().make_move(board, m, n)



class Bot1(Player):
    """
    Blocker bot. Reacts when opponent has two or more in a row, in a col or diagonal.

    """
    def __init__(self, number):
        """
        Initialize the Bot as an instance of the Player Class

        Parameters:
            number (int): The player number of the bot.
        """
        super().__init__("KI"+str(number), number)


    def make_move(self, board, m=None, n=None):
        """
        Generates the next move for the bot

        Parameters:
            board (Board): The current game board.
            m (int, optional): Needed for compatibility.
            n (int, optional): Needed for compatibility.

        Returns:
            tuple: A tuple representing the row and column indices of the move to be made.
            
        This function generates a move for the current player by checking if the opponent has 2 or more in a row, col or diag.
        If the opponent has 2 or more in a row, col or diag, the function will return will return all the coordinates of an empty cell to block the opponent.
        If the opponent does not have 2 or more in a row, col or diag, the function will return a random move on an empty cell.
        """
        
        # get all empty cells on the board
        empty_board_cells = list(zip(*np.where(board.array == 0)))
                
        # get the opponent number
        opponent = 1 if self.player_number == 2 else 2
        
        # Check on board if human player has 2 or more in a row, col oder diag
        cells_to_set = []
        for check_for in range(board.k-1,1,-1):
            # check horizontal 
            self._check_sequence(board, check_for, opponent, empty_board_cells, cells_to_set, 0, 1)
            # check vertical
            self._check_sequence(board, check_for, opponent, empty_board_cells, cells_to_set, 1, 0)
            # check main diagonal
            self._check_sequence(board, check_for, opponent, empty_board_cells, cells_to_set, 1, 1)
            # check anti diagonal
            self._check_sequence(board, check_for, opponent, empty_board_cells, cells_to_set, -1, 1)
            
            
            # if cells_to_set is not empty, break the loop
            if cells_to_set:
                break
        
        
        # if no cells were found to block the opponent, use all empty cells
        if not cells_to_set:
            cells_to_set = empty_board_cells       
            
        # Randomly select a cell to place the disc from all empty cells or just cells next to opponent
        n, m = choice(cells_to_set)
        
        return super().make_move(board, m, n)
    
    
    def _check_sequence(self, board: Board, check_for: int, player_number: int, empty_cells: list, cells_to_set: list, delta_row: int, delta_col: int):
        """
        Check if a sequence of consecutive cells is present on the board. If so add the previous 
        and next cells to the list of cells to set if they are empty.
        
        Parameters:
            board (Board): The game board.
            check_for (int): The number of consecutive cells to check for.
            player_number (int): The player number to check for.
            empty_cells (list): List of empty cells on the board.
            cells_to_set (list): List of cells to set for the bot.
            delta_row (int): The change in row direction to calculate the next or previous cell.
            delta_col (int): The change in column direction to calculate the next or previous cell.
            
        """
            
        for row in range(board.n - (check_for - 1) * delta_row):
            for col in range(board.m - (check_for - 1) * delta_col):
                # no other possibility was found besides continuing if the row is out of bounds, because the code wont run as intended otherwise
                if row >= board.n:
                    continue
                if all(board.array[row + i * delta_row, col + i * delta_col] == player_number for i in range(check_for)):
                    # calculate the previous and next cell
                    prev_cell = (row - delta_row, col - delta_col)
                    next_cell = (row + check_for * delta_row, col + check_for * delta_col)
                    
                    # check if prev cell to found series is empty and not already in the list of cells to set
                    if prev_cell in empty_cells and prev_cell not in cells_to_set:
                        cells_to_set.append(prev_cell)
                    # check if next cell to found series is empty and not already in the list of cells to set
                    if next_cell in empty_cells and next_cell not in cells_to_set:
                        cells_to_set.append(next_cell)



class Bot2(Player):
    """
    Blocker Bot with new features. 
    """
    def __init__(self, number):
        """
        Initialize the Bot as an instance of the Player Class

        Parameters:
            number (int): The player number of the bot.
        """
        super().__init__("KI"+str(number), number)


    def make_move(self, board, m=None, n=None):
        """
        Find the best move for the bot player on the given board.

        Parameters:
            board (Board): The current game board.
            m (int, optional): Needed for compatibility.
            n (int, optional): Needed for compatibility.

        Returns:
            tuple: The row and column numbers of the best move.
        
        This function generates a move for the current player by checking if the opponent has k-1 or more in a row, col or diag.
        It checks the number of x in a row descending from k-1 to 1. 
        If the opponent doex have x in a row it will break the loop. 
        It will enable to first block the opponent where it has higher numbers of x in a row.
        
        
        """
        
        # Check on board if human player has 2 or more in a row, col oder diag
        # Check empty cells on board
        empty_board_cells = self._find_empty_cells(board, should_add_ring = False)
       
        opponent = 1 if self.player_number == 2 else 2
        
        # cells to set represents the cells where the bot will place its disc
        cells_to_set = []
        
        # check if there is the need to block the opponent because it has at least k-2 in a row
        for check_for in range(board.k-1,board.k-2-1,-1):
            # check horizontal 
            self._check_sequence(board, check_for, opponent, empty_board_cells, cells_to_set, 0, 1)
            # check vertical
            self._check_sequence(board, check_for, opponent, empty_board_cells, cells_to_set, 1, 0)
            # check main diagonal
            self._check_sequence(board, check_for, opponent, empty_board_cells, cells_to_set, 1, 1)
            # check anti diagonal
            self._check_sequence(board, check_for, opponent, empty_board_cells, cells_to_set, -1, 1)
            
            # as soon as a cell is found, break. No need to check further because the sequence with the largest number of cells has been found
            if len(cells_to_set) > 0:
                break
        
        
        # sort the list of cells to set in descending order of distance to the edge
        cells_to_set.sort(reverse = True) if len(cells_to_set) > 0 else None
        
        # if no cells were found where the bot can block the opponent set in one of the empty cells
        # should_add_ring is set to True because all the empty cells are shuffled by ring later. Adding the ring for the empty cells in the _check_sequence method 
        # is not necessary and would make the code less readable
        
        if not cells_to_set:
            cells_to_set = self._find_empty_cells(board, should_add_ring = True)
        
        # shuffle the list of cells to set by ring. The list stays sorted by distance to the edge in descending order.
        cells_to_set = self._shuffle_by_ring(cells_to_set, board)
            
        # Choose row and col from the first entry of cells_to_set. Index 1 is the tuple containing the row and col.
        n, m = cells_to_set[0][1]
        
        return super().make_move(board, m, n)


    def _check_sequence(self, board: Board, check_for: int, player_number: int, empty_cells: list, cells_to_set: list, delta_row: int, delta_col: int):
            """
            Check if a sequence of consecutive cells is present on the board. If so add the previous 
            and next cells to the list of cells to set if they are empty.
            
            Parameters:
                board (Board): The game board.
                check_for (int): The number of consecutive cells to check for.
                player_number (int): The player number to check for.
                empty_cells (list): List of empty cells on the board.
                cells_to_set (list): List of cells to set for the bot.
                delta_row (int): The change in row direction to calculate the next or previous cell.
                delta_col (int): The change in column direction to calculate the next or previous cell.
                
            """
            
            for row in range(board.n - (check_for - 1) * delta_row):
                for col in range(board.m - (check_for - 1) * delta_col):
                    # no other possibility was found besides continuing if the row is out of bounds, because the code wont run as intended otherwise
                    if row >= board.n:
                        continue
                    if all(board.array[row + i * delta_row, col + i * delta_col] == player_number for i in range(check_for)):
                        # calculate the previous and next cell
                        prev_cell = (row - delta_row, col - delta_col)
                        next_cell = (row + check_for * delta_row, col + check_for * delta_col)
                      
                        # check if prev cell to found series is empty. The map function is used to extract the tuple which contains the cell from the cells_to_set
                        if prev_cell in empty_cells and prev_cell not in list(map(lambda x: x[1], cells_to_set)):
                            cells_to_set.append((self._distance_to_edge(*prev_cell, board), prev_cell))
                        # check if next cell to found series is empty. The map function is used to extract the tuple which contains the cell from the cells_to_set
                        if next_cell in empty_cells and next_cell not in list(map(lambda x: x[1], cells_to_set)):
                            cells_to_set.append((self._distance_to_edge(*next_cell, board), next_cell))
    

    
    def _find_empty_cells(self, board: Board, **kwargs) -> list:
        """
        Finds and returns a list of empty cells in the given board, sorted in descending order of distance to the edge.

        Parameters:
            board (Board): The board object representing the game board in the current state.
            **kwargs: Additional keyword arguments.
                should_add_ring (bool): Whether to add a ring to the list of empty cells. Default is False.

        Returns:
            empty_cells (list): A list of empty cells in the board, sorted in descending order of distance to the edge.
        """

        should_add_ring = kwargs.get("should_add_ring") if kwargs.get("should_add_ring") != None else False
        
        empty_cells = list(zip(*np.where(board.array == 0)))

        # make a list of tuples (distance, (row, col))
        ring_coords = [(self._distance_to_edge(row, col, board), (row, col)) for row, col in empty_cells]

        # sort the list in descending order of distance to edge
        ring_coords.sort(reverse=True)

        # keep the ring if should_add_ring is True: (distance, (row, col)) else remove the ring: (row, col)
        if should_add_ring:
            empty_cells_sorted = ring_coords
        else:
            # extract the coordinates from the sorted tuples
            empty_cells_sorted = [coords for _, coords in ring_coords]
        

        return empty_cells_sorted

     
    def _distance_to_edge(self, row, col, board):
        """function that calculates the distance to the edge of the board

        Parameters:
            row (int): row on board
            col (int): col on board
            board (Board): board object

        Returns:
            int: _distance_ to the edge of the board
            
        """
        distance = min(min(row, col), min(board.n-row-1, board.m-col-1))
        
        return distance
    
    
    def _calculate_number_of_rings(self, board: Board):
        '''
        Calculates the number of rings on the board
        '''
        min_dimension = min(board.n, board.m)
        if min_dimension % 2 == 0:
            num_rings = min_dimension // 2 + 1
        else:
            num_rings = min_dimension / 2
        
        return int(num_rings)
    
    
    def _shuffle_by_ring(self, cells: list, board: Board):
        """
        Shuffles the given cells by ring using the provided board.
        
        Parameters:
            cells (list): A list of cells to be shuffled.
            board (Board): The board object used to calculate the number of rings.
        
        Returns:
            list: The shuffled cells by ring
        """
        
        shuffled_cells = []
        num_rings = self._calculate_number_of_rings(board)
        for i in range(num_rings,-1,-1):
            cells_interim = []
            for cell in cells:
                if cell[0] == i:
                    cells_interim.append(cell)
                    shuffle(cells_interim)
            shuffled_cells.extend(cells_interim)
            
        return shuffled_cells
    
      
class Bot3(Player):
    
    def __init__(self, number):
        super().__init__("KI"+str(number), number)
        
    def make_move(self, board, m=None, n=None):
        """
        A method to make a move in the game board.

        Parameters:
            board: the game board
            m: the column index (Default is None, needed for compatibility)
            n: the row index (Default is None, needed for compatibility)

        Returns:
            Move on the game board as a player with the tuple (n, m)
        """
        
        opponent = 1 if self.player_number == 2 else 2
        
        empty_board_cells = self._find_empty_cells(board)

        cells_to_set = []
        
        #########################################################
        # check if bot has k-1 in a row to skip all further steps
        #########################################################
        
        # check horizontal 
        self._check_sequence(board, board.k-1, self.player_number, empty_board_cells, cells_to_set, 0, 1)
        # check vertical
        self._check_sequence(board, board.k-1, self.player_number, empty_board_cells, cells_to_set, 1, 0)
        # check main diagonal
        self._check_sequence(board, board.k-1, self.player_number, empty_board_cells, cells_to_set, 1, 1)
        # check anti diagonal
        self._check_sequence(board, board.k-1, self.player_number, empty_board_cells, cells_to_set, -1, 1)
        
        
        #####################################################################
        # DEFENSIVE MOVE
        #####################################################################
        
        if not cells_to_set: # empty list
            for check_for in range(board.k-1, 1, -1):
                # cells to set represents the cells that the bot hat determined to be valid for the next (good) move
                cells_to_set_vert, cells_to_set_hor, cells_to_set_diag_l_r, cells_to_set_diag_r_l = [], [], [], []
                
                #cells_to_set = []
                self._check_sequence(board, check_for, opponent, empty_board_cells, cells_to_set_vert, 1, 0)
                self._check_sequence(board, check_for, opponent, empty_board_cells, cells_to_set_hor, 0, 1)
                self._check_sequence(board, check_for, opponent, empty_board_cells, cells_to_set_diag_l_r, 1, 1)
                self._check_sequence(board, check_for, opponent, empty_board_cells, cells_to_set_diag_r_l, -1, 1)
                
                rows, cols, diags_l_r, diags_r_l = self._find_rows_for_k(empty_board_cells, opponent, board)
                
                
                # clean up cells_to_set, so that only the rows that are dangerous are left
                
                cells_to_set_hor, cells_to_set_vert, cells_to_set_diag_l_r, cells_to_set_diag_r_l = self._filter_cells(cells_to_set_hor, cells_to_set_vert, cells_to_set_diag_l_r, cells_to_set_diag_r_l, rows, cols, diags_l_r, diags_r_l)
                        
                cells_to_set = list(set(cells_to_set_vert + cells_to_set_hor + cells_to_set_diag_l_r + cells_to_set_diag_r_l))
                
                if cells_to_set: # if cells to set is populated, then break. Found the sequence with the greatest length
                    break
        
        
        #####################################################################
        # OFFENSIVE MOVE 
        #####################################################################
        
        
        if not cells_to_set: # empty list 
            for check_for in range(2,-1, -1):
                # cells to set represent the cells that the bot hat determined to be valid for the next (good) move
                cells_to_set_vert, cells_to_set_hor, cells_to_set_diag_l_r, cells_to_set_diag_r_l = [], [], [], []
                
                self._check_sequence(board, check_for, self.player_number, empty_board_cells, cells_to_set_vert, 1, 0)
                self._check_sequence(board, check_for, self.player_number, empty_board_cells, cells_to_set_hor, 0, 1)
                self._check_sequence(board, check_for, self.player_number, empty_board_cells, cells_to_set_diag_l_r, 1, 1)
                self._check_sequence(board, check_for, self.player_number, empty_board_cells, cells_to_set_diag_r_l, -1, 1)
                
                rows, cols, diags_l_r, diags_r_l = self._find_rows_for_k(empty_board_cells, self.player_number, board)
                
                # clean up cells_to_set, so that only the rows that are dagerous are left
                
                cells_to_set_hor, cells_to_set_vert, cells_to_set_diag_l_r, cells_to_set_diag_r_l = self._filter_cells(cells_to_set_hor, cells_to_set_vert, cells_to_set_diag_l_r, cells_to_set_diag_r_l, rows, cols, diags_l_r, diags_r_l)
                        
                cells_to_set = list(set(cells_to_set_vert + cells_to_set_hor + cells_to_set_diag_l_r + cells_to_set_diag_r_l))
                
                if cells_to_set:
                    break
            
        
        
        # sort the list of cells to set in descending order of distance to the edge
        cells_to_set.sort(reverse = True) if len(cells_to_set) > 0 else None
        
        # if no cells were found where the bot can block the opponent set in one of the empty cells
        # should_add_ring is set to True because all the empty cells are shuffled by ring later. Adding the ring for the empty cells in the _check_sequence method 
        # is not necessary and would make the code less readable
        
        
        if not cells_to_set:
            cells_to_set = self._find_empty_cells(board, should_add_ring = True)
        # shuffle the list of cells to set by ring. The list stays sorted by distance to the edge in descending order.
        cells_to_set = self._shuffle_by_ring(cells_to_set, board)
        
        
        # Choose row and col from the first entry of cells_to_set. Index 1 is the tuple containing the row and col.
        
        n, m = cells_to_set[0][1]
        
        return super().make_move(board, m, n)
       
     
    def _check_sequence(self, board: Board, check_for: int, player_number: int, empty_cells: list, cells_to_set: list, delta_row: int, delta_col: int):
            """
            Check if a sequence of consecutive cells is present on the board. If so add the previous 
            and next cells to the list of cells to set if they are empty.
            
            Parameters:
                board (Board): The game board.
                check_for (int): The number of consecutive cells to check for.
                player_number (int): The player number to check for.
                empty_cells (list): List of empty cells on the board.
                cells_to_set (list): List of cells to set for the bot.
                delta_row (int): The change in row direction to calculate the next or previous cell.
                delta_col (int): The change in column direction to calculate the next or previous cell.
                
            """
            
            
            for row in range(board.n - (check_for - 1) * delta_row):
                for col in range(board.m - (check_for - 1) * delta_col):
                    # no other possibility was found besides continuing if the row is out of bounds, because the code wont run as intended otherwise
                    if row >= board.n:
                        continue
                    if all(board.array[row + i * delta_row, col + i * delta_col] == player_number for i in range(check_for)):
                        # calculate the previous and next cell
                        prev_cell = (row - delta_row, col - delta_col)
                        next_cell = (row + check_for * delta_row, col + check_for * delta_col)
    
                        # check if prev cell to found series is empty. The map function is used to extract the tuple which contains the cell from the cells_to_set
                        if prev_cell in empty_cells and prev_cell not in list(map(lambda x: x[1], cells_to_set)):
                            cells_to_set.append((self._distance_to_edge(*prev_cell, board), prev_cell))
                        # check if next cell to found series is empty. The map function is used to extract the tuple which contains the cell from the cells_to_set
                        if next_cell in empty_cells and next_cell not in list(map(lambda x: x[1], cells_to_set)):
                            cells_to_set.append((self._distance_to_edge(*next_cell, board), next_cell))
     

        
    def _find_rows_for_k(self, empty_cells: list, player_number: int, board: Board):
        """
        Find rows, columns, and diagonals with the possibility of k in a row for a given player 
        i.e. places where there are k cells with either 0 or the player number in a row
        
        Parameters:
            empty_cells (list): List of empty cells on the board
            player_number (int): Number representing the player
        
        Returns:
            tuple: A tuple containing the rows, columns, and diagonal coordinates with the possibility of k in a row
        """

        # kernel for the convolution, length is determined by k
        kernel = np.ones(board.k)
        
        # The player has an opportunity if it is possible to get k in a row. We check that by searching the array for k in a row either number 0 or the player number.
        # This technique can be used for the offense or defense
        board_array = np.where((board.array == player_number) | (board.array == 0), 1, 0)
        
        # lists to store the rows, columns, and diagonals
        rows, cols, diags_l_r, diags_r_l = [], [], [], []
        
        # Fill the lists with the numbers of the rows or cols where it is possible to get k in a row
        # The list diags_l_r and diags_r_l are used to check the diagonals. The method differentiates to the rows and cols. For the diags we append all cells on
        # the diags to the list, which were found to be useful for getting k in a row.
        
        # check diagonally if k in a row is possible for the player with the given number
        for d in range(-board.n + board.k, board.m - board.k + 1):
            diag = np.diagonal(board_array, offset = d)
            if np.any(convolve(diag, kernel, mode = 'valid') == board.k):
                if d < 0:
                    diags_l_r.extend([(n - d, n) for n in range(min(board.n, board.m))])
                else:
                    diags_l_r.extend([(n, n + d) for n in range(min(board.n, board.m))])
                
                # make sure that only empty cells are able to be set
                for cell in diags_l_r:
                    if cell not in empty_cells:
                        diags_l_r.remove(cell)
            
            anti_diag = np.diagonal(np.fliplr(board_array), offset = d)
            if np.any(convolve(anti_diag, kernel, mode = 'valid') == board.k):
                if d < 0:
                    diags_r_l.extend([(n - d, m) for n, m in zip(range(board.n), range(board.m-1,-1,-1))])
                else:
                    diags_r_l.extend([(n, m + d) for n, m in zip(range(board.n), range(board.m-1,-1,-1))])
                
                # make sure that only empty cells are able to be set
                for cell in diags_l_r:
                    if cell not in empty_cells:
                        diags_l_r.remove(cell)

        # check all rows 
        for row in range(board.n):
            if np.any(convolve(board_array[row, :], kernel, mode = 'valid') == board.k):
                rows.append(row)
        
        # check all columns      
        for col in range(board.m):
            if np.any(convolve(board_array[: ,col], kernel, mode = 'valid') == board.k):
                cols.append(col)
        
        return rows, cols, diags_l_r, diags_r_l
        
    
    def _filter_cells(self, cells_to_set_hor, cells_to_set_vert, cells_to_set_diag_l_r, cells_to_set_diag_r_l, rows, cols, diags_l_r, diags_r_l):
        """
        Filters the input cells based on the specified criteria and returns the filtered cells for horizontal, vertical, and diagonal directions.

        Parameters:
        - cells_to_set_hor: List of cells to set horizontally.
        - cells_to_set_vert: List of cells to set vertically.
        - cells_to_set_diag_l_r: List of cells to set diagonally from left to right.
        - cells_to_set_diag_r_l: List of cells to set diagonally from right to left.
        - rows: List of rows with a opportunity for k in a row
        - cols: List of columns with a opportunity for k in a row
        - diags_l_r: List of cells with a opportunity for k in a row from left to right.
        - diags_r_l: List of cells with a opportunity for k in a row from right to left.

        Returns:
        - filtered_cells_hor: List of filtered cells for horizontal direction.
        - filtered_cells_vert: List of filtered cells for vertical direction.
        - filtered_cells_diag_l_r: List of filtered cells for diagonal direction from left to right.
        - filtered_cells_diag_r_l: List of filtered cells for diagonal direction from right to left.
        """
        
        filtered_cells_hor = [(ring, cell) for ring, cell in cells_to_set_hor if cell[0] in rows]
        filtered_cells_vert = [(ring, cell) for ring, cell in cells_to_set_vert if cell[1] in cols]
        filtered_cells_diag_l_r = [(ring, cell) for ring, cell in cells_to_set_diag_l_r if cell in diags_l_r]
        filtered_cells_diag_r_l = [(ring, cell) for ring, cell in cells_to_set_diag_r_l if cell in diags_r_l]

        return filtered_cells_hor, filtered_cells_vert, filtered_cells_diag_l_r, filtered_cells_diag_r_l     
    
    
    def _find_empty_cells(self, board: Board, **kwargs) -> list:
        """
        Finds and returns a list of empty cells in the given board, sorted in descending order of distance to the edge.

        Parameters:
            board (Board): The board object representing the game board in the current state.
            **kwargs: Additional keyword arguments.
                should_add_ring (bool): Whether to add a ring to the list of empty cells. Default is False.

        Returns:
            empty_cells (list): A list of empty cells in the board, sorted in descending order of distance to the edge.
        """

        should_add_ring = kwargs.get("should_add_ring") if kwargs.get("should_add_ring") != None else False
        
        empty_cells = list(zip(*np.where(board.array == 0)))

        # make a list of tuples (distance, (row, col))
        ring_coords = [(self._distance_to_edge(row, col, board), (row, col)) for row, col in empty_cells]

        # sort the list in descending order of distance to edge
        ring_coords.sort(reverse=True)

        # keep the ring if should_add_ring is True: (distance, (row, col)) else remove the ring: (row, col)
        if should_add_ring:
            empty_cells_sorted = ring_coords
        else:
            # extract the coordinates from the sorted tuples
            empty_cells_sorted = [coords for _, coords in ring_coords]
        

        return empty_cells_sorted   
    
    
    def _distance_to_edge(self, row: int, col: int, board: Board):
        """function that calculates the distance to the edge of the board

        Parameters:
            row (int): row on board
            col (int): col on board
            board (Board): board object

        Returns:
            int: _distance_ to the edge of the board
        """
        distance = min(min(row, col), min(board.n-row-1, board.m-col-1))
        
        return distance
    
    def _shuffle_by_ring(self, cells: list, board: Board):
        """
        Shuffles the given cells by ring using the provided board.
        
        Parameters:
            cells (list): A list of cells to be shuffled.
            board (Board): The board object used to calculate the number of rings.
        
        Returns:
            list: The shuffled cells by ring
        """
        
        shuffled_cells = []
        num_rings = self._calculate_number_of_rings(board)
        for i in range(num_rings,-1,-1):
            cells_interim = []
            for cell in cells:
                if cell[0] == i:
                    cells_interim.append(cell)
                    shuffle(cells_interim)
            shuffled_cells.extend(cells_interim)
            
        return shuffled_cells
    
    
    def _calculate_number_of_rings(self, board: Board):
        '''
        Calculates the number of rings on the board
        
        Parameters:
            board (Board): board object
        
        Returns:
            int: number of rings
        '''
        min_dimension = min(board.n, board.m)
        if min_dimension % 2 == 0:
            num_rings = min_dimension // 2 + 1
        else:
            num_rings = min_dimension / 2
        
        return int(num_rings)
    

if __name__ == "__main__":
    from Game import Game 
     
    game = Game(Board(5, 5, 4), Bot3(1), Bot3(2))
    game.start()

