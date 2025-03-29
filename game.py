"""
March 19, 2025

@authors: Christian Dees and Aitiana Mondragon
"""


from algorithms import UR, PMCGS, UCT

# Game constants
ROWS = 6
COLS = 7
PLAYER_R = 'r'
PLAYER_Y = 'y'
EMPTY = 'o'


# Represents game of Connect Four
class ConnectFour:
    
    # Initialize game
    def __init__(self, board=None, player=None):
        # 6x7 game board, current player, game winner
        self.board = board if board is not None else [[EMPTY] * COLS for _ in range(ROWS)]  
        self.player = player if player is not None else PLAYER_R
        self.outcome = None
    
    # Check if board has no spots available
    def boardFull(self):
        return all(self.board[0][col] != EMPTY for col in range(7))    
    
    # Function to get the legal moves (first available empty spot in each column)
    def getMoves(self):
        moves = []
        for col in range(COLS):
            # From bottom to top
            for row in range(ROWS - 1, -1, -1):  
                if self.board[row][col] == EMPTY:
                    moves.append((row, col))
                    break # Only need 1 per column
        return moves
    
    # Place piece on board spot
    def placePiece(self, move, player):
        row, col = move
        self.board[row][col] = player
    
    # Make space empty
    def removePiece(self, move):
        row, col = move
        self.board[row][col] = EMPTY

    # Function to check if the game has ended (win, loss, or draw)
    def isTerminal(self, lastMove):
        if lastMove is None: return False
        row, col = lastMove
        directions = [
            [(0, 1), (0, -1)],  # Horizontal 
            [(1, 0), (-1, 0)],  # Vertical 
            [(1, 1), (-1, -1)], # Positive Diagonal 
            [(1, -1), (-1, 1)]  # Negative Diagonal 
        ]
        # Each direction in relation to last move
        for direction in directions:
            count = 1  # Count the last move itself
            for dr, dc in direction:
                r, c = row, col # Start from last move
                # While in bounds, continue checking
                while 0 <= r + dr < 6 and 0 <= c + dc < 7 and self.board[r + dr][c + dc] == self.board[row][col]:
                    count += 1
                    r, c = r + dr, c + dc
                # Win if 4 consecutive match
                if count >= 4: 
                    if self.board[row][col] == PLAYER_R: self.outcome = -1
                    elif self.board[row][col] == PLAYER_Y: self.outcome = 1
                    return True
        # Check if no spots/draw      
        if self.boardFull(): 
            self.outcome = 0
            return True
        return False

    # Print results
    def displayOutcome(self):
        for row in self.board:
            print(" ".join(row))
        print("=" * 13)
        if self.outcome == 1: print("Y WON!")
        elif self.outcome == -1: print("R WON!")
        elif self.outcome == 0: print("DRAW!")

    # Run the game
    def play(self, algs, sims, display):
        # Get algorithms and simulations
        alg1, sim1 = algs[0], sims[0]
        alg2, sim2 = (algs[1], sims[1]) if len(algs) > 1 else (alg1, sim1)
        # Map algs to their classes/objs
        algorithms = {
            'ur': UR(self),
            'pmcgs': PMCGS(self),
            'uct': UCT(self)
        }
        while (1):
            # Make first move
            if self.player == PLAYER_R: move = algorithms[alg1].bestMove(sim1)
            else: move = algorithms[alg2].bestMove(sim2)
            # Make the move
            self.placePiece(move, self.player)
            # Check if game over
            if self.isTerminal(move):
                if display: self.displayOutcome()
                if self.outcome != 0: return self.player
                return None
            # Alternate player
            self.player = PLAYER_R if self.player == PLAYER_Y else PLAYER_Y