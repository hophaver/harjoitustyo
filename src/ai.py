# minimax for connect 4
#
# naming: "player" is always the bot, "opponent" is always the human.
# connect4.py calls find_best_move(board, BOT_PIECE) so player = bot.

from connect4 import (
    ROWS,
    COLUMNS,
    drop_piece,
    undo_move,
    column_is_full,
    get_valid_moves,
    check_winner,
    board_full,
)

# Move ordering: evaluating center columns first yields far earlier cutoffs in alpha-beta pruning
COLUMN_ORDER = [3, 2, 4, 1, 5, 0, 6]

def get_ordered_moves(board):
    return [c for c in COLUMN_ORDER if not column_is_full(board, c)]


# score one 4-slot line
# player(bot)'s lines are good, opponent(human)'s near-wins are bad

def evaluate_window(window, player, opponent):
    score = 0

    player_count = window.count(player)
    opponent_count = window.count(opponent)
    empty_count = window.count(" ")

    # bot's own threats
    if player_count == 4:
        score += 1000          # bot already won this line
    elif player_count == 3 and empty_count == 1:
        score += 10            # one more move wins
    elif player_count == 2 and empty_count == 2:
        score += 2             # good

    # human's threats hurt the bot
    if opponent_count == 3 and empty_count == 1:
        score -= 20            # opponent next could win

    return score


# score the whole board, seen from the bot's side
# higher = better for bot, lower/negative = better for human

def evaluate_board(board, player):
    opponent = "O" if player == "X" else "X"
    score = 0

    # extra points for controlling the middle column
    center_column = [board[r][COLUMNS // 2] for r in range(ROWS)]
    score += center_column.count(player) * 3

    # horizontal windows (left to right)
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            window = [board[r][c + i] for i in range(4)]
            score += evaluate_window(window, player, opponent)

    # vertical windows (top to bottom)
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            window = [board[r + i][c] for i in range(4)]
            score += evaluate_window(window, player, opponent)

    # diagonal windows going up-right (/)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window, player, opponent)

    # diagonal windows going down-right (\)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, player, opponent)

    return score


# Transposition table node types
EXACT = 0
LOWERBOUND = 1
UPPERBOUND = 2

# Transposition table: maps (board_tuple, is_maximizing) -> (depth, flag, score)
transposition_table = {}

def board_to_tuple(board):
    return tuple(tuple(row) for row in board)

def clear_transposition_table():
    transposition_table.clear()


# recursively search the game tree with alpha-beta pruning and transposition table caching
# is_maximizing = True when it's the bot's turn, False when it's the human's
# alpha = best score maximizing player can guarantee so far
# beta = best score minimizing player can guarantee so far
# last_row / last_column tell us where the most recent piece was dropped

def minimax(board, depth, alpha, beta, is_maximizing, player, opponent, last_row=None, last_column=None):
    # if there was a last move, first check if it just won the game
    if last_row is not None and last_column is not None:
        if is_maximizing:
            # human just moved, so the winner is the human
            if check_winner(board, last_row, last_column, opponent):
                return -10000 - depth
        else:
            # bot just moved, so the winner is the bot
            if check_winner(board, last_row, last_column, player):
                return 10000 + depth

    # no moves left so it is a tie
    if board_full(board):
        return 0

    # ran out of search depth return the heuristic value
    if depth == 0:
        return evaluate_board(board, player)

    # check transposition table
    alpha_orig = alpha
    beta_orig = beta
    board_key = (board_to_tuple(board), is_maximizing)
    if board_key in transposition_table:
        cached_depth, cached_flag, cached_score = transposition_table[board_key]
        if cached_depth >= depth:
            if cached_flag == EXACT:
                return cached_score
            elif cached_flag == LOWERBOUND:
                alpha = max(alpha, cached_score)
            elif cached_flag == UPPERBOUND:
                beta = min(beta, cached_score)
            if alpha >= beta:
                return cached_score

    valid_moves = get_ordered_moves(board)

    # bot turn: pick the move giving the highest score
    if is_maximizing:
        best = -float("inf")
        for column in valid_moves:
            row = drop_piece(board, column, player)
            value = minimax(board, depth - 1, alpha, beta, False, player, opponent, row, column)
            undo_move(board, column)
            if value > best:
                best = value
            alpha = max(alpha, best)
            if beta <= alpha:
                break  # Beta cutoff
    # human turn: pick the move giving the lowest score
    else:
        best = float("inf")
        for column in valid_moves:
            row = drop_piece(board, column, opponent)
            value = minimax(board, depth - 1, alpha, beta, True, player, opponent, row, column)
            undo_move(board, column)
            if value < best:
                best = value
            beta = min(beta, best)
            if beta <= alpha:
                break  # alpha cutoff

    # record position in transposition table
    if best <= alpha_orig:
        flag = UPPERBOUND
    elif best >= beta_orig:
        flag = LOWERBOUND
    else:
        flag = EXACT
    transposition_table[board_key] = (depth, flag, best)

    return best


# difficulty presets: depth determines how many turns ahead the bot calculates
DIFFICULTY_LEVELS = {
    "1": 3,  # Easy
    "2": 5,  # Medium (default)
    "3": 7,  # Hard
}


# try every column, see how good it is, return the best one for the bot
# depth = how many moves ahead the bot thinks
# player is the bot's piece (passed from connect4.py)

def find_best_move(board, player, depth=5):
    clear_transposition_table()
    opponent = "O" if player == "X" else "X"
    valid_moves = get_ordered_moves(board)

    if not valid_moves:
        return None  # board is full, no move to make

    best_score = -float("inf")
    best_column = valid_moves[0]
    alpha = -float("inf")
    beta = float("inf")

    for column in valid_moves:
        row = drop_piece(board, column, player)
        score = minimax(board, depth - 1, alpha, beta, False, player, opponent, row, column)
        undo_move(board, column)
        if score > best_score:
            best_score = score
            best_column = column
        alpha = max(alpha, best_score)

    return best_column