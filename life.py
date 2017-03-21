import sys
import curses
from curses import wrapper

# Cell values as represented internally.
DEAD = 0
ALIVE = 1

# Cell values as printed to the screen.
LIVE_PRINTCHAR = 'X'
DEAD_PRINTCHAR = 'O'

# Values for determining the next state of a cell.
MIN_STAY_ALIVE = 2
MAX_STAY_ALIVE = 3
MIN_COME_ALIVE = 3
MAX_COME_ALIVE = 3

# Prepare the board to be overwritten by returning cursor
# to the top of the board.
def reset_board(board):
    for row in board:
        sys.stdout.write("\033[F")

def update_display(stdscr, board):
    for x_index, x_val in enumerate(board):
        for y_index, y_val in enumerate(x_val):
            if y_val == ALIVE:
                stdscr.addstr(y_index,
                        (x_index * 2),
                        LIVE_PRINTCHAR)
            else:
                stdscr.addstr(y_index,
                        (x_index * 2),
                        DEAD_PRINTCHAR)

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

    board = [[0 for y in range(board_y)] for x in range(board_x)]
    return board

def count_neighbors(board, x, y):
    neighbors = board[x-1][y-1] \
            + board[x-1][y  ]   \
            + board[x-1][y+1]   \
            + board[x  ][y-1]   \
            + board[x  ][y+1]   \
            + board[x+1][y-1]   \
            + board[x+1][y  ]   \
            + board[x+1][y+1]
    return neighbors

def update_cell(board, x, y):
    board[x][y] = cell
    neighbors = count_neighbors(board, x, y)
    if cell == ALIVE:
        if neighbors < STAY_ALIVE_MIN or neighbors > STAY_ALIVE_MAX:
            return DEAD
        else:
            return ALIVE
    else:
        if neighbors < COME_ALIVE_MIN or neighbors > COME_ALIVE_MAX:
            return DEAD
        else:
            return ALIVE

def step(board):
    next_board = board
    for x_index, col in enumerate(board):
        for y_index, cell in enumerate(col):
            next_board[x_index][y_index] = update_cell(board, x_index, y_index)
    return next_board

def main(stdscr):
    stdscr.clear()

    board = build_board(stdscr)
    while True:
        update_display(stdscr, board)

    stdscr.refresh()
    stdscr.getkey()

wrapper(main)
