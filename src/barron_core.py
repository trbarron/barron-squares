"""
barron_core.py — Core definitions and algorithms for Barron Squares.

A Barron Square of order k is a (4k × 4k) matrix of decimal digits (0–9) where:
  - Every row i:  the k-digit number formed by cells [i][0..k-1]
                  times the k-digit number formed by cells [i][3k..4k-1]
                  equals the 2k-digit number formed by cells [i][k..3k-1].
  - Every col j:  the k-digit number formed by cells [0..k-1][j]
                  times the k-digit number formed by cells [3k..4k-1][j]
                  equals the 2k-digit number formed by cells [k..3k-1][j].
  - No edge cell (any cell in the outermost k rows or k columns) may be 0.

The free parameters are the four corner k×k blocks (TL, TR, BL, BR).
All other cells are uniquely determined; validity requires consistency.
"""

from itertools import product as iproduct
from typing import Optional


# ---------------------------------------------------------------------------
# Digit utilities
# ---------------------------------------------------------------------------

def to_digits(n: int, width: int) -> list[int]:
    """Return the decimal digits of n left-padded to `width` places."""
    return [int(c) for c in str(n).zfill(width)]


def from_digits(digits: list[int]) -> int:
    """Convert a list of decimal digits (most-significant first) to an int."""
    result = 0
    for d in digits:
        result = result * 10 + d
    return result


# ---------------------------------------------------------------------------
# Barron Square construction
# ---------------------------------------------------------------------------

def build_matrix(tl: list[list[int]], tr: list[list[int]],
                 bl: list[list[int]], br: list[list[int]],
                 k: int) -> Optional[list[list[int]]]:
    """
    Construct a (4k × 4k) matrix from four corner k×k blocks and
    return it if the Barron constraints are consistent, else None.

    Corner layout (n = 4k):
        TL  |   middle top    |  TR
        ----+-----------------+----
        mid |  inner (2k×2k)  | mid
        ----+-----------------+----
        BL  |  middle bottom  |  BR

    Steps:
      1. Place corner blocks.
      2. Fill edge rows (rows 0..k-1, rows 3k..4k-1) middle cells via row constraint.
      3. Fill edge cols (cols 0..k-1, cols 3k..4k-1) inner-row cells via col constraint.
      4. Fill inner rows (rows k..3k-1) middle cells via row constraint.
      5. Verify inner cols (cols k..3k-1) give the same inner center values.
      6. Check no-zero edge constraint.
    """
    n = 4 * k
    M = [[0] * n for _ in range(n)]

    # --- Step 1: Place corner blocks ---
    for r in range(k):
        for c in range(k):
            M[r][c]             = tl[r][c]        # top-left
            M[r][n - k + c]     = tr[r][c]        # top-right
            M[n - k + r][c]     = bl[r][c]        # bottom-left
            M[n - k + r][n - k + c] = br[r][c]   # bottom-right

    # --- Step 2: Fill edge rows (rows 0..k-1 and 3k..4k-1) ---
    for row in list(range(k)) + list(range(3 * k, 4 * k)):
        left  = from_digits([M[row][c] for c in range(k)])
        right = from_digits([M[row][n - k + c] for c in range(k)])
        prod  = left * right
        digits = to_digits(prod, 2 * k)
        if len(digits) > 2 * k:
            return None  # product overflow
        for i, d in enumerate(digits):
            M[row][k + i] = d

    # --- Step 3: Fill edge cols (cols 0..k-1 and 3k..4k-1), inner rows ---
    for col in list(range(k)) + list(range(3 * k, 4 * k)):
        top = from_digits([M[r][col] for r in range(k)])
        bot = from_digits([M[n - k + r][col] for r in range(k)])
        prod   = top * bot
        digits = to_digits(prod, 2 * k)
        if len(digits) > 2 * k:
            return None
        for i, d in enumerate(digits):
            M[k + i][col] = d

    # --- Step 4: Fill inner rows (rows k..3k-1), middle cells ---
    inner_center_from_rows = [[0] * (2 * k) for _ in range(2 * k)]
    for ri, row in enumerate(range(k, 3 * k)):
        left  = from_digits([M[row][c] for c in range(k)])
        right = from_digits([M[row][n - k + c] for c in range(k)])
        prod  = left * right
        digits = to_digits(prod, 2 * k)
        if len(digits) > 2 * k:
            return None
        for i, d in enumerate(digits):
            M[row][k + i] = d
            inner_center_from_rows[ri][i] = d

    # --- Step 5: Verify inner cols give the same center ---
    for ci, col in enumerate(range(k, 3 * k)):
        top = from_digits([M[r][col] for r in range(k)])
        bot = from_digits([M[n - k + r][col] for r in range(k)])
        prod   = top * bot
        digits = to_digits(prod, 2 * k)
        if len(digits) > 2 * k:
            return None
        for i, d in enumerate(digits):
            if inner_center_from_rows[i][ci] != d:
                return None  # Inconsistent

    # --- Step 6: No zeros on edges ---
    for row in range(n):
        for col in range(n):
            is_edge = (row < k or row >= 3 * k or col < k or col >= 3 * k)
            if is_edge and M[row][col] == 0:
                return None

    return M


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def is_valid_barron(M: list[list[int]], k: int) -> bool:
    """Return True if M is a valid Barron Square of order k."""
    n = 4 * k
    if len(M) != n or any(len(row) != n for row in M):
        return False

    # Check row constraint for all rows
    for row in range(n):
        left   = from_digits([M[row][c] for c in range(k)])
        right  = from_digits([M[row][n - k + c] for c in range(k)])
        middle = from_digits([M[row][k + i] for i in range(2 * k)])
        if left * right != middle:
            return False

    # Check col constraint for all cols
    for col in range(n):
        top    = from_digits([M[r][col] for r in range(k)])
        bot    = from_digits([M[n - k + r][col] for r in range(k)])
        middle = from_digits([M[k + i][col] for i in range(2 * k)])
        if top * bot != middle:
            return False

    # Check no zeros on edges
    for row in range(n):
        for col in range(n):
            is_edge = (row < k or row >= 3 * k or col < k or col >= 3 * k)
            if is_edge and M[row][col] == 0:
                return False

    return True


# ---------------------------------------------------------------------------
# Corner enumeration
# ---------------------------------------------------------------------------

def _corner_block_iter(k: int, nonzero: bool = True):
    """Iterate over all k×k blocks of digits (0–9; 1–9 if nonzero)."""
    digits = range(1, 10) if nonzero else range(10)
    for flat in iproduct(digits, repeat=k * k):
        yield [list(flat[r * k:(r + 1) * k]) for r in range(k)]


def find_all_barron_squares(k: int, verbose: bool = False) -> list[list[list[int]]]:
    """
    Find all Barron Squares of order k by enumerating corner block combinations.

    For k=1 (4×4):  9^4 = 6,561 combinations — instant.
    For k=2 (8×8):  9^16 ≈ 1.85e15 combinations — requires pruning.

    For k≥2 the search is done with early pruning (see find_8x8_fast.py
    or the C implementation barron8x8.c for dedicated BOT-derivation
    implementations).

    Returns a list of valid (4k × 4k) matrices.
    """
    results = []
    count = 0
    for tl in _corner_block_iter(k):
        for tr in _corner_block_iter(k):
            for bl in _corner_block_iter(k):
                for br in _corner_block_iter(k):
                    M = build_matrix(tl, tr, bl, br, k)
                    if M is not None:
                        results.append(M)
                    count += 1
                    if verbose and count % 100_000 == 0:
                        print(f"  checked {count:,}, found {len(results):,} so far")
    return results


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

def display(M: list[list[int]], k: int = 1) -> str:
    """Pretty-print a Barron Square, highlighting corner and edge regions."""
    n = len(M)
    lines = []
    for r, row in enumerate(M):
        sep_row = (r == k or r == 3 * (n // 4))
        if sep_row:
            lines.append("  " + "─" * (n * 2 - 1))
        cells = []
        for c, val in enumerate(row):
            sep_col = (c == k or c == 3 * (n // 4))
            if sep_col:
                cells.append("│")
            cells.append(str(val))
        lines.append("  " + " ".join(cells))
    return "\n".join(lines)
