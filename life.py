import sys
import curses
from curses import wrapper

DEAD_CELL = 'O'
LIVE_CELL = 'X'

# Prepare the board to be overwritten by returning cursor
# to the top of the board.
def reset_board(board):
    for row in board:
        sys.stdout.write("\033[F")

def print_board(board):
    for row in board:
        for cell in row:
            if cell:
                print(LIVE_CELL, end = ' ')
            else:
                print(DEAD_CELL, end = ' ')
        print()

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
