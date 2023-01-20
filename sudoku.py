import sys
import copy
import statistics
import time
import random
import pygame
import numpy as np

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


def convert_arr(arr):
    arr = np.flip(arr)
    arr = arr.transpose()
    unpackaged = []
    board = {}
    for row in arr:
        for element in row:
            unpackaged.append(element)
    for i in ROW:
        for j in COL:
            board[i+j] = unpackaged.pop()
    return board


def convert_board(board):
    x = 0
    temp = []
    arr = []
    for element in board:
        if x == 9:
            x = 0
            arr.append(temp)
            temp = []
        x += 1
        temp.append(board[element])
    arr.append(temp)
    toReturn = np.asarray(arr)
    toReturn = toReturn.transpose()
    return toReturn


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
        return True
    next_val = selectNext(unsolved)
    possible_domain = unsolved[next_val]
    pygame.event.pump()
    
    del unsolved[next_val]
    for value in possible_domain:
        backup_board = copy.deepcopy(board)
        backup_unsolved = copy.deepcopy(unsolved)
        # white color background
        screen.fill((255, 255, 255))
        draw()
        solve_text()
        pygame.display.update()

        if checkValid(board, next_val, value):
            board[next_val] = value
            pygame.time.delay(5)
            global grid
            grid = convert_board(board)
            unsolved = updateDomain(next_val, value, unsolved)
            if isValidDomain(unsolved):
                valid_board = backtrack(board, unsolved)
                if valid_board is True:
                    return True
        board = backup_board
        unsolved = backup_unsolved
    pygame.time.delay(5)
    grid = convert_board(backup_board)
    screen.fill((255, 255, 255))
    draw()
    solve_text()
    pygame.display.update()
    pygame.time.delay(15)
    return False


def solve(board):
    unsolved_board = initUnsolved(board)
    solvable = backtrack(board, unsolved_board)
    return solvable


def get_cord(pos):
    global x
    x = pos[0] // dif
    global y
    y = pos[1] // dif


# Highlight the cell selected
def draw_box():
    for i in range(2):
        pygame.draw.line(screen, (255, 0, 0), (x * dif - 3, (y + i) * dif), (x * dif + dif + 3, (y + i) * dif), 7)
        pygame.draw.line(screen, (255, 0, 0), ((x + i) * dif, y * dif), ((x + i) * dif, y * dif + dif), 7)


# Function to draw required lines for making Sudoku grid
def draw():
    # Draw the lines
    for i in range(9):
        for j in range(9):
            if start_grid[i][j] != 0:
                # Fill blue color in already numbered grid
                pygame.draw.rect(screen, (0, 153, 153), (i * dif, j * dif, dif + 1, dif + 1))

                # Fill grid with default numbers specified
                text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (i * dif + 15, j * dif + 15))

    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0 and start_grid[i][j] == 0:
                # Fill blue color in already numbered grid
                pygame.draw.rect(screen, (137, 207, 240), (i * dif, j * dif, dif + 1, dif + 1))

                # Fill grid with default numbers specified
                text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (i * dif + 15, j * dif + 15))
    # Draw lines horizontally and verticallyto form grid
    for i in range(10):
        if i % 3 == 0:
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)


# Fill value entered in cell
def draw_val(val):
    text1 = font1.render(str(val), 1, (0, 0, 0))
    screen.blit(text1, (x * dif + 15, y * dif + 15))


# Raise error when wrong value entered
def raise_error1():
    text1 = font1.render("WRONG !!!", 1, (0, 0, 0))
    screen.blit(text1, (20, 570))


def raise_error2():
    text1 = font1.render("Wrong !!! Not a valid Key", 1, (0, 0, 0))
    screen.blit(text1, (20, 570))


# Check if the value entered in board is valid
def valid(m, i, j, val):
    for it in range(9):
        if m[i][it] == val:
            return False
        if m[it][j] == val:
            return False
    it = i // 3
    jt = j // 3
    for i in range(it * 3, it * 3 + 3):
        for j in range(jt * 3, jt * 3 + 3):
            if m[i][j] == val:
                return False
    return True


# Display instruction for the game
def instruction():
    text1 = font2.render("PRESS D TO RESET TO DEFAULT", 1, (0, 0, 0))
    text2 = font2.render("PRESS F TO TRY NEW BOARD", 1, (0, 0, 0))
    text3 = font2.render("ENTER VALUES OR PRESS ENTER TO SOLVE", 1, (0, 0, 0))
    screen.blit(text1, (20, 520))
    screen.blit(text2, (20, 540))
    screen.blit(text3, (20, 560))

def solve_text():
    text3 = font2.render("Solving...", 1, (0, 0, 0))
    screen.blit(text3, (20, 520))

# Display options when solved
def result():
    text1 = font1.render("SUCCESS!", 1, (0, 0, 0))
    text2 = font2.render("PRESS D TO RETRY OR PRESS F FOR NEW BOARD", 1, (0, 0, 0))
    screen.blit(text1, (20, 520))
    screen.blit(text2, (20, 560))

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
    puzzle_list = sudoku_list.split("\n")

    # solved_board = solve(initial_board)
    # print_board(solved_board)
    # initialize game here, with solved_board kept track of, but also with current, "playable", board as the one actually shown

    # initialise the pygame font
    pygame.font.init()

    # Total window
    x_size = 500
    y_size = 600
    screen = pygame.display.set_mode((x_size, y_size))

    # Title and Icon
    pygame.display.set_caption("SUDOKU SOLVER USING BACKTRACKING")
    # img = pygame.image.load('icon.png')
    # pygame.display.set_icon(img)

    x = 0
    y = 0
    dif = x_size / 9
    val = 0

    # Load fonts
    font1 = pygame.font.SysFont("arial", 28)
    font2 = pygame.font.SysFont("arial", 20)

    # print_board(solved_board)

    run = True
    flag1 = 0
    flag2 = 0
    rs = 0
    error = 0
    global grid
    global start_grid
    # The loop thats keep the window running

    line = puzzle_list[randPuzzle]
    initial_board = {ROW[r] + COL[c]: int(line[9 * r + c])
                     for r in range(9) for c in range(9)}

    playable_board = convert_board(initial_board)
    grid = playable_board.copy()
    start_grid = playable_board.copy()

    while run:

        # White color background
        screen.fill((255, 255, 255))
        # Loop through the events stored in event.get()
        for event in pygame.event.get():
            # Quit the game window
            if event.type == pygame.QUIT:
                run = False
            # Get the mouse position to insert number
            if event.type == pygame.MOUSEBUTTONDOWN:
                flag1 = 1
                pos = pygame.mouse.get_pos()
                get_cord(pos)
            # Get the number to be inserted if key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x -= 1
                    flag1 = 1
                if event.key == pygame.K_RIGHT:
                    x += 1
                    flag1 = 1
                if event.key == pygame.K_UP:
                    y -= 1
                    flag1 = 1
                if event.key == pygame.K_DOWN:
                    y += 1
                    flag1 = 1
                if event.key == pygame.K_1:
                    val = 1
                if event.key == pygame.K_2:
                    val = 2
                if event.key == pygame.K_3:
                    val = 3
                if event.key == pygame.K_4:
                    val = 4
                if event.key == pygame.K_5:
                    val = 5
                if event.key == pygame.K_6:
                    val = 6
                if event.key == pygame.K_7:
                    val = 7
                if event.key == pygame.K_8:
                    val = 8
                if event.key == pygame.K_9:
                    val = 9
                if event.key == pygame.K_RETURN:
                    flag2 = 1
                    flag1 = 0
                # If D is pressed reset the board to default
                if event.key == pygame.K_d:
                    rs = 0
                    error = 0
                    flag2 = 0
                    grid = playable_board
                    playable_board = playable_board.copy()
                if event.key == pygame.K_f:
                    rs = 0
                    error = 0
                    flag2 = 0
                    randPuzzle = random.randint(1, 400)
                    line = puzzle_list[randPuzzle]
                    initial_board = {ROW[r] + COL[c]: int(line[9 * r + c])
                                     for r in range(9) for c in range(9)}

                    playable_board = convert_board(initial_board)
                    grid = playable_board.copy()
                    start_grid = playable_board.copy()
                    continue
        if flag2 == 1:
            solvable_board = convert_arr(grid)
            if solve(solvable_board) == False:
                error = 1
            else:
                rs = 1
            flag2 = 0
        if val != 0:
            draw_val(val)
            # print(x)
            # print(y)
            if valid(grid, int(x), int(y), val) == True:
                grid[int(x)][int(y)] = val
                flag1 = 0
            else:
                grid[int(x)][int(y)] = 0
                raise_error2()
            val = 0

        if error == 1:
            raise_error1()
        if rs == 1:
            screen.fill((255, 255, 255))
            result()
        draw()
        if flag1 == 1:
            draw_box()
        if rs != 1:
            instruction()

        # Update window
        pygame.display.update()

    # Quit pygame window
    pygame.quit()
