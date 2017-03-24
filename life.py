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

def step(board):
    new_board = copy.deepcopy(board)
    for x, col in enumerate(board):
        for y, cell in enumerate(col):
            new_board[x][y] = update_cell(board, x, y)
    return new_board

def update_info_window(alive, dead, info_window):
    info_window.clear()
    total = alive + dead
    alive_percent = (100 * alive/total)
    dead_percent  = (100 *  dead/total)
    alive_str = "%d alive (%3.2f%%)" % (alive, alive_percent)
    dead_str  = "%d dead (%3.2f%%)"  % (dead,  dead_percent)
    info_window.addstr(0, 0, alive_str)
    info_window.addstr(1, 0,  dead_str)
    info_window.refresh()

def update_display(board, display):
    board_window = display[1]
    alive = dead = 0;
    for x_index, x_val in enumerate(board):
        for y_index, y_val in enumerate(x_val):
            if y_val == ALIVE:
                board_window.addch(y_index,
                        (x_index * 2),
                        LIVE_PRINTCHAR,
                        curses.color_pair(2))
                alive += 1;
            else:
                board_window.addch(y_index,
                        (x_index * 2),
                        DEAD_PRINTCHAR,
                        curses.color_pair(3))
                dead += 1;
    board_window.refresh()
    info_window = display[2]
    update_info_window(alive, dead, info_window)

def switch_cell(board, x, y):
    if board[x][y] == ALIVE:
        board[x][y] = DEAD
    else:
        board[x][y] = ALIVE

def reset_board(board):
    for x in enumerate(board):
        for y in enumerate(col):
            board[x][y] = DEAD

def interact(board, display):
    stdscr = display[0]
    board_window = display[1]
    info_window = display[2]
    x = y = 0
    board_copy = board
    board_window.move(y,x*2)
    while True:
        c = board_window.getch()
        if c == curses.KEY_DOWN or c == ord('j'):
            y += 1
            board_window.move(y,x*2)
        elif c == curses.KEY_UP or c == ord('k'):
            y -= 1
            board_window.move(y,x*2)
        elif c == curses.KEY_LEFT or c == ord('h'):
            x -= 1
            board_window.move(y,x*2)
        elif c == curses.KEY_RIGHT or c == ord('l'):
            x += 1
            board_window.move(y,x*2)
        elif c == ord('s'):
            board_copy = copy.deepcopy(board)
            board = step(board)
            update_display(board, display)
            board_window.move(y,x*2)
        elif c == ord('u'):
            board = board_copy
            update_display(board, display)
            board_window.move(y,x*2)
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            switch_cell(board, x, y)
            update_display(board, display)
            board_window.move(y,x*2)
        elif c == ord('r'):
            reset_board(board)
            update_display(board, display)
            board_window.move(y,x*2)
        elif c == ord('R'):
            main(stdscr)
        elif c == ord('q'):
            sys.exit()

# Get a board dimension value from the user.
def get_dimension(window, label):
    curses.echo() # Enable echoing of user input.
    while True:
        try:
            window.clear()
            window.addstr(0, 0, "Enter the board %s: " % label)
            value = int(window.getstr())
            window.clear()
            assert value >= MIN_DIMENSION
        except (ValueError, AssertionError):
            window.addstr("Board %s must be at least %d.\n"
                    % (label, MIN_DIMENSION))
            continue
        curses.noecho()
        return value

def build_board(board_window):
    board_x = get_dimension(board_window, "width")
    board_y = get_dimension(board_window, "height")
    board = [[0 for y in range(board_y)] for x in range(board_x)]
    return board

def print_instructions(instruction_window):
    instruction_window.clear()
    instruction_1 = "Press 'q' to quit."
    instruction_2 = "Press 'r' to reset the board with the same dimensions."
    instruction_3 = "Press 'R' to reset the game completely"
    instruction_window.addstr(1, 0, instruction_1)
    instruction_window.addstr(2, 0, instruction_2)
    instruction_window.addstr(3, 0, instruction_3)
    instruction_window.refresh()

def init_colors():
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair((i + 1), i, -1)

def main(stdscr):
    init_colors()
    stdscr.clear()
    board = build_board(stdscr)
    stdscr.clear()
    stdscr.refresh()
    board_window = curses.newwin(len(board[0]), (len(board) * 2))
    info_window = curses.newwin(2, 25, 0, (len(board) * 2) + 1)
    instruction_window = curses.newwin(4, 53, 2, (len(board) * 2) + 1)
    print_instructions(instruction_window)
    display = (stdscr, board_window, info_window)
    while True:
        update_display(board, display)
        interact(board, display)

wrapper(main)
