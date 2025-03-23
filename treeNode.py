"""
March 19, 2025

@authors: Christian Dees and Aitiana Mondragon
"""

import math


# Nodes of a game tree
class Node:
    
    # Initialize node to be part of a tree
    def __init__(self, move=None, parent=None):
        self.move = move     # (row, col) where the move was made
        self.parent = parent # Parent node
        self.children = []   # Children nodes
        self.Q = 0  # Quality value 
        self.N = 0  # Visit count (ni)
        self.W = 0  # Win count (wi)


    # Selects best child from node 
    def bestChild(self, uct=False, uctPrint=False):
        bestChild = None
        bestValue = -float('inf')
        i =0
        # Compare every child
        for child in self.children:
            # uctPrint => uct algorithm AND verbose
            if uctPrint: i+=1
            # Use ucb value for best child
            if uct:
                if child.N == 0: ucb = float('inf') # Unexplored child
                else: ucb = child.Q / (child.N + 1e-6) + math.sqrt(2 * math.log(self.N + 1) / (child.N + 1e-6))
                if uctPrint: print(f"V{i}: {ucb}")
                if ucb > bestValue:
                    bestValue = ucb
                    bestChild = child
            # Use win-to-visit ratio if pmcgs
            else:
                if child.Q > bestValue:
                    bestValue = child.Q
                    bestChild = child
        # Display null for non-existing children
        if uctPrint: 
            for j in range(i, 7):
                print(f"V{j + 1}: null")
        
        return bestChild