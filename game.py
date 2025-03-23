"""
March 19, 2025

@authors: Christian Dees and Aitiana Mondragon
"""


import random

# Represents game of Connect Four
class ConnectFour:
    
    # Initialize game
    def __init__(self, board=None, player=None):
        # 6x7 game board
        self.board = board if board is not None else [["o" for _ in range(7)] for _ in range(6)]  
        # Current player
        self.player = player if player is not None else random.choice('y','r') 
    
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
    def displayResults(self, result):
        print("-" * 13)
        for row in self.board: print(" ".join(row).upper())
        print("-" * 13)
        if result == -1: print("Y Won!")  # -1 => y
        elif result == 0: print("Draw!")  # 0 => draw
        elif result == 1: print("R Won!") # 1 => r