"""
March 19, 2025

@authors: Christian Dees and Aitiana Mondragon
"""

import os


def extract(args):
    
    # Validate enough args
    if len(args) != 4:
        print("Usage: connectFour.py <filename> <verbosity> <number_of_simulations>")
        return None
    
    # Get filename
    filename = args[1]

    # Check file exists
    if not os.path.isfile(filename):
        print(f"Error: The file '{filename}' does not exist.")
        return None

    # Validate verbosity
    verbose = False
    verbosity = args[2].lower()
    if verbosity == 'verbose': verbose = True
    elif verbosity != 'brief':
        print("Error: Invalid verbosity. Use 'Verbose' or 'Brief'.")
        return None

    # Validate number of simulations
    try:
        sims = int(args[3])
        if sims < 0:
            print("Error: Number of simulations must be a positive integer.")
            return None
    except ValueError:
        print("Error: Number of simulations must be an integer.")
        return None

    # Read file
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except Exception as e:
        print(f"Error: Could not read the file. {e}")
        return None

    # Format lines
    lines = [line.strip().lower() for line in lines]

    # Validate algorithm
    if len(lines) < 3:
        print("Error: The file should contain at least 8 lines (algorithm, player, board (6x7)).")
        return None
    
    # Get algorithm
    algorithm = lines[0]
    if algorithm not in ['ur', 'pmcgs', 'uct']:
        print("Error: Invalid algorithm. Choose 'ur' (Uniform Random) or 'pmcgs' (Pure Monte Carlo Game Search) or uct (Upper Confidence Bound for trees).")
        return None
    
    # UR algorithm simulation constraint
    if sims > 0 and algorithm == 'ur':
        print("Error: Simulations must be set to 0 when using Uniform Random Strategy.")
        return None
    
    # UR algorithm output constraint
    if verbosity != 'brief' and algorithm == 'ur':
        print("Error: Verbosity must be set to 'Brief' when using Uniform Random Strategy.")
        return None
    
    # Validate player
    player = lines[1]
    if player not in ['r', 'y']:
        print("Error: Invalid player. Choose 'r' (red) or 'y' (yellow).")
        return None
    
    # Validate board size (should be 6x7)
    board = [list(line.strip()) for line in lines[2:]]
    if not len(board) == 6 and all(len(row) == 7 for row in board):
        print("Error: The board must be a 6x7 grid.")
        return None

    return board, player, algorithm, verbose, sims