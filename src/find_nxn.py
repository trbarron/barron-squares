"""
find_nxn.py — Generalized Barron Square finder for any order k.

Recall: a Barron Square of order k is a (4k × 4k) matrix.

For small k:
  k=1 → 4×4:   search space 9^4 ≈ 6.6×10^3   (trivial)
  k=2 → 8×8:   search space 9^16 ≈ 1.9×10^15  (need smart search)
  k=4 → 16×16: search space 9^64 ≈ 10^61      (need principled approach)

For k=4 and beyond, random search / constraint propagation / SAT solvers
are the practical path.  This module provides:
  1. A randomized search for k≥2
  2. Constraint propagation (arc consistency) for exact search
  3. Validation of candidate matrices

Usage:
    python src/find_nxn.py --k 4 --method random --trials 100000
"""

import random
import argparse
from barron_core import build_matrix, is_valid_barron, display, to_digits, from_digits
from itertools import product as iproduct


# ---------------------------------------------------------------------------
# Random search
# ---------------------------------------------------------------------------

def random_corners(k: int) -> tuple:
    """Sample random corner blocks (all nonzero digits)."""
    flat = [random.randint(1, 9) for _ in range(4 * k * k)]
    def block(start):
        return [flat[start + r * k: start + (r+1) * k] for r in range(k)]
    stride = k * k
    return block(0), block(stride), block(2*stride), block(3*stride)


def random_search(k: int, trials: int = 1_000_000,
                  verbose: bool = True) -> list[list[list[int]]]:
    """
    Search for valid Barron Squares of order k by random corner sampling.
    Not guaranteed to find all squares; useful for k≥3.
    """
    results = []
    found_set = set()
    for t in range(trials):
        tl, tr, bl, br = random_corners(k)
        M = build_matrix(tl, tr, bl, br, k)
        if M is not None:
            key = tuple(v for row in M for v in row)
            if key not in found_set:
                found_set.add(key)
                results.append(M)
                if verbose:
                    print(f"  Trial {t+1:,}: found square #{len(results)}")
    if verbose:
        print(f"  Completed {trials:,} trials, found {len(results)} distinct squares.")
    return results


# ---------------------------------------------------------------------------
# Exhaustive search for small k with pruning
# ---------------------------------------------------------------------------

def exhaustive_k1() -> list[list[list[int]]]:
    """Exhaustive search for k=1 (4×4)."""
    results = []
    for a, b, c, d in iproduct(range(1, 10), repeat=4):
        M = build_matrix([[a]], [[b]], [[c]], [[d]], k=1)
        if M is not None:
            results.append(M)
    return results


# ---------------------------------------------------------------------------
# Constraint propagation approach for 8×8
# ---------------------------------------------------------------------------

def constraint_search_k2() -> list[list[list[int]]]:
    """
    Exhaustive search for k=2 (8×8) with layered pruning.
    The corner blocks are 2×2 each (4 values each, 16 total).
    We enumerate in order TL → TR → BL → BR, pruning after each block.
    """
    from barron_core import to_digits, from_digits

    k = 2
    n = 8
    results = []

    def compute_row_mid(row_left_digits, row_right_digits):
        L = from_digits(row_left_digits)
        R = from_digits(row_right_digits)
        return to_digits(L * R, 4)

    # Enumerate corner blocks
    flat_blocks = list(iproduct(range(1, 10), repeat=4))

    for tl_flat in flat_blocks:
        tl = [list(tl_flat[:2]), list(tl_flat[2:])]

        for tr_flat in flat_blocks:
            tr = [list(tr_flat[:2]), list(tr_flat[2:])]

            # Compute rows 0 and 1 middles
            r0m = compute_row_mid([tl[0][0], tl[0][1]], [tr[0][0], tr[0][1]])
            r1m = compute_row_mid([tl[1][0], tl[1][1]], [tr[1][0], tr[1][1]])

            # All cells in rows 0–1 are edge cells (must be nonzero)
            if 0 in r0m or 0 in r1m:
                continue

            for bl_flat in flat_blocks:
                bl = [list(bl_flat[:2]), list(bl_flat[2:])]

                # Col 0 inner (rows 2–5, col 0): top=10*tl[0][0]+tl[1][0], bot=10*bl[0][0]+bl[1][0]
                c0_top = 10 * tl[0][0] + tl[1][0]
                c0_bot = 10 * bl[0][0] + bl[1][0]
                c0_inner = to_digits(c0_top * c0_bot, 4)

                c1_top = 10 * tl[0][1] + tl[1][1]
                c1_bot = 10 * bl[0][1] + bl[1][1]
                c1_inner = to_digits(c1_top * c1_bot, 4)

                # Cols 0 and 1 are edge cols; rows 2–5 ∩ edge cols = edge cells
                if 0 in c0_inner or 0 in c1_inner:
                    continue

                for br_flat in flat_blocks:
                    br = [list(br_flat[:2]), list(br_flat[2:])]

                    # Rows 6 and 7 middles
                    r6m = compute_row_mid([bl[0][0], bl[0][1]], [br[0][0], br[0][1]])
                    r7m = compute_row_mid([bl[1][0], bl[1][1]], [br[1][0], br[1][1]])
                    if 0 in r6m or 0 in r7m:
                        continue

                    # Cols 6 and 7 inner rows
                    c6_top = 10 * tr[0][0] + tr[1][0]
                    c6_bot = 10 * br[0][0] + br[1][0]
                    c6_inner = to_digits(c6_top * c6_bot, 4)

                    c7_top = 10 * tr[0][1] + tr[1][1]
                    c7_bot = 10 * br[0][1] + br[1][1]
                    c7_inner = to_digits(c7_top * c7_bot, 4)

                    if 0 in c6_inner or 0 in c7_inner:
                        continue

                    # Inner rows 2–5 middles from row constraint
                    inner_rows = []
                    ok = True
                    for ri in range(4):
                        left  = 10 * c0_inner[ri] + c1_inner[ri]
                        right = 10 * c6_inner[ri] + c7_inner[ri]
                        mid   = to_digits(left * right, 4)
                        inner_rows.append(mid)

                    # Verify inner cols 2–5
                    for ci in range(4):
                        col_top = 10 * r0m[ci] + r1m[ci]
                        col_bot = 10 * r6m[ci] + r7m[ci]
                        col_mid = to_digits(col_top * col_bot, 4)
                        for ri in range(4):
                            if inner_rows[ri][ci] != col_mid[ri]:
                                ok = False
                                break
                        if not ok:
                            break

                    if ok:
                        M = build_matrix(tl, tr, bl, br, k)
                        if M is not None:
                            results.append(M)

    return results


# ---------------------------------------------------------------------------
# Generalized exhaustive for small k using build_matrix
# ---------------------------------------------------------------------------

def exhaustive_general(k: int, max_squares: int = None,
                       verbose: bool = True) -> list:
    """
    General exhaustive search for any k, using build_matrix.
    Only practical for k=1 (instant) or k=2 (minutes).
    For k≥3, use random_search instead.
    """
    results = []
    flat_blocks = list(iproduct(range(1, 10), repeat=k*k))
    total = len(flat_blocks) ** 4

    if verbose:
        print(f"  Search space: {len(flat_blocks)^4:,} corner combinations")
        print(f"  ({len(flat_blocks):,}^4 = {total:,})")

    count = 0
    for tl_f in flat_blocks:
        tl = [list(tl_f[r*k:(r+1)*k]) for r in range(k)]
        for tr_f in flat_blocks:
            tr = [list(tr_f[r*k:(r+1)*k]) for r in range(k)]
            for bl_f in flat_blocks:
                bl = [list(bl_f[r*k:(r+1)*k]) for r in range(k)]
                for br_f in flat_blocks:
                    br = [list(br_f[r*k:(r+1)*k]) for r in range(k)]
                    M = build_matrix(tl, tr, bl, br, k)
                    if M is not None:
                        results.append(M)
                        if verbose:
                            print(f"  Found #{len(results)}")
                        if max_squares and len(results) >= max_squares:
                            return results
                    count += 1

    if verbose:
        print(f"  Checked {count:,} combinations")
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find Barron Squares of order k")
    parser.add_argument("--k", type=int, default=1,
                        help="Order k (matrix size = 4k). Default: 1")
    parser.add_argument("--method", choices=["exhaustive", "random"],
                        default="exhaustive",
                        help="Search method. Default: exhaustive")
    parser.add_argument("--trials", type=int, default=1_000_000,
                        help="Number of random trials (for --method random)")
    parser.add_argument("--max", type=int, default=None,
                        help="Stop after finding this many squares")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress")
    args = parser.parse_args()

    k = args.k
    n = 4 * k
    verbose = not args.quiet

    print(f"Barron Square finder: k={k}, matrix size {n}×{n}")
    print(f"Method: {args.method}")
    print()

    import time
    t0 = time.time()

    if args.method == "exhaustive":
        if k == 1:
            squares = exhaustive_k1()
        elif k == 2:
            squares = constraint_search_k2()
        else:
            print(f"Warning: exhaustive search for k={k} is very slow.")
            squares = exhaustive_general(k, max_squares=args.max, verbose=verbose)
    else:
        squares = random_search(k, trials=args.trials, verbose=verbose)

    elapsed = time.time() - t0
    print(f"\nFound {len(squares)} Barron Squares of order {k} ({n}×{n})")
    print(f"Time: {elapsed:.2f}s")

    if squares:
        print("\nFirst square found:")
        print(display(squares[0], k=k))
        from barron_core import is_valid_barron
        print(f"\nValidation: {is_valid_barron(squares[0], k)}")
