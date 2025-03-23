#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 2025

@author: Christian Dees, Aitiana Mondragon
"""

import sys
import random
import numpy as np
import argHandler
import treeNode

class ConnectFour:
    
    def __init__(self, board=None, player=None):
        self.board = np.array(board) if board is not None else np.array([['O'] * 7 for _ in range(6)])
        self.player = player or random.choice(['R','Y'])
        self.outcome = None
        self.history = []

        
    # Return list of tuples of legal spots
    def getEmptySpots(self):
        empty_spots = []
        rows = len(self.board)
        cols = len(self.board[0])
        for col in range(cols):
            # Start from bottom row
            for row in range(rows - 1, -1, -1):  
                # Check empty spot
                if self.board[row][col] == 'O':  
                    # Bottom or above a letter
                    if row == rows - 1 or self.board[row + 1][col] != 'O':  
                        empty_spots.append((row, col))
                    break  # Only need one spot per column
        return empty_spots
    
    # Check if board is full
    def boardFull(self):
        return all('O' not in row for row in self.board)

    # Place piece on board at row, col
    def placePiece(self, move):
        rowIdx, colIdx = move
        self.board[rowIdx] = self.board[rowIdx][:colIdx] + self.player + self.board[rowIdx][colIdx + 1:]
        self.history.append((rowIdx, colIdx))  # Track the move made
        self.switchPlayer()
    
    # Print board out
    def displayBoard(self):
        for row in self.board: 
            print(row)
            
    # Check if game in terminal state (win/draw)
    def isTerminal(self):
        # Get total rows and cols
        numRows = len(self.board)
        numCols = len(self.board[0])
        
        # Check horizontal
        def horizontalWinner(board):
            for row in range(len(board)):
                # Keep within bounds
                for col in range(len(board[0]) - 3):  
                    piece = board[row][col]
                    if piece != 'O': 
                        # Check if there are 4 consecutive pieces horizontally
                        if all(board[row][col + i] == piece for i in range(4)):
                            if piece == 'R': return -1
                            elif piece == 'Y': return 1
            # No horizontal winner
            return None
            
        # Evaluate if winner horizontal
        hw = (horizontalWinner(self.board))
        if hw is not None: 
            self.outcome = hw
            return hw
        
        # Check vertical -> transpose and check horizontally
        flippedBoard = [''.join(i) for i in zip(*self.board)]
        vw = (horizontalWinner(flippedBoard))
        if vw is not None: 
            self.outcome = vw
            return vw
        
        # Check positive diagonal
        for row in range(numRows - 3):    # Keep within bounds
            for col in range(3, numCols): 
                piece = self.board[row][col]
                if piece != 'O':
                    # Check bottom-left to top-right diagonal 
                    if all(self.board[row + i][col - i] == piece for i in range(4)):
                        if piece == 'R': 
                            self.outcome = -1
                            return -1
                        elif piece == 'Y': 
                            self.outcome = 1
                            return 1
        
        # Check negative diagonal
        for row in range(numRows - 3):     # Keep within bounds
            for col in range(numCols - 3):  
                piece = self.board[row][col]
                if piece != 'O':
                    # Check top-left to bottom-right
                    if all(self.board[row + i][col + i] == piece for i in range(4)):
                        if piece == 'R': 
                            self.outcome = -1
                            return -1
                        elif piece == 'Y': 
                            self.outcome = 1
                            return 1
        
        # Check draw
        if self.boardFull(): 
            self.outcome = 0
            return 0
        
        # Return non int if non-terminal state
        self.outcome = None
        return None
        
    # Show outcome of game
    def displayOutcome(self):
        print("-" * 7)
        self.displayBoard()
        print("-" * 7)
        if self.outcome == -1:  print("R Won!")
        elif self.outcome == 0: print("Draw!")
        elif self.outcome == 1: print("Y Won!")
        else: print("No outcome!")
        
    # Switch to current player
    def switchPlayer(self):
        self.player = 'R' if self.player == 'Y' else 'Y'
    
    def undoMove(self):
        if self.history:
            rowIdx, colIdx = self.history.pop()  # Get the last move
            self.board[rowIdx] = self.board[rowIdx][:colIdx] + 'O' + self.board[rowIdx][colIdx + 1:]

            



# Uniform Random Search
def urs(game):
    return random.choice(game.getEmptySpots())
    
# Pure Monte Carlo Game Search
def pmcgs(game, root, verbose, sims):
    
    allNodes = {}
    possibleMoves = root.getPossibleMoves(game)
    
    
    originalPlayer = game.player
    
    # Perform simulations
    for move in possibleMoves:
        
        if move not in allNodes:
            root.move = move
            allNodes[move] = root
        
        for _ in range(sims):
            game.history.clear()
            game.player = originalPlayer
            if verbose: print()
            # Reset the board to the original state before each simulation
            

            node = root
            totalDos = 0
            # Simulate a game
            while game.isTerminal() is None: 
                childMove = random.choice(node.getPossibleMoves(game))
                if childMove not in allNodes:
                    newNode = treeNode.Node(move=childMove, parent=node)
                    node.children.append(newNode)
                    allNodes[childMove] = newNode
                    if verbose: print("NODE ADDED")
                else:
                    newNode = allNodes[childMove]
                if verbose: print(f"Move selected: {childMove}")
                game.placePiece(childMove)
                totalDos+=1
                node = newNode
            
            totalUndos = 0
            # Get result of the game
            result = game.isTerminal()
            if verbose: print(f"TERMINAL NODE VALUE: {result}")
            # Backpropagate results
            while node is not None:
                game.undoMove()
                totalUndos+=1
                node.N += 1
                #if node.move == root.move:
                node.W += result
                node.Q = node.W / node.N
                if verbose: print(f"\nUpdated values:\nwi: {node.W}\nni: {node.N}")
                node = node.parent
                
            while game.history:
                game.undoMove()
                
            if verbose: print(f"TOTAL DOS: {totalDos}, TOTAL UNDOS: {totalUndos}")
    finalMove, maxQ = None, float('-inf')  # Initialize the final move and maxQ

    column_q_values = ['Null'] * 7  # Initialize all columns with 'Null'
    for move in possibleMoves:
        node = allNodes[move]
        col = move[1]  
        
        # Update final move if current Q value is higher
        if node.Q > maxQ:
            maxQ = node.Q
            finalMove = move
        
        # Set Q value for the column
        column_q_values[col] = "{:.2f}".format(node.Q)
    
    
    # Print the column results
    if verbose: print('\n'.join([f"Column {i + 1}: {column_q_values[i]}" for i in range(7)]))
    
    # Return the best move found after all simulations
    return finalMove


  
# Upper Confidence Bound for Trees
def uct():
    pass


# Simulate a game and return winner
def simulateGame(game, algorithm, root, verbose, sims):
    while game.isTerminal() is None:
        move = None
        if algorithm == 'ur':
            move = urs(game)
        elif algorithm == 'pmcgs':
            move = pmcgs(game, root, verbose, sims)        
        if move:
            print(f"FINAL Move selected: {move[1]+1}")
            game.placePiece(move)
            
    return game.outcome
    
    
# Assuming `ConnectFour` and `Node` are defined elsewhere
def main():
    # Initialize the game and simulation
    result = argHandler.extract(sys.argv)
    if result is None: return
    board, player, algorithm, verbose, sims = result
    game = ConnectFour(board, player)
    root = treeNode.Node(game)
    # Run algorithm
    if algorithm == 'ur': simulateGame(game, algorithm, None, 0)
    elif algorithm == 'pmcgs': simulateGame(game, algorithm, root, verbose, sims)
    game.displayOutcome()

# Call the main function
if __name__ == "__main__":
    main()
