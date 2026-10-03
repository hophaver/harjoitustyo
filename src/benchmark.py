# benchmark script for measuring search performance across different depths
import time
from connect4 import generate_board, drop_piece
from ai import find_best_move, get_search_stats


def run_benchmark():
    print("=" * 60)
    print("Connect Four AI - Empirical Performance Benchmark")
    print("=" * 60)

    # set up a sample board with a few moves played
    board = generate_board()
    drop_piece(board, 3, "X")
    drop_piece(board, 3, "O")
    drop_piece(board, 2, "X")
    drop_piece(board, 4, "O")

    print(f"{'Depth':<8}{'Time (s)':<14}{'Nodes Explored':<18}{'TT Hits':<12}{'Best Move'}")
    print("-" * 60)

    for depth in range(1, 7):
        start_time = time.perf_counter()
        best_col = find_best_move(board, "X", depth=depth)
        elapsed = time.perf_counter() - start_time
        stats = get_search_stats()

        nodes = stats["nodes"]
        tt_hits = stats["tt_hits"]
        print(f"{depth:<8}{elapsed:<14.4f}{nodes:<18}{tt_hits:<12}{best_col + 1}")

    print("=" * 60)


if __name__ == "__main__":
    run_benchmark()
