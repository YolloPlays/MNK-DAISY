from random import choice, shuffle
from itertools import combinations
from Player import Player
from Board import Board

class Bot(Player):
    """
    Random Bot. Places randomly on free cells

    """
    def __init__(self, number):
        super().__init__("KI"+str(number), number)

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
        super().__init__("KI"+str(number), number)

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
                if all(board.array[row, col + i] ==  1 for i in range(0, check_for)):
                    cells_to_set.append((row, col-1)) if (row, col-1) in empty_cells else None
                    cells_to_set.append((row, col+check_for)) if (row, col+check_for) in empty_cells else None
        
        
        # Check vertical for 2 in a row
        for col in range(board.m):
            for row in range(board.n - check_for + 1):
                if all(board.array[row + i, col] ==  1 for i in range(0, check_for)):
                    cells_to_set.append((row-1, col)) if (row-1, col) in empty_cells else None
                    cells_to_set.append((row+check_for, col)) if (row+check_for, col) in empty_cells else None
        
        
        # # Check diagonal for 2 in a row
        for row in range(board.n - check_for + 1):
            for col in range(board.m - check_for + 1):
                if all(board.array[row + i, col + i] ==  1 for i in range(0, check_for)):
                    cells_to_set.append((row-1, col-1)) if (row-1, col-1) in empty_cells else None
                    cells_to_set.append((row+check_for, col+check_for)) if (row+check_for, col+check_for) in empty_cells else None
        

        for row in range(board.n - check_for + 1):
            for col in range(check_for - 1, board.m):
                if all(board.array[row + i, col - i] ==  1 for i in range(0, check_for)):
                    cells_to_set.append((row-1, col+1)) if (row-1, col+1) in empty_cells else None
                    cells_to_set.append((row+check_for, col-check_for)) if (row+check_for, col-check_for) in empty_cells else None
        
        if len(cells_to_set) == 0:
            cells_to_set = empty_cells       
            
        # Randomly select a cell to place the disc from all cells or just cells nearby opponent
        n,m = choice(cells_to_set)
        # print(f'Spalte {m+1} , Zeile {n+1}')
        return super().make_move(board, m, n)


class Bot2(Player):
    """
    Blocker Bot with new features. 
    """
    def __init__(self, number):
        super().__init__("KI"+str(number), number)

    def make_move(self, board, m=None, n=None):
        # Check on board if human player has 2 or more in a row, col oder diag
        # Check empty cells on board
        empty_cells = self.find_empty_cells(board)
        opponent = 1 if self.player_number == 2 else 2
    
        
        for check_for in range(board.k-1,1,-1):
            cells_to_set = []
            # Check horizontal for 2 in a row
            for row in range(board.n):
                for col in range(board.m - check_for + 1):
                    if all(board.array[row, col + i] == opponent for i in range(0, check_for)):
                        cells_to_set.append([self.distance_to_edge(row, col-1, board),(row, col-1)]) if [self.distance_to_edge(row, col-1, board),(row, col-1)] in empty_cells else None
                        cells_to_set.append([self.distance_to_edge(row, col + check_for, board),(row, col + check_for)]) \
                            if [self.distance_to_edge(row, col + check_for, board),(row, col + check_for)] in empty_cells else None
            
            
            
            # Check vertical for 2 in a row
            for col in range(board.m):
                for row in range(board.n - check_for + 1):
                    if all(board.array[row + i, col] ==  opponent for i in range(0, check_for)):
                        cells_to_set.append([self.distance_to_edge(row - 1, col, board),(row - 1, col)]) if [self.distance_to_edge(row - 1, col, board),(row - 1, col)] in empty_cells else None
                        cells_to_set.append([self.distance_to_edge(row + check_for, col, board),(row + check_for, col)]) \
                            if [self.distance_to_edge(row + check_for, col, board),(row + check_for, col)] in empty_cells else None
            
            
            # # Check diagonal for 2 in a row (left to right)
            for row in range(board.n - check_for + 1):
                for col in range(board.m - check_for + 1):
                    if all(board.array[row + i, col + i] ==  opponent for i in range(0, check_for)):
                        cells_to_set.append([self.distance_to_edge(row - 1, col -1, board),(row - 1, col -1 )]) if [self.distance_to_edge(row - 1, col -1, board),(row - 1, col -1)] in empty_cells else None
                        cells_to_set.append([self.distance_to_edge(row + check_for, col + check_for, board),(row + check_for, col + check_for)]) \
                            if [self.distance_to_edge(row + check_for, col + check_for, board),(row + check_for, col + check_for)] in empty_cells else None
            
            
            # # Check diagonal for 2 in a row (right to left)
            for row in range(board.n - check_for + 1):
                for col in range(check_for - 1, board.m):
                    if all(board.array[row + i, col - i] ==  opponent for i in range(0, check_for)):
                        cells_to_set.append([self.distance_to_edge(row - 1, col +1, board),(row - 1, col +1 )]) if [self.distance_to_edge(row - 1, col +1, board),(row - 1, col +1)] in empty_cells else None
                        cells_to_set.append([self.distance_to_edge(row + check_for, col - check_for, board),(row + check_for, col - check_for)]) \
                            if [self.distance_to_edge(row + check_for, col - check_for, board),(row + check_for, col - check_for)] in empty_cells else None
            
            
            if len(cells_to_set) > 0:
                break
          
            
            
            
            

        #print(set_list)
        cells_to_set.sort(reverse= True) if len(cells_to_set) > 0 else None
        #cells_to_set.reverse() if len(cells_to_set) > 0 else None
        
        print(cells_to_set)
        
        # If set_list is empty the Bot chooses from all empty cells, but from the list with a higher probability
        # for the middle cells
        if len(cells_to_set) == 0:
            cells_to_set = empty_cells
        
        
        # Choose row and col from the first entry of cells_to_set
        n, m = cells_to_set[0][1]
        #print(f'Spalte {m+1} , Zeile {n+1}')
        return super().make_move(board, m, n)

    
    def find_empty_cells(self, board):
        """function that locates the empty spots on the board

        Returns:
            tuple: list with tuples of empty cells in the format (ring ,(n,m)) = (row, col)
        """
        
        empty_cells = []
        for col in range(board.m):
                for row in range(board.n):
                    empty_cells.append([self.distance_to_edge(row, col, board),(row, col)]) if board.array[row, col] == 0 else None
                empty_cells.sort()
                empty_cells.reverse()
                    
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
        
    def distance_to_edge(self, row, col, board):
        """function that calculates the distance to the edge of the board

        Args:
            row (int): row on board
            col (int): col on board
            board (Board): board object

        Returns:
            int: _distance_ to the edge of the board
            
        """
        distance = min(min(row, col), min(board.n-row-1, board.m-col-1))
        
        return distance
        

class Bot3(Player):
    """
    Blocker Bot with new features. Also able to play offensive
    """
    def __init__(self, number):
        super().__init__("KI"+str(number), number)

    def make_move(self, board, m=None, n=None):
        # Check on board if human player has 2 or more in a row, col oder diag
        # Check empty cells on board
        empty_cells = self.find_empty_cells(board)
        opponent = 1 if self.player_number == 2 else 2

        # check how many cells the bot has on the board
        cells_to_test = []
        bot_cells = self.find_bot_cells(board)
        #print(bot_cells, '\n')
        
        # bot_in_row = 1
        # for i in range(board.k-1,1,-1):
        #     if bot_in_row > 1:
        #         break
        #     combinations_list = list(combinations(bot_cells, i))
        #     for combination in combinations_list:
                
        #         combination = sorted(combination, key=lambda x: x[1][1])
                
        #         if all(((combination[k][1][1])+k) == combination[0][1][1] and combination[0][1][0] == combination[k][1][0] for k in range(1,len(combination))):
        #             print('found', combination)
        #             bot_in_row = i
                
        #         if bot_in_row > 1:
        #             break
                
        #         combination = sorted(combination, key=lambda x: x[1][0])
                
        #         if all(((combination[k][1][0])+k) == combination[0][1][0] and combination[0][1][1] == combination[k][1][1] for k in range(1,len(combination))):
        #             print('found', combination)
        #             bot_in_row = i
                
        #         if bot_in_row > 1:
        #             break
                
        #         combination = sorted(combination, key=lambda x: (x[1][0],x[1][1]), reverse=True)
        #         print(combination)
        #         print('bird')
                
        #         if all((combination[0][1][1] == (combination[k][1][1])+k) for k in range(1,len(combination))):
        #             print('found', combination)
        #             bot_in_row = i

                    
                    
        
        # print('bot in row', bot_in_row)
        
        

        
        
        # self. check how many cells the bot has in a row
        
        for check_for in range(board.k-1,board.k-2,-1):
            cells_to_set = []
            # Check horizontal for board.k-1 in a row
            for row in range(board.n):
                for col in range(board.m - check_for + 1):
                    if all(board.array[row, col + i] == self.player_number for i in range(0, check_for)):
                        cells_to_set.append([self.distance_to_edge(row, col-1, board),(row, col-1)]) if [self.distance_to_edge(row, col-1, board),(row, col-1)] in empty_cells else None
                        cells_to_set.append([self.distance_to_edge(row, col + check_for, board),(row, col + check_for)]) \
                            if [self.distance_to_edge(row, col + check_for, board),(row, col + check_for)] in empty_cells else None

            
            # Check vertical for board.k-1 in a row
                for col in range(board.m):
                    for row in range(board.n - check_for + 1):
                        if all(board.array[row + i, col] ==  opponent for i in range(0, check_for)):
                            cells_to_set.append([self.distance_to_edge(row - 1, col, board),(row - 1, col)]) if [self.distance_to_edge(row - 1, col, board),(row - 1, col)] in empty_cells else None
                            cells_to_set.append([self.distance_to_edge(row + check_for, col, board),(row + check_for, col)]) \
                                if [self.distance_to_edge(row + check_for, col, board),(row + check_for, col)] in empty_cells else None
                
                
                # # Check diagonal for board.k-1 in a row (left to right)
                for row in range(board.n - check_for + 1):
                    for col in range(board.m - check_for + 1):
                        if all(board.array[row + i, col + i] ==  opponent for i in range(0, check_for)):
                            cells_to_set.append([self.distance_to_edge(row - 1, col -1, board),(row - 1, col -1 )]) if [self.distance_to_edge(row - 1, col -1, board),(row - 1, col -1)] in empty_cells else None
                            cells_to_set.append([self.distance_to_edge(row + check_for, col + check_for, board),(row + check_for, col + check_for)]) \
                                if [self.distance_to_edge(row + check_for, col + check_for, board),(row + check_for, col + check_for)] in empty_cells else None
                
                
                # # Check diagonal for board.k-1 in a row (right to left)
                for row in range(board.n - check_for + 1):
                    for col in range(check_for - 1, board.m):
                        if all(board.array[row + i, col - i] ==  opponent for i in range(0, check_for)):
                            cells_to_set.append([self.distance_to_edge(row - 1, col +1, board),(row - 1, col +1 )]) if [self.distance_to_edge(row - 1, col +1, board),(row - 1, col +1)] in empty_cells else None
                            cells_to_set.append([self.distance_to_edge(row + check_for, col - check_for, board),(row + check_for, col - check_for)]) \
                                if [self.distance_to_edge(row + check_for, col - check_for, board),(row + check_for, col - check_for)] in empty_cells else None
                
                
                
            #print('bot has k-1 in a row and can set in following cells to win',cells_to_set)
                
            # if len(cells_to_set) > 0:
            #     break
                

        # if bot has less than k-1 in a row so bot will check if it is possible to block the opponent
        
        if len(cells_to_set) == 0:
            for check_for in range(board.k-1,board.k-2-1,-1):
                cells_to_set = []
                # Check horizontal for board.k-1 
                for row in range(board.n):
                    for col in range(board.m - check_for + 1):
                        if all(board.array[row, col + i] == opponent for i in range(0, check_for)):
                            cells_to_set.append([self.distance_to_edge(row, col-1, board),(row, col-1)]) if [self.distance_to_edge(row, col-1, board),(row, col-1)] in empty_cells else None
                            cells_to_set.append([self.distance_to_edge(row, col + check_for, board),(row, col + check_for)]) \
                                if [self.distance_to_edge(row, col + check_for, board),(row, col + check_for)] in empty_cells else None
                
                
                
                # Check vertical for 2 in a row
                for col in range(board.m):
                    for row in range(board.n - check_for + 1):
                        if all(board.array[row + i, col] ==  opponent for i in range(0, check_for)):
                            cells_to_set.append([self.distance_to_edge(row - 1, col, board),(row - 1, col)]) if [self.distance_to_edge(row - 1, col, board),(row - 1, col)] in empty_cells else None
                            cells_to_set.append([self.distance_to_edge(row + check_for, col, board),(row + check_for, col)]) \
                                if [self.distance_to_edge(row + check_for, col, board),(row + check_for, col)] in empty_cells else None
                
                
                # # Check diagonal for 2 in a row (left to right)
                for row in range(board.n - check_for + 1):
                    for col in range(board.m - check_for + 1):
                        if all(board.array[row + i, col + i] ==  opponent for i in range(0, check_for)):
                            cells_to_set.append([self.distance_to_edge(row - 1, col -1, board),(row - 1, col -1 )]) if [self.distance_to_edge(row - 1, col -1, board),(row - 1, col -1)] in empty_cells else None
                            cells_to_set.append([self.distance_to_edge(row + check_for, col + check_for, board),(row + check_for, col + check_for)]) \
                                if [self.distance_to_edge(row + check_for, col + check_for, board),(row + check_for, col + check_for)] in empty_cells else None
                
                
                # # Check diagonal for 2 in a row (right to left)
                for row in range(board.n - check_for + 1):
                    for col in range(check_for - 1, board.m):
                        if all(board.array[row + i, col - i] ==  opponent for i in range(0, check_for)):
                            cells_to_set.append([self.distance_to_edge(row - 1, col +1, board),(row - 1, col +1 )]) if [self.distance_to_edge(row - 1, col +1, board),(row - 1, col +1)] in empty_cells else None
                            cells_to_set.append([self.distance_to_edge(row + check_for, col - check_for, board),(row + check_for, col - check_for)]) \
                                if [self.distance_to_edge(row + check_for, col - check_for, board),(row + check_for, col - check_for)] in empty_cells else None
                
                if len(cells_to_set) > 0:
                    break
        
        
        # Make Bot be offensive if there is nothing to block. Bot should look in empty cells, if there is a possiblity to get k in a row
        # Check horizontal if there is a possibility to get k in a row
        
        
        # Horizontal offensive move
        
        
        
        
        # check if there are k-1 set by the bot
        # horizontal
        
        # Horizontal offensive move - check for the bot's cells in a row
    
        
                    
            
                    
        if len(cells_to_set) == 0: 
            for row in range(board.n):
                for col in range(board.m - board.k + 1):
                    if all((board.array[row, col + i] == self.player_number) or (board.array[row, col + i] == 0) for i in range(0, board.k)):
                        for i in range(0, board.k):
                            cells_to_test.append([self.distance_to_edge(row, col+i, board),(row, col+i)]) if ([self.distance_to_edge(row, col+i, board),(row, col+i)] in empty_cells) else None
            
            print('test',cells_to_test)
            
            for cell_to_test in cells_to_test:
                if [cell_to_test[0], (cell_to_test[1][0], (cell_to_test[1][1])+1)] in bot_cells or [cell_to_test[0], (cell_to_test[1][0], (cell_to_test[1][1])-1)] in bot_cells:
                    if cells_to_test[i] not in cells_to_set:
                        cells_to_set.append(cells_to_test[i])
            
            # for i in range(len(cells_to_test)):
            #     if [cells_to_test[i][0], (cells_to_test[i][1][0], cells_to_test[i][1][1]+1)] in bot_cells or [cells_to_test[i][0], (cells_to_test[i][1][0], cells_to_test[i][1][1]-1)] in bot_cells:
            #         if cells_to_test[i] not in cells_to_set:
            #             cells_to_set.append(cells_to_test[i])
            
            # for i in range(len(cells_to_test)):
            #     if [cells_to_test[i][0], (cells_to_test[i][1][0] +1, cells_to_test[i][1][1])] in bot_cells or [cells_to_test[i][0], (cells_to_test[i][1][0]-1, cells_to_test[i][1][1])] in bot_cells:
            #         if cells_to_test[i] not in cells_to_set:
            #             cells_to_set.append(cells_to_test[i])
              
            print('offensive',cells_to_set)
        
        #cells_to_set.sort(reverse = True) if len(cells_to_set) > 0 else None
        
        
        # If set_list is empty the Bot chooses from all empty cells, but from the list with a higher probability
        # for the middle cells
        if len(cells_to_set) == 0:
            cells_to_set = empty_cells
        
        cells_to_set = self.shuffle_by_ring(cells_to_set, board)
        
        #print(empty_cells)
        # print(cells_to_set)
        
        #print(cells_to_set)
        # Choose row and col from the first entry of cells_to_set
        n, m = cells_to_set[0][1]
        #print(f'Spalte {m+1} , Zeile {n+1}')
        return super().make_move(board, m, n)
    

    
    def find_empty_cells(self, board):
        """function that locates the empty spots on the board

        Returns:
            tuple: list with tuples of empty cells in the format (ring ,(n,m)) = (row, col)
        """
        
        empty_cells = []
        for col in range(board.m):
                for row in range(board.n):
                    empty_cells.append([self.distance_to_edge(row, col, board),(row, col)]) if board.array[row, col] == 0 else None
                empty_cells.sort()
                empty_cells.reverse()
                    
        return empty_cells
    
    def find_bot_cells(self, board):
        """function that locates the cells set by the player on the board

        Returns:
            tuple: list with tuples of cells set by the bot in the format (ring ,(n,m)) = (row, col)
        """
        
        bot_cells = []
        for col in range(board.m):
                for row in range(board.n):
                    bot_cells.append([self.distance_to_edge(row, col, board),(row, col)]) if board.array[row, col] == self.player_number else None
                bot_cells.sort()
                bot_cells.reverse()
                    
        return bot_cells
    
    
    def distance_to_edge(self, row, col, board):
        """function that calculates the distance to the edge of the board

        Args:
            row (int): row on board
            col (int): col on board
            board (Board): board object

        Returns:
            int: _distance_ to the edge of the board
        """
        distance = min(min(row, col), min(board.n-row-1, board.m-col-1))
        
        return distance
        
    def shuffle_by_ring(self, cells: list, board: Board):
        '''
        Randomly shuffles the list of cells by ring, so that the bot sets in a random cell in the highest ring
        '''
        shuffled_cells = []
        num_rings = self.calculate_number_of_rings(board)
        for i in range(num_rings,-1,-1):
            cells_interim = []
            for cell in cells:
                if cell[0] == i:
                    cells_interim.append(cell)
                    shuffle(cells_interim)
            shuffled_cells.extend(cells_interim)
            
        return shuffled_cells
            
            
    def calculate_number_of_rings(self, board):
        '''
        Calculates the number of rings on the board
        '''
        min_dimension = min(board.n, board.m)
        if min_dimension % 2 == 0:
            num_rings = min_dimension // 2 + 1
        else:
            num_rings = min_dimension / 2
        
        return int(num_rings)
    
        

if __name__ == "__main__":
    from Game import Game 
     
    game = Game(Board(5, 5, 4), Player("PP", 1), Bot3(2))
    game.player1.make_move(game.board, 0, 0)
    #game.board.array[0][0] = 2
    #game.board.array[0][1] = 2
    game.board.array[1][1] = 2
    game.board.array[1][2] = 2
    game.board.array[3][3] = 2
    #game.board.array[2][2] = 1
    #game.board.array[4][0] = 1
    game.board.array[1][3] = 2
    #game.board.array[1][1] = 1
    #game.board.array[0][4] = 2
    game.board.display()
    #game.player2.make_move(game.board, 1, 2)
    #game.player1.make_move(game.board, 1, 3)
    game.game_move(4,4)
    game.board.display()
    game.game_move(0,0)
    game.board.display()
    #game.game_move(2,4)
    #game.game_move(0,0)
    
    #game.board.display()


