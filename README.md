# Sudoku-solver
This project is a Sudoku solver and generator implemented in Python. The program can solve any given Sudoku puzzle using a backtracking algorithm and generate new Sudoku puzzles with varying levels of difficulty.
Code Overview
display(bo): Function to print the Sudoku board.
find(bo): Function to find the next empty cell in the board.
valid(bo, value, pos): Function to check if placing a value in a specific position is valid.
Solve(bo): Recursive function to solve the Sudoku puzzle.
fill_board(bo): Function to fill the board completely with a valid Sudoku solution.
remove_elements(bo, attempts): Function to remove a specified number of elements from the filled board to create a puzzle.
generate_sudoku(): Function to generate a new Sudoku puzzle.
