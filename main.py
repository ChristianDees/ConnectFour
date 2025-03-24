#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
March 19, 2025

@authors: Christian Dees and Aitiana Mondragon
"""


import sys
from game import ConnectFour
from config import GameConfig

    
# Setup game and parameters
def main():
    # Get args and create game
    configs = GameConfig(sys.argv).getConfigs()
    if None in configs: return
    board, player, algorithm, verbose, sims = configs
    game = ConnectFour(board, player)
    # Play the game
    game.play(algorithm, verbose, sims)

if __name__ == "__main__":
    main()