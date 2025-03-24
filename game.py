"""
March 19, 2025

@authors: Christian Dees and Aitiana Mondragon
"""


import random
from algorithms import PMCGS, UR

# Represents game of Connect Four
class ConnectFour:
    
    # Initialize game
    def __init__(self, board=None, player=None):
        # 6x7 game board, current player, game winner
        self.board = board if board is not None else [["o" for _ in range(7)] for _ in range(6)] 
        self.player = player if player is not None else random.choice('y','r') 
        self.outcome = None
    
    # Check if board has no spots available
    def boardFull(self):
        return all(self.board[0][col] != 'o' for col in range(7))
    
    # Place piece on board spot
    def placePiece(self, move):
        row, col = move
        # If spot is empty
        if self.board[row][col] == 'o': self.board[row][col] = self.player
    
    # Undo a given move
    def undoMove(self, move):
        row, col = move
        # Make spot empty
        if self.board[row][col] != 'o': self.board[row][col] = 'o'
    
    # Check if game is over from win 
    def isTerminal(self, lastMove):
        if lastMove is None: return False
        row, col = lastMove
        directions = [
            [(0, 1), (0, -1)],  # Horizontal 
            [(1, 0), (-1, 0)],  # Vertical 
            [(1, 1), (-1, -1)], # Positive Diagonal 
            [(1, -1), (-1, 1)]  # Negative Diagonal 
        ]
        # Check every direction 
        for direction in directions:
            count = 1  # Count the last move itself
            for dr, dc in direction:
                r, c = row, col # Start from last move
                # While in bounds, continue checking
                while 0 <= r + dr < 6 and 0 <= c + dc < 7 and self.board[r + dr][c + dc] == self.board[row][col]:
                    count += 1
                    r, c = r + dr, c + dc
                # 4 in row is won
                if count >= 4: return True
        return False

    # Alternate current player 
    def switchPlayer(self):
        self.player = 'r' if self.player == 'y' else 'y'
    
    # Get empty spots on board
    def getMoves(self):
        moves = []
        for col in range(7):
            # Start at the bottom row
            for row in range(5, -1, -1): 
                # Append any open spots
                if self.board[row][col] == 'o':  
                    moves.append((row, col))
                    break
        return moves

    # Print game outcome and board
    def displayResults(self, ):
        print("-" * 13)
        for row in self.board: print(" ".join(row).upper())
        print("-" * 13)
        if self.outcome == -1: print("Y Won!")  # -1 => y
        elif self.outcome == 0: print("Draw!")  # 0 => draw
        elif self.outcome == 1: print("R Won!") # 1 => r
        else: print("No outcome!")
        
    # Official playing of Connect Four
    def play(self, algorithm, verbose, sims):
        move = None   # Current move to be made
        while self.outcome is None:
            if self.isTerminal(move):
                # If this is current player, then previous won
                if self.player == 'r': self.outcome = -1  # Y won
                elif self.player == 'y': self.outcome = 1 # R won
            if self.boardFull(): self.outcome = 0 # Draw
            if self.outcome is not None: break
            # Handle Pure Monte Carlo Game Search
            if algorithm == 'pmcgs':
                mcts = PMCGS(self, verbose)
                mcts.run(sims) # Run for given simulations
                move = mcts.bestMove() 
            # Handle Upper Confidence bound for Tree
            elif algorithm == 'uct':
                uct = PMCGS(self, verbose, uct=True)
                uct.run(sims)  # Run for given simulations
                move = uct.bestMove()
            # Handle Uniform Random
            elif algorithm == 'ur':
                ur = UR(self)
                move = ur.bestMove()
            if move is None: break
            print(f"FINAL Move selected: {move[1] + 1}") 
            self.placePiece(move) # Make move
            self.switchPlayer()   # Alternate player
        # Game is complete
        self.displayResults()