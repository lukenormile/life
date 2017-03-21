import sys
import curses
from curses import wrapper
import copy

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

# Minimum board width/height:
MIN_DIMENSION = 3

# How cells are represented internally.
DEAD = 0
ALIVE = 1

# How cells are formatted when printed.
DEAD_PRINTCHAR = 'O'
LIVE_PRINTCHAR = 'X'

# Configurable constants for behavior of cells.
MIN_STAY_ALIVE = 2
MAX_STAY_ALIVE = 3
MIN_COME_ALIVE = 3
MAX_COME_ALIVE = 3

def count_neighbors(board, x, y):
    left =  (x-1) % len(board)
    right = (x+1) % len(board)
    up =    (y-1) % len(board[0])
    down =  (y+1) % len(board[0])
    neighbors = board[left][up]  \
            + board[left] [y]    \
            + board[left] [down] \
            + board[x]    [up]   \
            + board[x]    [down] \
            + board[right][up]   \
            + board[right][y]    \
            + board[right][down]
    return neighbors

def update_cell(board, x, y):
    neighbors = count_neighbors(board, x, y)
    if board[x][y] == ALIVE:
        if neighbors < MIN_STAY_ALIVE or neighbors > MAX_STAY_ALIVE:
            return DEAD
        else:
            return ALIVE
    else:
        if neighbors < MIN_COME_ALIVE or neighbors > MAX_COME_ALIVE:
            return DEAD
        else:
            return ALIVE

def reset_board(board):


def step(board):
    new_board = copy.deepcopy(board)
    for x, col in enumerate(board):
        for y, cell in enumerate(col):
            new_board[x][y] = update_cell(board, x, y)
    return new_board

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

def switch_cell(board, x, y):
    if board[x][y] == ALIVE:
        board[x][y] = DEAD
    else:
        board[x][y] = ALIVE

def interact(stdscr, board):
    x = 0
    y = 0
    board_copy = board
    stdscr.move(y,x*2)
    while True:
        c = stdscr.getch()
        if c == curses.KEY_DOWN or c == ord('j'):
            y += 1
            stdscr.move(y,x*2)
        elif c == curses.KEY_UP or c == ord('k'):
            y -= 1
            stdscr.move(y,x*2)
        elif c == curses.KEY_LEFT or c == ord('h'):
            x -= 1
            stdscr.move(y,x*2)
        elif c == curses.KEY_RIGHT or c == ord('l'):
            x += 1
            stdscr.move(y,x*2)
        elif c == ord('s'):
            board_copy = copy.deepcopy(board)
            board = step(board)
            update_display(stdscr, board)
            stdscr.move(y,x*2)
        elif c == ord('u'):
            board = board_copy
            update_display(stdscr, board)
            stdscr.move(y,x*2)
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            switch_cell(board, x, y)
            update_display(stdscr, board)
            stdscr.move(y,x*2)
        elif c == ord('R'):
            main(stdscr)
        elif c == ord('q'):
            sys.exit()

# Get a board dimension value from the user.
def get_dimension(stdscr, name="width"):
    curses.echo() # Enable echoing of user input.
    while True:
        try:
            stdscr.clear()
            stdscr.addstr(0, 0, "Enter the board %s: " % name)
            value = int(stdscr.getstr())
            stdscr.clear()
            assert value >= MIN_DIMENSION
        except (ValueError, AssertionError):
            stdscr.addstr("Board %s must be at least %d.\n"
                    % (name, MIN_DIMENSION))
            continue
        curses.noecho()
        return value

def build_board(stdscr):
    board_x = get_dimension(stdscr, "width")
    board_y = get_dimension(stdscr, "height")

    board = [[0 for y in range(board_y)] for x in range(board_x)]
    return board

def main(stdscr):
    stdscr.clear()

    board = build_board(stdscr)
    while True:
        update_display(stdscr, board)
        interact(stdscr, board)

    stdscr.refresh()
    stdscr.getkey()

wrapper(main)
