"""
March 19, 2025

@authors: Christian Dees and Aitiana Mondragon
"""


from math import sqrt, log


# Node class to represent each node in the search tree
class Node:
    def __init__(self, move=None, parent=None, player=None):
        self.move = move  # The move that led to this node (now a tuple (row, col))
        self.wins = 0  # Number of wins from this node
        self.visits = 0  # Number of visits to this node
        self.children = {}  # Children nodes
        self.parent = parent  # Parent node (for backpropagation)

    def ucb_value(self, total_visits, C=1.4):
        # UCB value computation (if visits > 0, compute UCB)
        if self.visits == 0:
            return float('inf')  # Unvisited nodes have an infinite UCB value.
        return (self.wins / self.visits) + C * sqrt(log(self.parent.visits) / self.visits)