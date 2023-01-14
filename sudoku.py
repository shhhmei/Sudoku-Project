import sys
import copy
import statistics
import time
import random
#import pygame

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

def convert_board(line):
    x = 9
    board = [list(line[y - x:y]) for y in range(x, len(line) + x, x)]
    grid = []
    for element in board:
        res = [eval(i) for i in element]
        grid.append(res)
    return grid

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
    # Read boards from source.
    src_filename = 'sudokus_start.txt'
    try:
        srcfile = open(src_filename, "r")
        sudoku_list = srcfile.read()
    except:
        print("Error reading the sudoku file %s" % src_filename)
        exit()

    # Solve each board using backtracking
    randPuzzle = random.randint(1, 400)
    currPuzzle = 0
    for line in sudoku_list.split("\n"):
        currPuzzle += 1
        if currPuzzle != randPuzzle:
            continue

        board = {ROW[r] + COL[c]: int(line[9 * r + c])
                 for r in range(9) for c in range(9)}
        
        grid = convert_board(line)
        
        print(board)
        print(grid)
        
        #print_board(board)
        
        #solved_board = backtracking(board)

        #initialize game here, with solved_board kept track of, but also with current, "playable", board as the one actually shown

        #print_board(solved_board)

        