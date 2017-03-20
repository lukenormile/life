import sys

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
def get_dimension(name="width"):
    while True:
        try:
            value = int(input("Board %s: " % name))
            assert value > 0
        except (ValueError, AssertionError):
            print("Please use a positive integer for board %s.", name)
            continue
        return value

def build_board():
    board_x = get_dimension("width")
    board_y = get_dimension("height")

    board = [[0 for x in range(board_x)] for y in range(board_y)]
    print_board(board)
    reset_board(board)
    print_board(board)
    return board


def main():
    board = build_board()

if __name__ == "__main__":
    main()
