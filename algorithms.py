"""
March 19, 2025

@authors: Christian Dees and Aitiana Mondragon
"""


import random
from treeNode import Node

# Uniform Random
class UR:

    # Initialize ur for a game
    def __init__(self, game):
        self.game = game # Game initial state
        
    # Get best move (random selection)
    def bestMove(self):
        moves = self.game.getMoves()
        return random.choice(moves)


# Pure Monte Carlo Game Search (Includes UCT)
class PMCGS:
    
    # Initialize pmcgs for a game
    def __init__(self, game, verbosity=False, uct=False):
        self.game = game       # Game initial state
        self.root = Node()     # Starting point for search
        self.verbosity = verbosity # Detailed output flag
        self.uct = uct         # Upper Confidence Bound for Trees
        self.uctMaxi = self.game.player # Get the maximizer
    
    # Get unexplored node
    def explore(self):
        currNode = self.root
        # Find leaf node
        while currNode is not None:
            if len(currNode.children) <= 0:
                # Get children
                self.expand(currNode)
                break
            if self.verbosity: print(f"\nwi: {currNode.W}\nni: {currNode.N}")
            # Find best child, pmcgs => random, uct => best ucb value
            currNode = currNode.bestChild(self.uct, self.uctMaxi, self.game.player, uctPrint=(self.uct and self.verbosity))
            if self.verbosity: print(f"Move selected: {currNode.move}")
        return currNode
    
    # Generate children (possible moves)
    def expand(self, node):
        moves = self.game.getMoves()
        # Add child (new possible game state)
        for move in moves:
            child = Node(move, parent=node)
            node.children.append(child)
        if self.verbosity: print("NODE ADDED\n")
        return node.children  

    # Simulate a game being ran
    def simulate(self, node):
        player = self.game.player 
        result = None  # Game outcome
        history = []   # Keep track of moves
        move = None  
        # Make initial move from current node
        self.game.placePiece(node.move)
        history.append(node.move)
        while result is None:
            if self.game.isTerminal(move):
                # If this is current player, then previous won
                if self.game.player == 'r': result = -1  # Y won
                elif self.game.player == 'y': result = 1 # R won
            if self.game.boardFull(): result = 0 # Draw
            if result is not None: break
            moves = self.game.getMoves()
            if not moves: break
            # Pick random move for rest of rollout
            move = random.choice(moves)
            self.game.placePiece(move) # Play move
            history.append(move)       # Add move made
            self.game.switchPlayer()   # Alternate player
        # Keep player order accurate in case broke from loop    
        if player != self.game.player: self.game.switchPlayer()
        # Restore board to original state
        for move in history:self.game.undoMove(move)
        return result # (-1,0,1, None)
    
    # Update stats up the tree
    def backpropagate(self, node, result):
        if result is None: return
        currNode = node
        while currNode is not None:
            currNode.N += 1      # Visited
            currNode.W += result # Game outcome
            currNode.Q = currNode.W / currNode.N 
            if self.verbosity: print(f"\nUpdated values:\nwi: {currNode.W}\nni: {currNode.N}")
            currNode = currNode.parent
            
    # Get best move after simulations        
    def bestMove(self):
        # Display Q values of children 
        if self.verbosity:
            print("\n")
            for idx in range(7):
                if idx < len(self.root.children): print(f"Column {idx+1}: {self.root.children[idx].Q:.2f}")
                else: print(f"Column {idx+1}: null")
        # Best child contains the best move to make
        bestChild = self.root.bestChild(self.uct, self.uctMaxi, self.game.player, uctPrint=False)
        if bestChild is not None: return bestChild.move
        return None
    
    # Create tree and result for nodes per simulation
    def run(self, sims):
        for _ in range(sims):
            node = self.explore()
            if node is None or node.move is None: continue
            # Now at leaf node, so find result
            result = self.simulate(node)  
            self.backpropagate(node, result)