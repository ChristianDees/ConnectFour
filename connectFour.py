#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 16:49:19 2025

@author: Christian Dees, Aitiana Mondragon
"""

import sys
import random

# Uniform Random 
def ur(board):
    move = random.randint(1,7)
    # Continue getting new move if possible
    while not legalMove(board, move-1) and not boardFull(board): 
        move = random.randint(1,7)
    if legalMove(board, move - 1): print(f"FINAL Move selected: {move}")
    

# Pure Monte Carlo Game Search
def pmcgs(verbose, numSims):
    '''
    Every move in tree search & rollout is random
    Output value for each of the immediate next moves (null for illegal) 
     and move selected at the end
    
    '''
    
    if verbose:
        pass
        # print additional info each simulation trace
    
    pass

# Upper Confidence Bound for Trees
def uct():
    pass
    
# Check if potential move is legal
def legalMove(board, colIdx):
    #return False
    return any(row[colIdx] == 'O' for row in board)
    
# Check if board is full
def boardFull(board):
    return all('0' not in row for row in board)

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
                    return True
    
    # Check draw
    if boardFull(board): return 0
    
    # Return non int if non-terminal state
    return None
    

def main():
    # Get args
    if len(sys.argv) != 4:
        print("Usage: connectFour.py <filename> <output_type> <number_of_simulations>")
        return
    # Get filename and strip '\n'
    filename = sys.argv[1]
    with open(filename, 'r') as file: 
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    
    ot = lines[0] # Output type
    np = lines[1]  # Next player (red or yellow)
    board = [line for line in lines[2:]] # Create board (6 x 7)
    # O -> open
    # Make move by specifying column (1-7), full column = illegal
    # Win for red (Min player) -> -1
    # Win for yellow (Max player) -> 1
    # Draw -> 0
    print(board)
    for i in board:
        print(i)
    print(termState(board))
    
    pass

if __name__ == '__main__':
    main()