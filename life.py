import sys
import curses
from curses import wrapper

# How cells are represented internally.
DEAD = 0
ALIVE = 1

# How cells are formatted when printed.
DEAD_PRINTCHAR = 'O'
LIVE_PRINTCHAR = 'X'

# Configurable constants for behavior of cells.
MIN_TO_STAY_ALIVE = 2
MAX_TO_STAY_ALIVE = 3
MIN_TO_COME_ALIVE = 3
MAX_TO_COME_ALIVE = 3

def print_board(board):
    for row in board:
        for cell in row:
            if cell:
                print(LIVE_PRINTCHAR, end = ' ')
            else:
                print(DEAD_PRINTCHAR, end = ' ')
        print()

def count_neighbors(board, x, y):
    neighbors = board[x-1][y-1] \
        + board[x-1][y]         \
        + board[x-1][y+1]       \
        + board[x][y-1]         \
        + board[x][y+1]         \
        + board[x+1][y-1]       \
        + board[x+1][y]         \
        + board[x+1][y+1]

def update_cell(board, x, y):
    neighbor_count = count_neighbors(board, x, y)
    if board[x][y] == DEAD:
        if neighbor_count >= MIN_TO_COME_ALIVE \
                and neighbor_count <= MAX_TO_COME_ALIVE:
                    return ALIVE
        else:
            return DEAD
    else:
        if neighbor_count >= MIN_TO_STAY_ALIVE \
                and neighbor_count <= MAX_TO_STAY_ALIVE:
                    return ALIVE
        else:
            return DEAD

def step(board):
    new_board = board
    for x in range(board_x):
        for y in range(board_y):
            update_cell(board, x, y)

# Get a board dimension value from the user.
def get_dimension(stdscr, name="width"):
    curses.echo() # Enable echoing of user input.
    while True:
        try:
            stdscr.addstr("Enter the board %s: " % name)
            value = int(stdscr.getstr())
            stdscr.clear()
            assert value > 0
        except (ValueError, AssertionError):
            stdscr.addstr("Please use a positive integer for board %s.\n"
                    % name)
            continue
        curses.noecho()
        return value

def build_board(stdscr):
    board_x = get_dimension(stdscr, "width")
    board_y = get_dimension(stdscr, "height")

    board = [[0 for x in range(board_x)] for y in range(board_y)]
    return board


def main(stdscr):
    stdscr.clear()

    board = build_board(stdscr)

    stdscr.refresh()
    stdscr.getkey()

wrapper(main)
