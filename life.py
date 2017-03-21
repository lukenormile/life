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

# Minimum board width/height:
MIN_DIMENSION = 3

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

def switch_cell(board, x, y):
    if board[x][y] == ALIVE:
        board[x][y] = DEAD
    else:
        board[x][y] = ALIVE

def update_cell(board, x, y):
    cell = board[x][y]
    neighbors = count_neighbors(board, x, y)
    if cell == ALIVE:
        if neighbors < MIN_STAY_ALIVE or neighbors > MAX_STAY_ALIVE:
            return DEAD
        else:
            return ALIVE
    else:
        if neighbors < MIN_COME_ALIVE or neighbors > MAX_COME_ALIVE:
            return DEAD
        else:
            return ALIVE

def step(board):
    next_board = board
    for x_index, col in enumerate(board):
        for y_index, cell in enumerate(col):
            next_board[x_index][y_index] = update_cell(board, x_index, y_index)
    return next_board

def interact(stdscr, board):
    x = 0
    y = 0
    stdscr.move(y,x*2)
    while True:
        c = stdscr.getch()
        if c == curses.KEY_DOWN:
            y += 1
            stdscr.move(y,x*2)
        elif c == curses.KEY_UP:
            y -= 1
            stdscr.move(y,x*2)
        elif c == curses.KEY_LEFT:
            x -= 1
            stdscr.move(y,x*2)
        elif c == curses.KEY_RIGHT:
            x += 1
            stdscr.move(y,x*2)
        elif c == ord('s'):
            step(board)
            update_display(stdscr, board)
            stdscr.move(y,x*2)
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            switch_cell(board, x, y)
            update_display(stdscr, board)
            stdscr.move(y,x*2)
        elif c == ord('q'):
            sys.exit()

def main(stdscr):
    stdscr.clear()

    board = build_board(stdscr)
    while True:
        update_display(stdscr, board)
        interact(stdscr, board)

    stdscr.refresh()
    stdscr.getkey()

wrapper(main)
