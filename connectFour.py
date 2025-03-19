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
def pmcgs():
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
    ur(board)
    
    pass

if __name__ == '__main__':
    main()