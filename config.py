"""
March 19, 2025

@authors: Christian Dees and Aitiana Mondragon
"""


import os
import random

# Extract and get configurations for game
class GameConfig:
    def __init__(self, args):
        self.filename = None  # File holding player, board, and algorithm
        self.verbose = False  # Flag for detailed output
        self.sims = 0         # Number of simulations
        self.algorithm = None # Algorithm to be used
        self.player = None    # Current player
        self.board = None     # Game board
        self.tournamentMode = False  # Flag for tournament mode
        self.parseArgs(args)  # Parse args to set values

    # Sets all constructor values
    def parseArgs(self, args):
        # If no arguments are provided, set default values
        if len(args) == 1:
            self.board = [[' ' for _ in range(7)] for _ in range(6)]  # Empty board
            self.player = random.choice(['r', 'y'])  # Randomly choose player
            return

        # Check for tournament mode
        if len(args) == 2 and args[1] == '-t':
            self.tournamentMode = True
            return

        # Validate enough args
        if len(args) != 4:
            print("Usage: main.py <filename> <verbosity> <number_of_simulations>")
            return None
        
        # Get filename
        self.filename = args[1]

        # Check file exists
        if not os.path.isfile(self.filename):
            print(f"Error: The file '{self.filename}' does not exist.")
            return None

        # Validate verbosity
        verbosity = args[2].lower()
        if verbosity == 'verbose':
            self.verbose = True
        elif verbosity != 'brief':
            print("Error: Invalid verbosity. Use 'Verbose' or 'Brief'.")
            return None

        # Validate number of simulations
        try:
            self.sims = int(args[3])
            if self.sims < 0:
                print("Error: Number of simulations must be a positive integer.")
                return None
        except ValueError:
            print("Error: Number of simulations must be an integer.")
            return None

        # Read file
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
        except Exception as e:
            print(f"Error: Could not read the file. {e}")
            return None

        # Format lines
        lines = [line.strip().lower() for line in lines]

        # Validate file size
        if len(lines) < 3:
            print("Error: The file should contain at least 3 lines (algorithm, player, board (6x7)).")
            return None
        
        # Validate algorithm
        self.algorithm = lines[0]
        if self.algorithm not in ['ur', 'pmcgs', 'uct']:
            print("Error: Invalid algorithm. Choose 'ur' (Uniform Random), 'pmcgs' (Pure Monte Carlo Game Search), or 'uct' (Upper Confidence Bound for Trees).")
            return None

        # UR algorithm simulation constraint
        if self.sims > 0 and self.algorithm == 'ur':
            print("Error: Simulations must be set to 0 when using Uniform Random Strategy.")
            return None

        # UR algorithm output constraint
        if self.verbose and self.algorithm == 'ur':
            print("Error: Verbosity must be set to 'Brief' when using Uniform Random Strategy.")
            return None

        # Validate player
        self.player = lines[1]
        if self.player not in ['r', 'y']:
            print("Error: Invalid player. Choose 'r' (red) or 'y' (yellow).")
            return None

        # Validate board size (should be 6x7)
        self.board = [list(line.strip()) for line in lines[2:]]
        if not len(self.board) == 6 or any(len(row) != 7 for row in self.board):
            print("Error: The board must be a 6x7 grid.")
            return None
    
    # Get the game's configurations
    def getConfigs(self):
        return self.board, self.player, self.algorithm, self.verbose, self.sims