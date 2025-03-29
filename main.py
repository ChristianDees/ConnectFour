#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
March 19, 2025

@authors: Christian Dees and Aitiana Mondragon
"""

import algorithms
import sys
from game import ConnectFour
from config import GameConfig
import itertools


# Round-robin tournament for algorithms
def tournament():
    configs = [
        ('ur', 0),
        ('pmcgs', 50),   # Default = 500
        ('pmcgs', 1000), # Default = 10k
        ('uct', 50),     # Default = 500
        ('uct', 1000)    # Default = 10k
    ]
    # Every combo (total=25)
    combinations = list(itertools.product(configs, repeat=2))
    # Combo: number of wins
    wins = {((alg1, sims1), (alg2, sims2)): 0 for (alg1, sims1), (alg2, sims2) in combinations}
    wins.update({((alg2, sims2), (alg1, sims1)): 0 for (alg1, sims1), (alg2, sims2) in combinations})
    totalGames = 100
    startPlayer = 'r'
    for algSims, victories in wins.items():
        (alg1, sim1), (alg2, sim2) = algSims
        for _ in range(totalGames):
            game = ConnectFour(board=None,player=startPlayer)
            winner = game.play(algs=[alg1, alg2], sims=[sim1, sim2], display=False)
            if winner==startPlayer:
                wins[algSims] += 1
    for key, value in wins.items():
        print(f"[{key[0][0]} {key[0][1]}][{key[1][0]} {key[1][1]}]: {round((value/totalGames)*100)}%")
  
# Setup game and parameters
def main():
    
    # Get args and create game
    try:
        gameConfig = GameConfig(sys.argv)
        configs = gameConfig.getConfigs()
        board, player, algorithm, verbose, sims = configs
        if gameConfig.tournamentMode: tournament()
        elif None in configs: return
        else:
            board, player, algorithm, verbose, sims = configs
            game = ConnectFour(board=board, player=player)
            # Play the game
            game.play([algorithm], [sims], display=True)
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    '''
    # MANUAL TESTING 1V1
    games = 20
    rWins = 0
    yWins = 0
    for _ in range(games):
        # Create and run the game
        game = ConnectFour(board=None,player='r')
        winner = game.play(['uct','uct'], [1000, 5], display=True)
        print(f"Winner: {winner}")
        if winner=='r': rWins+=1
        elif winner=='y': yWins+=1
    print(f"PMCGS: {(rWins/games)*100}%, UCT: {(yWins/games)*100}%")
    '''
    main()