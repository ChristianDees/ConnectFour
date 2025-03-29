"""
March 19, 2025

@authors: Christian Dees and Aitiana Mondragon
"""


import random
from treeNode import Node
from math import sqrt, log

# Game constants
ROWS = 6
COLS = 7
PLAYER_R = 'r'
PLAYER_Y = 'y'
EMPTY = 'o'


# UR (Uniform Random) Algorithm
class UR:
    
    # Initialize UR for a game
    def __init__(self, game):
        self.game = game
    
    # Return random legal move
    def bestMove(self, sims=0):
        moves = self.game.getMoves()
        if moves: return random.choice(moves)
        return None


# Base class for Monte Carlo Game Search 
class MCGS:
    
    # Initialize MCGS for a game
    def __init__(self, game):
        self.game = game

    # Simulate a complete game with random moves
    def randomRollout(self, node):
        current_player = self.game.player
        history = [] # Track moves
        move = node.move
        self.game.placePiece(move, current_player)
        history.append(move)
        current_player = PLAYER_R if current_player == PLAYER_Y else PLAYER_Y
        while True:
            moves = self.game.getMoves()
            if not moves: return 0  # Draw
            move = random.choice(moves)
            self.game.placePiece(move, current_player)
            history.append(move)
            # Found terminal state
            if self.game.isTerminal(move):
                for move in history: self.game.removePiece(move) # Undo moves
                return 1 if current_player == 'y' else -1 
            # Alternate player
            current_player = PLAYER_R if current_player == PLAYER_Y else PLAYER_Y

    # Update stats up the tree
    def backpropagate(self, node, outcome):
        while node:
            node.visits += 1     
            node.wins += outcome
            node = node.parent
    
    # Get move for mini
    def miniBestMove(self, root):
        bestMove = None
        bestValue = float('inf')
        for child in root.children.values():
            value = child.wins / child.visits if child.visits > 0 else float('inf')
            if value < bestValue:
                bestValue = value
                bestMove = child
        return bestMove
    
    # Get move for maxi
    def maxiBestMove(self, root):
        bestMove = None
        bestValue = float('-inf')
        for child in root.children.values():
            value = child.wins / child.visits if child.visits > 0 else float('-inf')
            if value > bestValue:
                bestValue = value
                bestMove = child
        return bestMove


# Pure Monte Carlo Game Search Algorithm 
class PMCGS(MCGS):
    
    # Initialize PMCGS for a game 
    def __init__(self, game):
        super().__init__(game)

    # Get the best move to be made
    def bestMove(self, simulations):
        root = Node()
        moves = self.game.getMoves()
        
        # Child node for each possible move 
        for row, col in moves: root.children[(row, col)] = Node(move=(row, col), parent=root)
        for _ in range(simulations):
            node = root
            # Get random leaf node to expand and simulate the game
            while node.children:
                row, col = random.choice(list(node.children.keys()))  
                node = node.children[(row, col)]  

            # Get result of leaf node (possible state)
            outcome = self.randomRollout(node)
            self.backpropagate(node, outcome)
        
        # Best move dictated from win/visit ratio & Maxi/Mini
        bestMove = None
        if self.game.player == PLAYER_R: bestMove = self.miniBestMove(root)
        elif self.game.player == PLAYER_Y: bestMove = self.maxiBestMove(root)
        if bestMove: return bestMove.move
        return None


# Upper Confidence Bound for Trees Algorithm
class UCT(MCGS):
    
    # Initialize UCT for a game
    def __init__(self, game):
        super().__init__(game)
        
    # Calculate UCB Value 
    def UCB(self, node, parent_visits):
        C = 1.4  # Exploration constant
        # Prioritize non-explored nodes
        if node.visits == 0:
            return float('inf')  
        nodeQ = node.wins / node.visits
        exploration = sqrt(log(parent_visits) / node.visits)
        return nodeQ + C * exploration    
        
    # Get the best move based on UCB vals
    def selectBestMoveUsingUCB(self, node):
        ucbVals = {}
        # Create UCB vals for each child
        for move in node.children: ucbVals[move] = self.UCB(node.children[move], node.visits)
        # Mini and Maxi
        if self.game.player == PLAYER_R: return min(ucbVals, key=ucbVals.get)
        elif self.game.player == PLAYER_Y: return max(ucbVals, key=ucbVals.get)
        

    # Get the best move to be made
    def bestMove(self, simulations):
        root = Node()
        moves = self.game.getMoves()
        
        # Child node for each possible move 
        for row, col in moves: root.children[(row, col)] = Node(move=(row, col), parent=root)
        for _ in range(simulations):
            node = root
            # Get leaf node with best UCB value 
            while node.children:
                # Calculate UCB values for all children and get the best for maxi/mini
                bestMove = self.selectBestMoveUsingUCB(node)
                node = node.children[bestMove]
            
            # Get result of leaf node 
            outcome = self.randomRollout(node)
            self.backpropagate(node, outcome)
            
        # Best move dictated from win/visit ratio & Mini/Maxu
        bestMove = None
        if self.game.player == PLAYER_R: bestMove = self.miniBestMove(root)
        elif self.game.player == PLAYER_Y: bestMove = self.maxiBestMove(root)
        if bestMove: return bestMove.move
        return None

    def __init__(self, game):
        self.game = game
        

    def move(self, simulations):
        root = Node()

        # Get all possible legal moves
        moves = self.game.getMoves()

        # Initialize the root children with legal moves
        for row, col in moves:
            root.children[(row, col)] = Node(move=(row, col), parent=root)

        for _ in range(simulations):
            node = root

            # Select a node using UCT
            while node.children:
                # Calculate UCB values for all children
                ucb_values = {move: self.ucb_value(node.children[move], node.visits, self.game.player) for move in node.children}
                best_move = max(ucb_values, key=ucb_values.get)  # Select the move with the highest UCB value
                node = node.children[best_move]

            # Simulate random moves and backpropagate the result
            outcome = self.randomRollout(node)
            self.backpropagate(node, outcome)

        best_move = None
        # After simulations, choose the best move based on win/visit ratio
        if self.game.player == PLAYER_R:  # minimizer
            best_move = min(root.children.values(), key=lambda x: x.wins / x.visits if x.visits > 0 else float('inf'))
        elif self.game.player == PLAYER_Y:  # maximizer
            best_move = max(root.children.values(), key=lambda x: x.wins / x.visits if x.visits > 0 else float('-inf'))

        if best_move:
            return best_move.move
        return None

    # UCB calculation for UCT
    def ucb_value(self, node, parent_visits, player):
        # UCB = (win/visits) + C * sqrt(log(parent_visits) / visits)
        C = 1.4  # Exploration constant
        if node.visits == 0:
            return float('inf')  # If the node has not been visited, prioritize it
        win_rate = node.wins / node.visits
        exploration = sqrt(log(parent_visits) / node.visits)
        return win_rate + C * exploration

    # Simulate a random game from the current state
    def randomRollout(self, node):
        current_player = self.game.player
        history = []
        move = node.move
        self.game.placePiece(move, current_player)
        history.append(move)
        current_player = PLAYER_R if current_player == PLAYER_Y else PLAYER_Y
        while True:
            moves = self.game.getMoves()
            if not moves:
                return 0  # Draw if no moves left
            move = random.choice(moves)
            self.game.placePiece(move, current_player)
            history.append(move)

            if self.game.isTerminal(move):
                for move in history:
                    
                    self.game.removePiece(move)
                    
                return 1 if current_player == 'y' else -1  # Yellow wins or Red wins

            # Switch player
            current_player = PLAYER_R if current_player == PLAYER_Y else PLAYER_Y

    # Backpropagate the result of a simulation through the tree
    def backpropagate(self, node, outcome):
        while node:
            node.visits += 1
            node.wins += outcome
            node = node.parent