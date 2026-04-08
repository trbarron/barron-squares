"""
find_8x8.py — Enumerate all 8×8 Barron Squares (k=2).

For k=2 the four corner 2×2 blocks contain 16 nonzero digits, giving
9^16 ≈ 1.85×10^15 raw combinations — far too many to brute-force.

Strategy: decompose the search using precomputed tables and early pruning.

Key observation
───────────────
Given corners TL, TR, BL, BR (each a 2×2 block of digits 1–9):

  Phase A  (top half)
    • Row 0: (10·M[0][0]+M[0][1]) × (10·M[0][6]+M[0][7]) → M[0][2..5]
    • Row 1: (10·M[1][0]+M[1][1]) × (10·M[1][6]+M[1][7]) → M[1][2..5]

  Phase B  (bottom half)
    • Row 6, Row 7 middles → similarly from BL, BR

  Phase C  (left/right edge columns, inner rows)
    • Col 0: (10·M[0][0]+M[1][0]) × (10·M[6][0]+M[7][0]) → M[2..5][0]
    • Col 1, Col 6, Col 7: similarly

  Phase D  (inner rows 2–5)
    • Left ends of rows 2–5 come from cols 0–1 (Phase C)
    • Right ends come from cols 6–7 (Phase C)
    • → middles M[2..5][2..5] from row constraint

  Phase E  (consistency check)
    • Inner cols 2–5: tops from Phase A, bottoms from Phase B
    • → must match Phase D middles exactly

Pruning: we can check that edge no-zero constraints are satisfied after
each phase, eliminating bad branches early.

Usage:
    python src/find_8x8.py
"""

from barron_core import build_matrix, display, is_valid_barron, to_digits, from_digits
from itertools import product as iproduct
from collections import defaultdict


def _row_middle(left_digits: list[int], right_digits: list[int]) -> list[int] | None:
    """
    Given k left digits and k right digits forming two k-digit numbers,
    return the 2k digits of their product, or None if any digit is zero
    in an edge-row context (edge constraint applied by caller).
    """
    L = from_digits(left_digits)
    R = from_digits(right_digits)
    return to_digits(L * R, 2 * len(left_digits))


def _block_to_2digit(block_col: list[int]) -> int:
    """Convert two-cell column slice [top, bot] to 2-digit int."""
    return 10 * block_col[0] + block_col[1]


def find_all_8x8(verbose: bool = True) -> list[list[list[int]]]:
    """
    Find all 8×8 Barron Squares using layered pruning.

    Outline of pruned search
    ─────────────────────────
    For each TL (9^4 = 6,561):
      compute partial edge-row middles for row 0 and row 1 (cols 2–5)
      For each TR (9^4):
        complete row 0 and row 1 middles
        check no-zero edge constraint on rows 0–1
        For each BL (9^4):
          compute partial edge-row middles for row 6 and row 7
          compute inner-row left-ends from col-0, col-1 products
          check no-zero edge constraint on col 0, col 1 inner cells
          For each BR (9^4):
            complete row 6, row 7 middles
            complete inner-row right-ends from col 6, col 7 products
            check no-zero edge on col 6, col 7 inner cells
            compute inner-row middles (rows 2–5, cols 2–5) via row constraint
            verify inner col constraint (cols 2–5) gives same center
            collect valid squares
    """
    k = 2
    n = 8
    results = []

    checked = 0

    # Precompute: for each pair of 2-digit numbers (A, B) where A and B
    # are formed from nonzero digits, what 4-digit product do they give?
    # We'll just compute inline; the pruning reduces the real work.

    for tl_flat in iproduct(range(1, 10), repeat=4):
        tl = [list(tl_flat[:2]), list(tl_flat[2:])]  # 2×2 block

        for tr_flat in iproduct(range(1, 10), repeat=4):
            tr = [list(tr_flat[:2]), list(tr_flat[2:])]

            # --- Compute rows 0 and 1 middles (cols 2–5) ---
            row0_mid = _row_middle(
                [tl[0][0], tl[0][1]], [tr[0][0], tr[0][1]]
            )
            row1_mid = _row_middle(
                [tl[1][0], tl[1][1]], [tr[1][0], tr[1][1]]
            )

            # No-zero check on edge rows 0 and 1 (cols 2–5 are edge cols?
            # No — cols 2–5 are INNER cols, but rows 0–1 are edge rows,
            # so all cells in rows 0–1 must be nonzero.)
            if any(d == 0 for d in row0_mid + row1_mid):
                continue

            for bl_flat in iproduct(range(1, 10), repeat=4):
                bl = [list(bl_flat[:2]), list(bl_flat[2:])]

                row6_mid_partial = _row_middle(
                    [bl[0][0], bl[0][1]], [0, 0]  # right end unknown yet
                )
                # Compute col 0 inner rows (rows 2–5, col 0)
                col0_top = 10 * tl[0][0] + tl[1][0]
                col0_bot = 10 * bl[0][0] + bl[1][0]
                col0_inner = to_digits(col0_top * col0_bot, 4)

                col1_top = 10 * tl[0][1] + tl[1][1]
                col1_bot = 10 * bl[0][1] + bl[1][1]
                col1_inner = to_digits(col1_top * col1_bot, 4)

                # No-zero check: col 0 and col 1 inner rows are edge cols
                if any(d == 0 for d in col0_inner + col1_inner):
                    continue

                for br_flat in iproduct(range(1, 10), repeat=4):
                    br = [list(br_flat[:2]), list(br_flat[2:])]
                    checked += 1

                    # --- Complete rows 6 and 7 middles ---
                    row6_mid = _row_middle(
                        [bl[0][0], bl[0][1]], [br[0][0], br[0][1]]
                    )
                    row7_mid = _row_middle(
                        [bl[1][0], bl[1][1]], [br[1][0], br[1][1]]
                    )
                    if any(d == 0 for d in row6_mid + row7_mid):
                        continue

                    # --- Col 6 and col 7 inner rows ---
                    col6_top = 10 * tr[0][0] + tr[1][0]
                    col6_bot = 10 * br[0][0] + br[1][0]
                    col6_inner = to_digits(col6_top * col6_bot, 4)

                    col7_top = 10 * tr[0][1] + tr[1][1]
                    col7_bot = 10 * br[0][1] + br[1][1]
                    col7_inner = to_digits(col7_top * col7_bot, 4)

                    if any(d == 0 for d in col6_inner + col7_inner):
                        continue

                    # --- Build inner rows 2–5: left/right ends now known ---
                    # Row r (for r in 2..5, index ri = r-2):
                    #   left  = [col0_inner[ri], col1_inner[ri]]
                    #   right = [col6_inner[ri], col7_inner[ri]]
                    inner_center_from_rows = []
                    valid = True
                    for ri in range(4):
                        left  = [col0_inner[ri], col1_inner[ri]]
                        right = [col6_inner[ri], col7_inner[ri]]
                        mid   = _row_middle(left, right)
                        inner_center_from_rows.append(mid)

                    if not valid:
                        continue

                    # --- Verify inner cols 2–5 ---
                    # Col c (for c in 2..5, index ci = c-2):
                    #   top = [row0_mid[ci], row1_mid[ci]]
                    #   bot = [row6_mid[ci], row7_mid[ci]]
                    consistent = True
                    for ci in range(4):
                        top = [row0_mid[ci], row1_mid[ci]]
                        bot = [row6_mid[ci], row7_mid[ci]]
                        mid_from_col = _row_middle(top, bot)
                        # mid_from_col should equal column ci of inner_center_from_rows
                        for ri in range(4):
                            if inner_center_from_rows[ri][ci] != mid_from_col[ri]:
                                consistent = False
                                break
                        if not consistent:
                            break

                    if not consistent:
                        continue

                    # --- Assemble full matrix ---
                    M = build_matrix(tl, tr, bl, br, k)
                    if M is not None:
                        results.append(M)
                        if verbose:
                            print(f"  Found square #{len(results)} "
                                  f"(checked {checked:,} BR blocks)")

    if verbose:
        print(f"\nTotal checked: {checked:,}")
    return results


def find_all_8x8_fast(verbose: bool = True) -> list[list[list[int]]]:
    """
    Faster version using precomputed lookup tables.

    Key idea: precompute for every pair (A, B) of 2-digit numbers
    (formed from nonzero digits) the resulting 4-digit product string.
    Then the consistency check reduces to table lookups.
    """
    k = 2
    results = []

    # All 2-digit nonzero-digit numbers: 11–99 with no zero digit
    valid_2digit = [n for n in range(11, 100)
                    if (n // 10) != 0 and (n % 10) != 0]

    # Precompute product table: (A, B) -> 4-digit list
    prod_table: dict[tuple[int, int], list[int]] = {}
    for A in range(11, 100):
        for B in range(11, 100):
            prod_table[(A, B)] = to_digits(A * B, 4)

    # We represent each 2×2 corner block as four values a,b,c,d:
    #   [[a,b],[c,d]]
    # The "left" 2-digit of row 0 is 10a+b, of row 1 is 10c+d.
    # The "top" 2-digit of col 0 is 10a+c, of col 1 is 10b+d.

    # For pruning: precompute which (TL, TR) pairs produce valid row 0 and row 1.
    # A pair is valid if neither row0_mid nor row1_mid contains a zero.

    def corner_rows(tl_flat, tr_flat):
        """(row0_mid, row1_mid) or None if any zero in edge rows."""
        a0, b0, c0, d0 = tl_flat  # TL: [[a0,b0],[c0,d0]]
        a1, b1, c1, d1 = tr_flat  # TR: [[a1,b1],[c1,d1]]
        r0m = prod_table[(10*a0+b0, 10*a1+b1)]
        r1m = prod_table[(10*c0+d0, 10*c1+d1)]
        if 0 in r0m or 0 in r1m:
            return None
        return r0m, r1m

    def corner_cols_left(tl_flat, bl_flat):
        """(col0_inner, col1_inner) or None if any zero."""
        a0, b0, c0, d0 = tl_flat
        a2, b2, c2, d2 = bl_flat
        c0i = prod_table[(10*a0+c0, 10*a2+c2)]
        c1i = prod_table[(10*b0+d0, 10*b2+d2)]
        if 0 in c0i or 0 in c1i:
            return None
        return c0i, c1i

    def corner_cols_right(tr_flat, br_flat):
        a1, b1, c1, d1 = tr_flat
        a3, b3, c3, d3 = br_flat
        c6i = prod_table[(10*a1+c1, 10*a3+c3)]
        c7i = prod_table[(10*b1+d1, 10*b3+d3)]
        if 0 in c6i or 0 in c7i:
            return None
        return c6i, c7i

    def corner_rows_bottom(bl_flat, br_flat):
        a2, b2, c2, d2 = bl_flat
        a3, b3, c3, d3 = br_flat
        r6m = prod_table[(10*a2+b2, 10*a3+b3)]
        r7m = prod_table[(10*c2+d2, 10*c3+d3)]
        if 0 in r6m or 0 in r7m:
            return None
        return r6m, r7m

    flat_iter = list(iproduct(range(1, 10), repeat=4))

    # Precompute valid (TL, TR) pairs
    tl_tr_cache: dict = {}  # tl_flat -> [(tr_flat, row0_mid, row1_mid), ...]
    for tl_flat in flat_iter:
        valid_trs = []
        for tr_flat in flat_iter:
            res = corner_rows(tl_flat, tr_flat)
            if res is not None:
                valid_trs.append((tr_flat, res[0], res[1]))
        if valid_trs:
            tl_tr_cache[tl_flat] = valid_trs

    # Precompute valid (TL, BL) pairs
    tl_bl_cache: dict = {}
    for tl_flat in flat_iter:
        valid_bls = []
        for bl_flat in flat_iter:
            res = corner_cols_left(tl_flat, bl_flat)
            if res is not None:
                valid_bls.append((bl_flat, res[0], res[1]))
        if valid_bls:
            tl_bl_cache[tl_flat] = valid_bls

    total_checked = 0

    for tl_flat, tl_trs in tl_tr_cache.items():
        for tr_flat, row0_mid, row1_mid in tl_trs:
            bl_list = tl_bl_cache.get(tl_flat, [])
            for bl_flat, col0_inner, col1_inner in bl_list:
                # Need (TR, BR) for right cols and bottom rows
                for br_flat in flat_iter:
                    total_checked += 1

                    # Right cols
                    right_res = corner_cols_right(tr_flat, br_flat)
                    if right_res is None:
                        continue
                    col6_inner, col7_inner = right_res

                    # Bottom rows
                    bot_res = corner_rows_bottom(bl_flat, br_flat)
                    if bot_res is None:
                        continue
                    row6_mid, row7_mid = bot_res

                    # Compute inner center from rows
                    inner_rows = []
                    ok = True
                    for ri in range(4):
                        left  = (10 * col0_inner[ri] + col1_inner[ri])
                        right = (10 * col6_inner[ri] + col7_inner[ri])
                        mid   = prod_table.get((left, right))
                        if mid is None:
                            mid = to_digits(left * right, 4)
                        inner_rows.append(mid)

                    # Verify inner cols
                    for ci in range(4):
                        top_num = 10 * row0_mid[ci] + row1_mid[ci]
                        bot_num = 10 * row6_mid[ci] + row7_mid[ci]
                        col_mid = prod_table.get((top_num, bot_num))
                        if col_mid is None:
                            col_mid = to_digits(top_num * bot_num, 4)
                        for ri in range(4):
                            if inner_rows[ri][ci] != col_mid[ri]:
                                ok = False
                                break
                        if not ok:
                            break

                    if ok:
                        tl = [list(tl_flat[:2]), list(tl_flat[2:])]
                        tr = [list(tr_flat[:2]), list(tr_flat[2:])]
                        bl = [list(bl_flat[:2]), list(bl_flat[2:])]
                        br = [list(br_flat[:2]), list(br_flat[2:])]
                        M = build_matrix(tl, tr, bl, br, k)
                        if M is not None:
                            results.append(M)
                            if verbose:
                                print(f"  Found #{len(results):3d}  "
                                      f"corners: TL={tl_flat} TR={tr_flat} "
                                      f"BL={bl_flat} BR={br_flat}")

    if verbose:
        print(f"\nTotal BR combinations checked: {total_checked:,}")
    return results


if __name__ == "__main__":
    print("Finding all 8×8 Barron Squares (fast version)...")
    print("This may take several minutes.\n")

    import time
    t0 = time.time()
    squares = find_all_8x8_fast(verbose=True)
    elapsed = time.time() - t0

    print(f"\n{'='*60}")
    print(f"Total found: {len(squares)}")
    print(f"Time: {elapsed:.1f}s")
    print("=" * 60)

    if squares:
        print("\nFirst 3 squares:")
        for M in squares[:3]:
            print(display(M, k=2))
            assert is_valid_barron(M, k=2), "VALIDATION FAILED!"
            print()
