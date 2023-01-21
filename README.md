# Sudoku-Project

This project represents a playable Sudoku game, taking advantage of a robust Sudoku solver that incorporates both backtracking and forward checking algorithms, as well as the pygame module and a set of 400 provided sudoku puzzles in a separate text file that my program opened and read through. Upon running the program, this project randomly selects one out of 400 games, and presents it, as well as various prompts and instructions for interacting with the game. 

Players can play through the game as normal, or take advantage of the built in solver tool by pressing ENTER to check their work. This game will then show a visual representation of the solver tool in action, present text indicating whether or not the board is correct/solvable thus far (if the player has inputted values), and correctly solving it if so.

In order to complete this project, I wrote an AI algorithm for solving any given sudoku puzzle, implementing basic backtracking and forward-checking algorithms. I also utilized the pygames module, and after finding a boilerplate tutorial for implementing pygames, successfully modified my code to be compatible in order to incorporate a visual and interactive component. 
