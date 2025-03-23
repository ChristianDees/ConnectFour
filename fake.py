import random
import math

class ConnectFour:
    def __init__(self, board, player):
        self.board = board if board else []
        self.player = player if player else random.choice(['r','y'])
        
    
    def boardFull(self):
        # Check if the board is full
        return all(self.board[0][col] != 'o' for col in range(7))
    
    def placePiece(self, move):
        row, col = move
        # Drop the disc in the specified (row, col) position
        if self.board[row][col] == 'o':  # Check if the spot is empty
            self.board[row][col] = self.player
            
    
    def undoMove(self, move):
        row, col = move
        # Undo the move by resetting the given (row, col) to 'O'
        if self.board[row][col] != 'o':
            self.board[row][col] = 'o'
            
    
    def isTerminal(self):
        # Check for a winning condition (4 in a row horizontally, vertically, or diagonally)
        for row in range(6):
            for col in range(7):
                if self.board[row][col] == 'o':  # Skip empty spots
                    continue
                # Check horizontally
                if col <= 3 and all(self.board[row][col + i] == self.board[row][col] for i in range(4)):
                    return True
                # Check vertically
                if row <= 2 and all(self.board[row + i][col] == self.board[row][col] for i in range(4)):
                    return True
                # Check diagonal (bottom-left to top-right)
                if row <= 2 and col <= 3 and all(self.board[row + i][col + i] == self.board[row][col] for i in range(4)):
                    return True
                # Check diagonal (top-left to bottom-right)
                if row >= 3 and col <= 3 and all(self.board[row - i][col + i] == self.board[row][col] for i in range(4)):
                    return True
        return False

    def switchPlayer(self):
        # Switch the player after a move
        self.player = 'r' if self.player == 'y' else 'y'
        
    def getEmptySpots(self):
        # Return the list of (row, col) where a move can be made (not full)
        moves = []
        for col in range(7):
            for row in range(5, -1, -1):  # Start from the bottom row
                if self.board[row][col] == 'o':  # Find the first empty spot
                    moves.append((row, col))
                    break
        return moves
    
    def displayOutcome(self):
        for row in self.board:
            print(" ".join(row))
        print(f"{self.player} Won!")

class Node:
    def __init__(self, move=None, parent=None):
        self.move = move  # The (row, col) where the move was made
        self.parent = parent  # Parent node
        self.children = []  # Children nodes
        self.Q = 0  # Quality value (average win score)
        self.N = 0  # Visit count (ni)
        self.W = 0  # Win count (wi)

    def bestChild(self):
        # Returns the child node with the highest win-to-visit ratio
        bestChild = None
        bestValue = -float('inf')

        for child in self.children:
            
            if child.Q > bestValue:
                bestValue = child.Q
                bestChild = child

        return bestChild


class PMCTS:
    def __init__(self, game, verbose=False):
        self.game = game
        self.verbose = verbose
        self.root = Node()  # The root doesn't represent any move
    
    def explore(self):
        currNode = self.root
        # Keep selecting child nodes until we encounter an unexpanded node
        while currNode is not None:
            if len(currNode.children) <= 0:
                # Expand the node to generate its children if not fully expanded
                self.expand(currNode)
                break
            currNode = currNode.bestChild()  # Select the best child based on UCB
        return currNode
    
    def expand(self, node):
        # Generate children for the current node (possible moves)
        moves = self.game.getEmptySpots()
        random.shuffle(moves)
        for move in moves:
            # Ensure a unique child for each possible move
            child = Node(move, parent=node)
            node.children.append(child)
        if self.verbose: print("NODE ADDED")
        return node.children  # Return the newly created children

    def simulate(self, node):
        
        game = self.game
        
        player = game.player  # Store the initial player
        
        initMove = node.move
        game.placePiece(initMove)  # Make the initial move
        history = []
        # Check if the current move immediately wins
        result = None
        if game.isTerminal():
            if game.player == 'r':
                result = 1
            elif game.player == 'y':
                result = -1
            else:
                result = 0  
        
        
        # Simulate the rest of the game
        while not game.boardFull():
            moves = game.getEmptySpots()
            if not moves:
                break
            move = random.choice(moves)
            game.placePiece(move)  # Make the move
            history.append(move)
            #rint(f"Move selected: {move}")
            if game.isTerminal():
                if game.player == 'r':
                    result = 1 
                elif game.player == 'y':
                    result=  -1
                else:
                    result= 0
                break
            game.switchPlayer()  
        if game.player != player:
            game.switchPlayer() 
        for move in history:
            game.undoMove(move) 
    
        game.undoMove(initMove)  
        
        return result  

    def backpropagate(self, node, result):
        if result is None:return
        currNode = node
        while currNode is not None:
            currNode.N += 1
            currNode.W += result
            currNode.Q = currNode.W / currNode.N  
            if self.verbose: print(f"\nUpdated values:\nwi: {currNode.W}\nni: {currNode.N}")
            currNode = currNode.parent

    def run(self, sims):
        for _ in range(sims):
            node = self.explore()
            if node is None or node.move is None: continue
            result = self.simulate(node)  
            self.backpropagate(node, result)

    def bestMove(self):
        if self.verbose:
            for idx in range(7):
                if idx < len(self.root.children): print(f"Column {idx+1}: {self.root.children[idx].Q:.2f}")
                else: print(f"Column {idx+1}: null")
        bestChild = self.root.bestChild()
        if bestChild is not None:
            return bestChild.move
        return None  



def print_board(board):
    for row in board:
        print(" ".join(row))

import os
def extract(args):
    
    # Validate enough args
    if len(args) != 4:
        print("Usage: connectFour.py <filename> <verbosity> <number_of_simulations>")
        return None
    
    filename = args[1]

    # Check file exists
    if not os.path.isfile(filename):
        print(f"Error: The file '{filename}' does not exist.")
        return None

    # Validate verbosity
    verbose = False
    verbosity = args[2].lower()
    if verbosity == 'verbose':
        verbose = True
    elif verbosity != 'brief':
        print("Error: Invalid verbosity. Use 'Verbose' or 'Brief'.")
        return None

    # Validate number of simulations
    try:
        sims = int(args[3])
        if sims < 0:
            print("Error: Number of simulations must be a positive integer.")
            return None
    except ValueError:
        print("Error: Number of simulations must be an integer.")
        return None

    # Read file
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except Exception as e:
        print(f"Error: Could not read the file. {e}")
        return None

    # Format lines
    lines = [line.strip().lower() for line in lines]

    # Validate algorithm
    if len(lines) < 3:
        print("Error: The file should contain at least 8 lines (algorithm, player, board (6x7)).")
        return None
    
    algorithm = lines[0]
    if algorithm not in ['ur', 'pmcgs', 'uct']:
        print("Error: Invalid algorithm. Choose 'ur' (Uniform Random) or 'pmcgs' (Pure Monte Carlo Game Search) or uct (Upper Confidence Bound for trees).")
        return None
    
    if sims > 0 and algorithm == 'ur':
        print("Error: Simulations must be set to 0 when using Uniform Random Strategy.")
        return None
    
    if verbosity != 'brief' and algorithm == 'ur':
        print("Error: Verbosity must be set to 'Brief' when using Uniform Random Strategy.")
        return None
    
    # Validate player
    player = lines[1]
    if player not in ['r', 'y']:
        print("Error: Invalid player. Choose 'r' (red) or 'y' (yellow).")
        return None
    
    # Validate board size (should be 6x7)
    board = [list(line.strip()) for line in lines[2:]]
    if not len(board) == 6 and all(len(row) == 7 for row in board):
        print("Error: The board must be a 6x7 grid.")
        return None

    return board, player, algorithm, verbose, sims

import sys

def play(game, algorithm, verbose, sims):
    pass




# Play the game until there is a winner or the game ends in a draw
def main():
    result = extract(sys.argv)
    if result is None: return
    board, player, algorithm, verbose, sims = result
    # Example Usage: Simulate a full game
    game = ConnectFour(board, player)
    
    #game.player = player.upper()

    while not game.boardFull():
        pmcts = PMCTS(game, verbose)
        pmcts.run(sims)  
        bestMove = pmcts.bestMove()  
        if bestMove is None: break
        print(f"FINAL Move selected: {bestMove[1] + 1}")
        game.placePiece(bestMove)  
        if game.isTerminal():
            game.displayOutcome()
            break

if __name__ == "__main__":
    main()

