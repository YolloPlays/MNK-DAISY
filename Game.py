from Board import Board
from Player import Player
from MyBot import *
import random as rr
import os

class Game:
    def __init__(self, board:Board, player1:Player, player2:Player  = Bot0(2), **kwargs) -> None:
        """
        Initializes the game with the given board, players, and optional parameters.

        Parameters:
            board (Board): The game board.
            player1 (Player): The first player.
            player2 (Player): The second player.
            shuffle (bool, optional): Indicates if the players should be shuffled. Defaults to None.
            should_log (bool, optional): Indicates if the game should be logged. Defaults to None.
            repeat (int, optional): Indicates the number of game repetitions. Defaults to None.
            should_print (bool, optional): Indicates if the game should print. Defaults to None.
        """
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.shuffle = kwargs.get("shuffle")
        self.starting_player = bool(rr.getrandbits(1)) if self.shuffle else True
        self.playerturn = self.starting_player
        self.gui = False
        self.game_started = False
        self.should_log = kwargs.get("should_log") if kwargs.get("should_log") != None else False
        self.repeat = a if (a:=kwargs.get("repeat")) else 1
        self.should_print = kwargs.get("should_print") if kwargs.get("should_print") != None else True
        if self.should_log:
            log_path = os.path.join(os.getcwd(), "Logs")
            try:
                os.mkdir(log_path)
            except Exception:
                print("Logs folder might already exist.")
            try:
                with open(os.path.join(log_path, f"log_{str(player1)[7:11]}_{str(player2)[7:11]}.csv"), "x") as f:
                    f.write("starting player,winning number\n")
            except Exception:
                print("File already created, beginning to append")
            self.f = open(os.path.join(log_path, f"log_{str(player1)[7:11]}_{str(player2)[7:11]}.csv"), "a")
    
    
    @classmethod
    def create_game(cls):
        """
        Interactively configures and creates a new game instance with customized settings or defaults.
        
        This method guides the user through a series of choices to configure the game setup, including:
        - Board size (m, n, k) with an option to use default values (5, 5, 4) or enter custom values.
        - Selection of the game mode: Human vs. Human, Human vs. Bot, or Bot vs. Bot.
        - For games involving humans, names for the human players are requested.
        - For games involving bots, the user selects from available bot types for each bot player.
        - Finally, the user decides which player starts the game.
        
        The method utilizes input validation to ensure that all user inputs are valid before proceeding
        with the game configuration. If an invalid input is detected at any stage, the user is prompted
        to re-enter a valid option.
        
        Parameters:
            cls: Class method parameter used to instantiate the class with the configured settings.
        
        Returns:
            A new instance of the class configured according to the user's selections.
        
        Note:
            - The 'm', 'n', and 'k' parameters define the board's dimensions and the win condition, respectively.
            - The method provides a flexible setup process, allowing for a variety of game configurations.
            - The choice of who starts the game can significantly impact the gameplay experience.
    
        """
        
        
        skip_input = True if len(input('Hit "Enter" to play with default values (m = 5, n = 5, k = 4). \nPress any "key + Enter" to enter custom values: ')) == 0 else False
        
        if not skip_input:
            print('Please enter the size of the board: \n')
            m = int(input("m: "))
            n = int(input("n: "))
            k = int(input("k: "))
            board = Board(m, n, k)
        
        else:
            board = Board()
        
        print(30*"-")
        
        bots = {"1": Bot0, "2": Bot1, "3": Bot2, "4": Bot3}
        
        while True:
            print("Please choose a gamemode: \n" )
            
            gamemodes = {"1": "Human vs. Human", "2": "Human vs. Bot", "3": "Bot vs. Bot"}
            for key, value in gamemodes.items():
                print(f"{key}: {value}")
            gamemode_choice = input("Please enter the number of the gamemode you would like to play: ").strip()
            print(30*"-")
            
            if gamemode_choice not in gamemodes:
                print("Invalid input. Please choose a valid gamemode number. \n")
                continue
            break
        
        if gamemode_choice == "1" or gamemode_choice == "2":
            player1 = Player(input("Please enter the name for human player 1: "), 1)
            print(30*"-")
            if gamemode_choice == "1":
                player2 = Player(input("Please enter the name for human player 2: "), 2)
                print(30*"-")
            else:
                while True:
                    print("Please choose a bot: \n")
                    for key, value in bots.items():
                        print(f"{key}: {value.__name__}")
                    bot_choice = input("Please enter the number of the bot you would like to play against: ").strip()
                    print(30*"-")
                    if bot_choice not in bots:
                        print("Invalid input. Please choose a valid bot number. \n")
                        continue

                    player2 = bots[bot_choice](2)
                    break
        
        if gamemode_choice == "3":
            while True:
                print("Please choose a bot for player 1: \n")
                for key, value in bots.items():
                    print(f"{key}: {value.__name__}")
                bot_choice = input("Please enter the number of the bot you would like to set as player 1: ").strip()
                print(30*"-")

                if bot_choice not in bots:
                    print("Invalid input. Please choose a valid bot number. \n")
                    continue

                player1 = bots[bot_choice](1)
                break
            
            while True:
                print("Please choose a bot for player 2: \n")
                for key, value in bots.items():
                    print(f"{key}: {value.__name__}")
                bot_choice = input("Please enter the number of the bot you would like to set as player 2: ").strip()
                print(30*"-")
                
                if bot_choice not in bots:
                    print("Invalid input. Please choose a valid bot number. \n")
                    continue

                player2 = bots[bot_choice](2)
                
                break
        
            
        while True:
            startplayer_choice = input(f"Who should start? (1: {player1.name}, 2: {player2.name}): ").strip()
            print(30*"-")
            if startplayer_choice == "1":
                break
            elif startplayer_choice == "2":
                player_interim = player1
                player1 = player2
                player2 = player_interim
                break
            else:
                print("Invalid Input. Please choose 1 or 2. ")
                continue

        return cls(board, player1, player2)
    
    
    def game_move(self, m, n):
        """
        A function to handle the game move, including player turn, player change, win check, and debugging.
        Parameters: #<= Are overwritten for Bots and only used for player moves
            self: the object instance
            m: the column index of the move
            n: the row index of the move
        Returns:
            Tuple containing success status, current player's turn, and the position of the chip placed
        """
        # TODO handle real play and player change handle win check
        # print(m, n) # <= Reality: player move # Debug
        current_player_turn = self.playerturn
        current_player = self.player1 if current_player_turn else self.player2
        success = False
        chip_at=None
        if self.board.array[n][m] == 0 or type(current_player) != Player:
            chip_at = current_player.make_move(self.board, m, n)
            success = True
            self.playerturn = not self.playerturn
        # self.board.display() # DEBUG
        # self.gui.display_win(False) # DEBUG
        return (success, current_player_turn, chip_at) # <= needed for gui to know whos players turn it was True: player1, False: player 2
    
    def is_bot(self):
        """
        Check if the current player is a bot. 
        Returns:
            (bool) indicating if the current player is a bot.
        """
        current_player = self.player1 if self.playerturn else self.player2
        return type(current_player) != Player
        
     
    def start(self):
        """
        Method to start the game. Sets the game_started flag to True and, if the gui is available gameloop will be handled by GUI.
        """
        self.game_started = True
        if not self.gui: # <= Backwards compatibility for raw input
            self.game_loop()
        
        
    def game_loop(self):
        """
        The game loop that iterates through the game rounds and player moves, 
        determines the winner, displays the board, and logs the game results if needed.
        """
        for i in range(self.repeat):
            while self.game_started and not self.board.has_won() and not self.board.is_draw():
                player = self.player1 if self.playerturn else self.player2
                self.board.display() if self.should_print else None
                player.make_move(self.board)
                self.playerturn = not self.playerturn
            if self.board.has_won():
                winner = self.player2 if self.board.has_won()-1 else self.player1
                print(f"{winner.name} has won") if self.should_print else None
                self.board.display() if self.should_print else None
                self.log(f"{int(not self.starting_player)+1},{winner.player_number}")
            else: 
                print("Full board! It's a draw") if self.should_print else None
                self.log(f"{int(not self.starting_player)+1},0")
            self.board.reset()
            if self.shuffle:
                self.starting_player = bool(rr.getrandbits(1))
                self.playerturn = self.starting_player
            print("\n\n\n\n\n") if self.should_print else None
        #print(i) # <= Debug
    
    def log(self, string):
        """
        Logs the given string if logging is enabled.

        Parameters:
            string (str): The string to be logged.
        """
        if self.should_log:
            self.f.write(f"{string}\n")

      
if __name__ == "__main__":
    
    game = Game.create_game()
    if game:
        game.start()
    
