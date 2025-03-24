#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
March 19, 2025

@authors: Christian Dees and Aitiana Mondragon
"""


import sys
from game import ConnectFour
from config import GameConfig
import itertools

# Round-robin tournament for algorithms
def tournament():
    configs = [
        ('ur', 0),
        ('pmcgs', 500),   # Default = 500
        ('pmcgs', 10000), # Default = 10k
        ('uct', 500),     # Default = 500
        ('uct', 10000)    # Default = 10k
    ]
    # Every combo (total=25)
    combinations = list(itertools.product(configs, repeat=2))
    # Combo: number of wins
    wins = {((alg1, sims1), (alg2, sims2)): 0 for (alg1, sims1), (alg2, sims2) in combinations}
    wins.update({((alg2, sims2), (alg1, sims1)): 0 for (alg1, sims1), (alg2, sims2) in combinations})
    # Switch player based on seen setup before
    expectAlgs = {}
    player = None
    totalGames = 1
    for (alg1, sims1), (alg2, sims2) in combinations:
        # Swap player if needed, start with r by default
        expectAlgs[(alg2, alg1)] = 'r' if player == 'y' else 'y' 
        player = expectAlgs.get((alg1, alg2), 'r')  
        # Run algorithms against each other for x games
        for _ in range(totalGames):
            game = ConnectFour(board=None, player=player)
            result = game.play(algorithms=[alg1, alg2], verbose=None, sims=[sims1, sims2], display=False)
            # Check if resulted in win and update
            if (result == -1 and player == 'y') or (result == 1 and player == 'r'): wins[((alg1, sims1), (alg2, sims2))] += 1
    
    # Print outcome of win percentages
    for key, value in wins.items():
        print(f"[{key[0][0]} {key[0][1]}][{key[1][0]} {key[1][1]}]: {round((value/totalGames)*100)}%")
  
# Setup game and parameters
def main():
    # Get args and create game
    gameConfig = GameConfig(sys.argv)
    configs = gameConfig.getConfigs()
    try:
        if gameConfig.tournamentMode: tournament()
        elif None in configs: return
        else:
            board, player, algorithm, verbose, sims = configs
            game = ConnectFour(board, player)
            # Play the game
            game.play([algorithm], verbose, [sims])
    except KeyboardInterrupt:
        print("\nExiting...")
        
if __name__ == "__main__":
    main()