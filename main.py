#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
March 19, 2025

@authors: Christian Dees and Aitiana Mondragon
"""

import sys
from algorithms import PMCGS, UR
from game import ConnectFour
from argHandler import extract


# Official playing of Connect Four
def play(game, algorithm, verbose, sims):
    result = None # Game outcome
    move = None   # Current move to be made
    while result is None:
        if game.isTerminal(move):
            # If this is current player, then previous won
            if game.player == 'r': result = -1  # Y won
            elif game.player == 'y': result = 1 # R won
        if game.boardFull(): result = 0 # Draw
        if result is not None: break
        # Handle Pure Monte Carlo Game Search
        if algorithm == 'pmcgs':
            mcts = PMCGS(game, verbose)
            mcts.run(sims) # Run for given simulations
            move = mcts.bestMove() 
        # Handle Upper Confidence bound for Tree
        elif algorithm == 'uct':
            uct = PMCGS(game, verbose, uct=True)
            uct.run(sims)  # Run for given simulations
            move = uct.bestMove()
        # Handle Uniform Random
        elif algorithm == 'ur':
            ur = UR(game)
            move = ur.bestMove()
        if move is None: break
        print(f"FINAL Move selected: {move[1] + 1}") 
        game.placePiece(move) # Make move
        game.switchPlayer()   # Alternate player
    # Game is complete
    game.displayResults(result)
    
# Setup game and parameters
def main():
    # Get args
    result = extract(sys.argv)
    if result is None: return
    board, player, algorithm, verbose, sims = result
    game = ConnectFour(board, player)
    # Play the game
    play(game, algorithm, verbose, sims)

if __name__ == "__main__":
    main()