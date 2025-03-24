# Connect Four AI

![Static Badge](https://img.shields.io/badge/Language-Python-blue)
![GitHub repo size](https://img.shields.io/github/repo-size/christiandees/ConnectFour)
![GitHub all releases](https://img.shields.io/github/downloads/christiandees/ConnectFour/total)

This program implements three distinct AI algorithms for playing Connect Four: **Uniform Random**, **Pure Monte Carlo Search**, and **Upper Confidence Bound for Trees (UCT)**. The game is played on a grid of 7 columns and 6 rows, with the objective of getting four of your pieces in a horizontal, vertical, or diagonal line.

The program explores these algorithms by constructing a game tree, where each node represents a potential new game state after a move. These algorithms use a combination of exploration and exploitation techniques to traverse the tree and evaluate possible moves. The leaf nodes represent terminal game states, which are simulated using random moves to determine the outcome. The overall goal is to leverage these algorithms to identify the most optimal move.

### Key Algorithms:
- **Uniform Random**: Moves are selected randomly from the available options.
- **Pure Monte Carlo Search**: A form of Monte Carlo Tree Search (MCTS) that simulates many random games from the current game state to estimate the best move.
- **Upper Confidence Bound for Trees (UCT)**: A Monte Carlo Tree Search variant that balances exploration and exploitation by considering both the potential value of a move and how many times it has been explored.

The program simulates a round-robin tournament where these three algorithms compete against each other, allowing for an in-depth comparison of their performance in different game scenarios.

## Table of Contents
1. [Getting Started](#getting-started)  
   1.1. [Command-Line Arguments](#command-line-arguments)  
   1.2. [File Format](#file-format-exampletxt)  
   1.3. [Default Behavior](#default-behavior)  
   1.4. [Verbosity and Simulations](#verbosity-and-simulations)  
   1.5. [Tournament Mode](#tournament-mode)  
2. [Example](#example)  
3. [Modules](#modules)  
   3.1. [treeNode.py](#treenode)  
   3.2. [algorithms.py](#algorithms)  
   3.3. [game.py](#game)  
   3.4. [config.py](#config)
4. [Contributing](#contributing)  
   4.1. [Issues and Feature Requests](#issues-and-feature-requests)




## Getting Started

### **Command-Line Arguments**

Run a game with:
```bash
./main.py <filename> <verbosity> <number_of_simulations>
```

- **`<filename>`**: Path to the input file (e.g., `example.txt`).
- **`<verbosity>`**: `brief` (minimal output) or `verbose` (detailed output).
- **`<number_of_simulations>`**: Number of simulations to run for move determination.

### **File Format: `example.txt`**

1. **First Line**: Algorithm to use (e.g., `"UR"`, `"PMCGS"`, `"UCT"`).
2. **Second Line**: The player to start, either `"r"` (red) or `"y"` (yellow).
3. **Next Six Lines**: The game board, with:
   - **`'r'`** for red, **`'y'`** for yellow, and **`'o'`** for empty spots.

### **Default Behavior**  
If no arguments are provided, the program will:
- Use an empty board.
- Randomly select the first player.
- Display brief output.
- Set the algorithm to *uniform random*.
- Run with 0 simulations.

To run the program with default settings, simply use:

```bash
./main.py
```
### **Verbosity and Simulations**  
If you want to specify the verbosity level and the number of simulations, you can provide two arguments: `<verbosity>` and `<number_of_simulations>`. If no file is provided, the program will still:
- Use an empty board.
- Randomly choose the first player.

Run the program with custom verbosity and simulation count as follows:

```bash
./main.py <verbosity> <number_of_simulations>
```

### **Tournament Mode**

To run a round-robin tournament between AI algorithms, use:
```bash
./main.py -t
```

## Example

**Example.txt**
```
PMCGS 
R
O O O O O O O
O O O O O O O
O O Y O O O Y
O O R O O O Y
O Y R Y O Y R
Y R R Y O R R
```
**Input**
```bash
./main.py example.txt brief 100
```

**Output**
```
FINAL Move selected: 5
FINAL Move selected: 1
FINAL Move selected: 4
FINAL Move selected: 7
FINAL Move selected: 7
FINAL Move selected: 3
FINAL Move selected: 6
FINAL Move selected: 3
FINAL Move selected: 1
FINAL Move selected: 1
FINAL Move selected: 1
FINAL Move selected: 4
FINAL Move selected: 2
-------------
O O Y O O O R
R O Y O O O Y
Y O Y Y O O Y
R R R R O R Y
Y Y R Y O Y R
Y R R Y R R R
-------------
R Won!
```

## Modules
- <a id="treenode"></a> **`treeNode.py`**: Defines a **game tree node** that represents a game state, including possible move nodes, as well as visit and win counts.
- <a id="algorithms"></a> **`algorithms.py`**: Contains the different **AI algorithms** for gameplay.
- <a id="game"></a> **`game.py`**: Manages the **Connect Four game** logic, including board state, turn-taking, and win conditions.
- <a id="config"></a> **`config.py`**: Handles **game setup** by parsing input files and configuring game parameters like the board layout, algorithms, and starting player.

## Contributing

We welcome contributions to the **Connect Four AI** project! Whether you want to add new features, fix bugs, or improve the documentation, your contributions are greatly appreciated.

### Issues and Feature Requests
If you find a bug or have a feature request, please [open an issue](https://github.com/christiandees/ConnectFour/issues) and provide a detailed description. We encourage contributions to improve the project, and we’ll be happy to review your ideas!

