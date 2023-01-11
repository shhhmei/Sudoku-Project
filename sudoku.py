#!/usr/bin/env python
# coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import copy
import statistics
import time
import random

ROW = "ABCDEFGHI"
COL = "123456789"

def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def initUnsolved(board):
    unsolved_board = {}
    for key in board:
        if board[key] == 0:
            unsolved_board[key] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for key in board:
        if board[key] != 0:
            updateDomain(key, board[key], unsolved_board)
    return unsolved_board


def updateDomain(idx, val, unsolved):
    subgroupsROW = {"A": ["A", "B", "C"], "B": ["A", "B", "C"], "C": ["A", "B", "C"], "D": ["D", "E", "F"],
                    "E": ["D", "E", "F"], "F": ["D", "E", "F"], "G": ["G", "H", "I"], "H": ["G", "H", "I"],
                    "I": ["G", "H", "I"]}
    subgroupsCOL = {"1": ["1", "2", "3"], "2": ["1", "2", "3"], "3": ["1", "2", "3"], "4": ["4", "5", "6"],
                    "5": ["4", "5", "6"], "6": ["4", "5", "6"], "7": ["7", "8", "9"], "8": ["7", "8", "9"],
                    "9": ["7", "8", "9"]}
    for key in unsolved:
        if key == idx:
            continue
        if (key[0] == idx[0]) or (key[1] == idx[1]) or (
                key[0] in subgroupsROW[idx[0]] and key[1] in subgroupsCOL[idx[1]]):
            if val in unsolved[key]:
                unsolved[key].remove(val)
    return unsolved


def checkValid(board, idx, val):
    subgroupsROW = {"A": ["A", "B", "C"], "B": ["A", "B", "C"], "C": ["A", "B", "C"], "D": ["D", "E", "F"],
                    "E": ["D", "E", "F"], "F": ["D", "E", "F"], "G": ["G", "H", "I"], "H": ["G", "H", "I"],
                    "I": ["G", "H", "I"]}
    subgroupsCOL = {"1": ["1", "2", "3"], "2": ["1", "2", "3"], "3": ["1", "2", "3"], "4": ["4", "5", "6"],
                    "5": ["4", "5", "6"], "6": ["4", "5", "6"], "7": ["7", "8", "9"], "8": ["7", "8", "9"],
                    "9": ["7", "8", "9"]}
    for i in ROW:
        for j in COL:
            temp = i + j
            if i == idx[0] or j == idx[1] or (i in subgroupsROW[idx[0]] and j in subgroupsCOL[idx[1]]):
                if board[temp] == val:
                    return False
    return True


def isValidDomain(unsolved):
    for key in unsolved:
        if len(unsolved[key]) == 0:
            return False
    return True


def selectNext(unsolved_board):
    curr_min = 10
    curr_key = ""
    for key in unsolved_board:
        if unsolved_board[key] is None:
            return []
        if len(unsolved_board[key]) < curr_min:
            curr_key = key
            curr_min = len(unsolved_board[key])
    return curr_key


def backtrack(board, unsolved):
    if len(unsolved) == 0:
        return board
    next_val = selectNext(unsolved)
    possible_domain = unsolved[next_val]

    del unsolved[next_val]
    for value in possible_domain:
        backup_board = copy.deepcopy(board)
        backup_unsolved = copy.deepcopy(unsolved)
        print_board(backup_board)
        if checkValid(board, next_val, value):
            board[next_val] = value
            unsolved = updateDomain(next_val, value, unsolved)
            if isValidDomain(unsolved):
                result = backtrack(board, unsolved)
                if result != []:
                    return result
        board = backup_board
        unsolved = backup_unsolved
    return []


def backtracking(board):
    unsolved_board = initUnsolved(board)
    solved_board = backtrack(board, unsolved_board)
    return solved_board


if __name__ == '__main__':
    if len(sys.argv) > 1:

        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = {ROW[r] + COL[c]: int(sys.argv[1][9 * r + c])
                 for r in range(9) for c in range(9)}

        print_board(board)
        solved_board = backtracking(board)
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        print_board(solved_board)
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py
        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        mean = 0
        min_time = sys.maxsize
        max_time = 0
        running_list = []

        counter = 0
        # Solve each board using backtracking
        randPuzzle = random.randint(1, 400)
        currPuzzle = 0
        for line in sudoku_list.split("\n"):
            currPuzzle += 1
            if len(line) < 9:
                continue
            if currPuzzle != randPuzzle:
                continue
            
            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = {ROW[r] + COL[c]: int(line[9 * r + c])
                     for r in range(9) for c in range(9)}

            #print_board(board)

            start_time = time.time()

            # Solve with backtracking
            solved_board = backtracking(board)

            #print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

            end_time = time.time()
            curr = end_time - start_time
            counter += 1

            if curr > max_time:
                max_time = curr

            if curr < min_time:
                min_time = curr

            mean += curr
            running_list.append(curr)

        #print("Max time =", max_time)
        #print("Min time =", min_time)
        #print("Mean time =", mean/counter)
        #print("Standard Deviation =", statistics.stdev(running_list))

        print("Solved", counter, "puzzles.")
        #print("Finishing all boards in file.")