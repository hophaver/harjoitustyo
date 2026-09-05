import sys  # for checking --test flag
import unittest  # for unit tests at bottom of file


ROWS = 6
COLUMNS = 7


# generate board

def generate_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]


# print board
# column numbers, walls and bottom

def print_board(board):
    print("\n 1 2 3 4 5 6 7")
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLUMNS * 2 + 1))


# drop pieces

def drop_piece(board, column, player):
    for r in range(ROWS - 1, -1, -1):
        if board[r][column] == " ":
            board[r][column] = player
            return r
    return None


# check if move is valid

def column_is_full(board, column):
    return board[0][column] != " "

def valid_move(board, column):
    return 0 <= column < COLUMNS and not column_is_full(board, column)



# 4 valid directions ƒor a win: up-down, left-right, down-right, down-left

directions = [(1, 0), (0, 1), (1, 1), (1, -1)]


# check if last move won

def check_winner(board, row, col, player):
    for dr, dc in directions:
        count = 1
        for sign in (1, -1):
            r, c = row + sign * dr, col + sign * dc
            while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player:
                count += 1
                r += sign * dr
                c += sign * dc
        if count >= 4:
            return True
    return False


# check if board is full

def board_full(board):
    return all(board[0][c] != " " for c in range(COLUMNS))


# handle one human players turn until a valid column is given

def person_turn(board, player):
    while True:
        try:
            col = int(input(f"Player {player}, pick a column (1-7): ")) - 1
        except ValueError:
            continue
        if valid_move(board, col):
            return col
        print("invalid move")


# mode select

def main():
    mode = input("bot (1) or pvp (2) ?: ").strip().upper()
    players = ["X", "O"]
    ai_turn = False
    if mode == "1":
        print("playing against bot (not yet)")
    elif mode == "2":
        pass
    else:
        print("invalid choice -> defaulting to pvp")

    board = generate_board()
    print_board(board)

    turn = 0
    while True:
        player = players[turn % 2]
        col = person_turn(board, player)
        row = drop_piece(board, col, player)
        print_board(board)

        if check_winner(board, row, col, player):
            print(f"player {player} won")
            return
        if board_full(board):
            print("draw")
            return
        turn += 1


# unit tests with --test flag

class TestBoard(unittest.TestCase):
    # a horizontal row of X should be a win
    def test_drop_and_winner_horizontal(self):
        board = generate_board()
        board[0][0] = "X"
        board[0][1] = "X"
        board[0][2] = "X"
        board[0][3] = "X"
        self.assertEqual(check_winner(board, 0, 3, "X"), True)

    # dropping 6 pieces into a column fills it
    def test_column_fill(self):
        board = generate_board()
        for _ in range(6):
            drop_piece(board, 0, "X")
        self.assertTrue(column_is_full(board, 0))

    # empty board should never report a winner
    def test_no_winner_empty(self):
        board = generate_board()
        self.assertFalse(check_winner(board, 0, 0, "X"))


if __name__ == "__main__":
    if "--test" in sys.argv:
        sys.argv.remove("--test")
        unittest.main()
    else:
        main()