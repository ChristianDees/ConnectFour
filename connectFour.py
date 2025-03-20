#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 16:49:19 2025

@author: Christian Dees, Aitiana Mondragon
"""

import sys
import random

# Uniform Random 
def ur(board, piece):
    return random.choice(getEmptySpots(board))
    
# Pure Monte Carlo Game Search
def pmcgs(board, piece, sims):
    pass

# Upper Confidence Bound for Trees
def uct():
    pass
    
# Check if board is full
def boardFull(board):
    return all('O' not in row for row in board)

# Return list of tuples of legal spots
def getEmptySpots(board):
    empty_spots = []
    rows = len(board)
    cols = len(board[0])
    for col in range(cols):
        # Start from bottom row
        for row in range(rows - 1, -1, -1):  
            # Check empty spot
            if board[row][col] == 'O':  
                # Bottom or above a letter
                if row == rows - 1 or board[row + 1][col] != 'O':  
                    empty_spots.append((row, col))
                break  # Only need one spot per column
    return empty_spots

# Place piece on board at row, col
def placePiece(board, piece, move):
    rowIdx = move[0]
    colIdx = move[1]
    # Update piece at given spot
    board[rowIdx] = board[rowIdx][:colIdx] + piece + board[rowIdx][colIdx + 1:]

# Print board out
def displayBoard(board):
    for row in board:
        print(row)


# Check if game in terminal state (win/draw)
def termState(board):
    
    # Get total rows and cols
    numRows = len(board)
    numCols = len(board[0])
    
    # Check horizontal
    def horizontalWinner(boardC):
        for row in range(len(boardC)):
            # Keep within bounds
            for col in range(len(boardC[0]) - 3):  
                piece = boardC[row][col]
                if piece != 'O': 
                    # Check if there are 4 consecutive pieces horizontally
                    if all(boardC[row][col + i] == piece for i in range(4)):
                        if piece == 'R': return -1
                        elif piece == 'Y': return 1
        # No horizontal winner
        return None
        
    # Evaluate if winner horizontal
    hw = (horizontalWinner(board))
    if hw is not None: return hw
    
    # Check vertical -> transpose and check horizontally
    flippedBoard = [''.join(i) for i in zip(*board)]
    vw = (horizontalWinner(flippedBoard))
    if vw is not None: return vw
    
    # Check positive diagonal
    for row in range(numRows - 3):    # Keep within bounds
        for col in range(3, numCols): 
            piece = board[row][col]
            if piece != 'O':
                # Check bottom-left to top-right diagonal 
                if all(board[row + i][col - i] == piece for i in range(4)):
                    if piece == 'R': return -1
                    elif piece == 'Y': return 1
    
    # Check negative diagonal
    for row in range(numRows - 3):     # Keep within bounds
        for col in range(numCols - 3):  
            piece = board[row][col]
            if piece != 'O':
                # Check top-left to bottom-right
                if all(board[row + i][col + i] == piece for i in range(4)):
                    if piece == 'R': return -1
                    elif piece == 'Y': return 1
    
    # Check draw
    if boardFull(board): return 0
    
    # Return non int if non-terminal state
    return None

# Switch to current player
def altPiece(piece):
    return 'R' if piece == 'R' else 'Y'

# Simulate a game and return winner
def simulateGame(board, piece, verbose=False):
    boardC = board[:] # Copy board
    currPiece = piece 
    # Go through whole game
    while not boardFull(boardC):
        emptySpots = getEmptySpots(board)
        move = random.choice(emptySpots)
        placePiece(boardC, currPiece, move)
        winner = termState(boardC)
        if winner is not None:
            return winner
        currPiece = altPiece(currPiece)
    # No more spots -> draw
    return 0
  
def main():
    # Get args
    if len(sys.argv) != 4:
        print("Usage: connectFour.py <filename> <output_type> <number_of_simulations>")
        return
    filename = sys.argv[1]
    ot = sys.argv[2]
    sims = int(sys.argv[3])
    with open(filename, 'r') as file: 
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    
    alg = lines[0] # Algorithm
    np = lines[1]  # Next player (red or yellow)
    board = [line for line in lines[2:]] # Create board (6 x 7)
    # O -> open
    # Make move by specifying column (1-7), full column = illegal
    # Win for red (Min player) -> -1
    # Win for yellow (Max player) -> 1
    # Draw -> 0
    
    if alg == "UR":
        move = ur(board, np)
        print(f"FINAL Move selected: {move[1]+1}")
    elif alg == "PMCGS":
        move = pmcgs(board, np, sims)
        print(f"FINAL Move selected: {move[1]+1}")
        
if __name__ == '__main__':
    main()