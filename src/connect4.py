
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


def undo_move(board, column):
    for r in range(ROWS):
        if board[r][column] != " ":
            board[r][column] = " "
            return r
    return None


# check if move is valid

def column_is_full(board, column):
    return board[0][column] != " "

def valid_move(board, column):
    return 0 <= column < COLUMNS and not column_is_full(board, column)

def get_valid_moves(board):
    return [c for c in range(COLUMNS) if not column_is_full(board, c)]



# 4 valid directions ƒor a win: up-down, left-right, down-right, down-left

directions = [(1, 0), (0, 1), (1, 1), (1, -1)]


# check if last move won

def check_winner(board, row, column, player):
    for dr, dc in directions:
        count = 1
        for sign in (1, -1):
            r, c = row + sign * dr, column + sign * dc
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


# one VALID player move

def person_turn(board, player):
    while True:
        try:
            column = int(input(f"Player {player}, pick a column (1-7): ")) - 1
        except ValueError:
            continue
        if valid_move(board, column):
            return column
        print("invalid move")


# bot moves

def bot_turn(board, player, depth=5):
    from ai import find_best_move
    print(f"Bot ({player}) is thinking...")
    return find_best_move(board, player, depth)


# mode select

def main():
    mode = input("bot (1) or pvp (2) ?: ").strip().upper()
    players = ["X", "O"]
    
    ai = None
    depth = 5

    if mode == "1":
        ai = "O"  # bot plays after player
        print("playing against bot")
        from ai import DIFFICULTY_LEVELS
        diff = input("select difficulty - 1: Easy, 2: Medium, 3: Hard (default: 2): ").strip()
        depth = DIFFICULTY_LEVELS.get(diff, 5)
    elif mode == "2":
        pass
    else:
        print("invalid choice -> defaulting to pvp")

    board = generate_board()
    print_board(board)

    turn = 0
    while True:
        player = players[turn % 2]
        if player == ai:
            column = bot_turn(board, player, depth)
        else:
            column = person_turn(board, player)
        row = drop_piece(board, column, player)
        print_board(board)

        if check_winner(board, row, column, player):
            if player == ai:
                print(f"bot ({player}) won")
            else:
                print(f"player ({player}) won")
            return
        if board_full(board):
            print("draw")
            return
        turn += 1


if __name__ == "__main__":
    main()