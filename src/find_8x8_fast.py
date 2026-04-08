"""
find_8x8_fast.py — Efficient 8×8 Barron Square finder.

Mathematical insight
────────────────────
An 8×8 Barron Square has four 2×2 corner blocks TL, TR, BL, BR.
Given TL, TR, and just two derived 2-digit values (col6_B, col7_B), the
ENTIRE remainder of the matrix is forced:

  col6_B = 10*m + o,  col7_B = 10*n + p   (from BR = [[m,n],[o,p]])

  → BR uniquely determined: m,n,o,p from col6_B, col7_B
  → row6_R = 10m+n,  row7_R = 10o+p   (right ends of rows 6,7)
  → col6_inner, col7_inner   (rows 2–5 of cols 6,7)
  → RIGHT[ri] = 10*col6_inner[ri] + col7_inner[ri]
  → TOP[ci] = 10*row0_mid[ci] + row1_mid[ci]   (from TL × TR)

  Now the inner-center IC[ri][ci] = digit(ci) of LEFT[ri] × RIGHT[ri].
  For IC to satisfy the column constraint:
      N_col[ci] = from_digits(IC[*][ci]) = TOP[ci] × BOT[ci]
  so BOT[ci] = N_col[ci] / TOP[ci]  (must be an exact integer, 2-digit, no-zero).

  From BOT[ci] we recover row6_mid[ci]=BOT[ci]//10, row7_mid[ci]=BOT[ci]%10.
  Then row6_L = from_digits(row6_mid) / row6_R, row7_L = from_digits(row7_mid) / row7_R.
  BL is fully determined by row6_L and row7_L.
  Finally: verify the BL we derived is consistent with col0_T, col1_T constraints.

So the search is:
  TL (6561) × valid TR (avg ~2290) × valid (col6_B, col7_B) (avg ~2304)
= ~37 billion combinations, but almost all fail the first BOT divisibility check.
In practice, because the BOT check fails with probability ≈ 1 - 1/avg_TOP ≈ 98%
on the first column, the effective work is much less.

We additionally depend on LEFT — but LEFT depends on BL (which we're deriving),
so we iterate over (col0_B, col1_B) ∈ V(col0_T) × V(col1_T) as the last step.

Final loop structure
─────────────────────
  For each TL (6561):
    For each valid TR (~2290):
      compute TOP, col0_T, col1_T, col6_T, col7_T
      For each (col6_B, col7_B) in V(col6_T)×V(col7_T)  (~2304):
        derive row6_R, row7_R → check valid 2-digit no-zero
        compute col6_inner, col7_inner → RIGHT
        For each (col0_B, col1_B) in V(col0_T)×V(col1_T)  (~2304):
          compute col0_inner, col1_inner → LEFT
          compute IC from LEFT×RIGHT
          for ci=0..3: check TOP[ci] | N_col[ci], derive BOT
          derive row6_L, row7_L from BOT
          check BL consistency: col0_B_derived==col0_B, col1_B_derived==col1_B
          if all pass: record square

Usage:
    python src/find_8x8_fast.py
"""

import sys, os, time
sys.path.insert(0, os.path.dirname(__file__))

from barron_core import build_matrix, is_valid_barron, display, to_digits, from_digits
from itertools import product as iproduct

# ---------------------------------------------------------------------------
# Precomputed tables
# ---------------------------------------------------------------------------

# PROD4[A][B] = 4-digit list of A*B (A, B ∈ 0..99).
# Entries are None for invalid (non-2-digit-no-zero) inputs.
PROD4 = [[None] * 100 for _ in range(100)]
for _A in range(11, 100):
    if _A // 10 == 0 or _A % 10 == 0:
        continue
    for _B in range(11, 100):
        if _B // 10 == 0 or _B % 10 == 0:
            continue
        _p = _A * _B
        PROD4[_A][_B] = (_p // 1000, (_p // 100) % 10, (_p // 10) % 10, _p % 10)

# VALID_R[A] = sorted list of B ∈ {11..99} (no-zero) where A*B is 4-digit no-zero.
VALID_R = [[] for _ in range(100)]
VALID_R_SET = [set() for _ in range(100)]
for _A in range(11, 100):
    if _A // 10 == 0 or _A % 10 == 0:
        continue
    for _B in range(11, 100):
        if _B // 10 == 0 or _B % 10 == 0:
            continue
        _p = PROD4[_A][_B]
        if _p is not None and 0 not in _p:
            VALID_R[_A].append(_B)
            VALID_R_SET[_A].add(_B)


# ---------------------------------------------------------------------------
# Inner check: given (TOP, RIGHT, row6_R, row7_R, col0_T, col1_T) and a
# specific (col0_B, col1_B), compute LEFT, IC, BOT, row6_L, row7_L and
# check consistency.
# Returns (row6_L, row7_L) if consistent, else None.
# ---------------------------------------------------------------------------

def _check_inner(top, right, row6R, row7R, col0T, col1T, col0B, col1B):
    # Compute col0_inner, col1_inner
    c0i = PROD4[col0T][col0B]
    if c0i is None or 0 in c0i:
        return None
    c1i = PROD4[col1T][col1B]
    if c1i is None or 0 in c1i:
        return None

    # LEFT[ri]
    L0 = 10 * c0i[0] + c1i[0]
    L1 = 10 * c0i[1] + c1i[1]
    L2 = 10 * c0i[2] + c1i[2]
    L3 = 10 * c0i[3] + c1i[3]

    # Check LEFT values have no-zero digits (they're 2-digit numbers from edge cols)
    if (L0 // 10 == 0 or L0 % 10 == 0 or
        L1 // 10 == 0 or L1 % 10 == 0 or
        L2 // 10 == 0 or L2 % 10 == 0 or
        L3 // 10 == 0 or L3 % 10 == 0):
        return None

    # IC from rows: IC[ri][ci] = digit(ci) of (L[ri] × right[ri])
    p0 = L0 * right[0]
    p1 = L1 * right[1]
    p2 = L2 * right[2]
    p3 = L3 * right[3]

    # N_col[ci] = from_digits(IC[*][ci]) for ci=0..3
    # N_col[0] = thousands digits: p0//1000, p1//1000, p2//1000, p3//1000
    # N_col[1] = hundreds digits, etc.
    N0 = (p0 // 1000) * 1000 + (p1 // 1000) * 100 + (p2 // 1000) * 10 + (p3 // 1000)
    T0 = top[0]
    if N0 % T0 != 0:
        return None
    B0 = N0 // T0
    if B0 < 11 or B0 > 99 or B0 // 10 == 0 or B0 % 10 == 0:
        return None

    N1 = ((p0 // 100) % 10) * 1000 + ((p1 // 100) % 10) * 100 + ((p2 // 100) % 10) * 10 + ((p3 // 100) % 10)
    T1 = top[1]
    if N1 % T1 != 0:
        return None
    B1 = N1 // T1
    if B1 < 11 or B1 > 99 or B1 // 10 == 0 or B1 % 10 == 0:
        return None

    N2 = ((p0 // 10) % 10) * 1000 + ((p1 // 10) % 10) * 100 + ((p2 // 10) % 10) * 10 + ((p3 // 10) % 10)
    T2 = top[2]
    if N2 % T2 != 0:
        return None
    B2 = N2 // T2
    if B2 < 11 or B2 > 99 or B2 // 10 == 0 or B2 % 10 == 0:
        return None

    N3 = (p0 % 10) * 1000 + (p1 % 10) * 100 + (p2 % 10) * 10 + (p3 % 10)
    T3 = top[3]
    if N3 % T3 != 0:
        return None
    B3 = N3 // T3
    if B3 < 11 or B3 > 99 or B3 // 10 == 0 or B3 % 10 == 0:
        return None

    # row6_mid = [B0//10, B1//10, B2//10, B3//10]
    # row7_mid = [B0%10, B1%10, B2%10, B3%10]
    r6m0 = B0 // 10; r6m1 = B1 // 10; r6m2 = B2 // 10; r6m3 = B3 // 10
    r7m0 = B0 % 10;  r7m1 = B1 % 10;  r7m2 = B2 % 10;  r7m3 = B3 % 10

    # All edge row middles must be nonzero
    if (r6m0 == 0 or r6m1 == 0 or r6m2 == 0 or r6m3 == 0 or
        r7m0 == 0 or r7m1 == 0 or r7m2 == 0 or r7m3 == 0):
        return None

    N_row6 = r6m0 * 1000 + r6m1 * 100 + r6m2 * 10 + r6m3
    N_row7 = r7m0 * 1000 + r7m1 * 100 + r7m2 * 10 + r7m3

    if N_row6 % row6R != 0:
        return None
    row6L = N_row6 // row6R
    if row6L < 11 or row6L > 99 or row6L // 10 == 0 or row6L % 10 == 0:
        return None

    if N_row7 % row7R != 0:
        return None
    row7L = N_row7 // row7R
    if row7L < 11 or row7L > 99 or row7L // 10 == 0 or row7L % 10 == 0:
        return None

    # Consistency: the BL derived from row6L, row7L must give col0_B and col1_B
    # BL[0] = [row6L//10, row6L%10], BL[1] = [row7L//10, row7L%10]
    # col0_B_check = 10*(row6L//10) + (row7L//10)
    # col1_B_check = 10*(row6L%10) + (row7L%10)
    if (10 * (row6L // 10) + (row7L // 10) != col0B or
        10 * (row6L % 10) + (row7L % 10) != col1B):
        return None

    return (row6L, row7L)


# ---------------------------------------------------------------------------
# Main search
# ---------------------------------------------------------------------------

def find_all_8x8(verbose: bool = True) -> list:
    """Find all 8×8 Barron Squares using the BOT-derivation method."""
    results = []
    outer_count = 0
    check_count = 0
    t0 = time.time()

    all_blocks = list(iproduct(range(1, 10), repeat=4))

    for tl_flat in all_blocks:
        a, b, c, d = tl_flat
        row0L = 10 * a + b
        row1L = 10 * c + d
        col0T = 10 * a + c
        col1T = 10 * b + d

        vTR0 = VALID_R[row0L]
        vTR1 = VALID_R_SET[row1L]
        vBL0 = VALID_R[col0T]
        vBL1 = VALID_R_SET[col1T]

        if not vTR0 or not vTR1 or not vBL0 or not vBL1:
            continue

        for tr_flat in all_blocks:
            e, f, g, h = tr_flat
            row0R = 10 * e + f
            row1R = 10 * g + h

            if row0R not in VALID_R_SET[row0L] or row1R not in vTR1:
                continue

            # Rows 0 and 1 middles
            r0m = PROD4[row0L][row0R]
            r1m = PROD4[row1L][row1R]
            if r0m is None or r1m is None:
                continue
            # All cells in edge rows 0,1 must be nonzero (already guaranteed by VALID_R)

            # TOP[ci] = 10*r0m[ci] + r1m[ci]
            TOP = (
                10 * r0m[0] + r1m[0],
                10 * r0m[1] + r1m[1],
                10 * r0m[2] + r1m[2],
                10 * r0m[3] + r1m[3],
            )
            # TOP values must be 2-digit no-zero (they're in edge rows)
            if any(t < 11 or t > 99 or t // 10 == 0 or t % 10 == 0 for t in TOP):
                continue

            col6T = 10 * e + g
            col7T = 10 * f + h

            vC6 = VALID_R[col6T]
            vC7 = VALID_R_SET[col7T]
            if not vC6 or not vC7:
                continue

            for col6B in vC6:
                if col6B not in VALID_R_SET[col6T]:
                    continue  # redundant but kept for clarity

                # Derive row6_R, row7_R from (col6_B, col7_B)
                m = col6B // 10
                o_val = col6B % 10

                for col7B in vC7:
                    outer_count += 1
                    n = col7B // 10
                    p_val = col7B % 10

                    row6R = 10 * m + n
                    row7R = 10 * o_val + p_val

                    # row6_R and row7_R must be valid 2-digit no-zero
                    if (row6R < 11 or row6R > 99 or row6R // 10 == 0 or row6R % 10 == 0 or
                        row7R < 11 or row7R > 99 or row7R // 10 == 0 or row7R % 10 == 0):
                        continue

                    # Compute col6_inner and col7_inner
                    c6i = PROD4[col6T][col6B]
                    c7i = PROD4[col7T][col7B]
                    if c6i is None or 0 in c6i or c7i is None or 0 in c7i:
                        continue

                    # RIGHT[ri]
                    RIGHT = (
                        10 * c6i[0] + c7i[0],
                        10 * c6i[1] + c7i[1],
                        10 * c6i[2] + c7i[2],
                        10 * c6i[3] + c7i[3],
                    )
                    # RIGHT values (edge col inner rows, must be nonzero)
                    if any(r < 11 or r > 99 or r // 10 == 0 or r % 10 == 0 for r in RIGHT):
                        continue

                    # Inner loop: (col0_B, col1_B)
                    for col0B in vBL0:
                        for col1B_val in VALID_R[col1T]:
                            if col1B_val not in vBL1:
                                continue
                            check_count += 1
                            res = _check_inner(
                                TOP, RIGHT, row6R, row7R,
                                col0T, col1T, col0B, col1B_val
                            )
                            if res is None:
                                continue

                            row6L, row7L = res

                            # Reconstruct corner blocks
                            tl = [[a, b], [c, d]]
                            tr = [[e, f], [g, h]]
                            bl = [[row6L // 10, row6L % 10],
                                  [row7L // 10, row7L % 10]]
                            br = [[m, n], [o_val, p_val]]

                            M = build_matrix(tl, tr, bl, br, k=2)
                            if M is not None:
                                results.append(M)
                                if verbose:
                                    elapsed = time.time() - t0
                                    print(f"  Found #{len(results):3d}  "
                                          f"TL={tl_flat} TR={tr_flat}  "
                                          f"({elapsed:.1f}s, {outer_count/1e6:.1f}M outer, "
                                          f"{check_count/1e6:.1f}M inner checks)")

        if verbose and (tl_flat[0] * 6561 + tl_flat[1] * 729 + tl_flat[2] * 81 + tl_flat[3]) % 500 == 0:
            elapsed = time.time() - t0
            print(f"  TL={tl_flat}  {elapsed:.0f}s  outer={outer_count/1e6:.1f}M  "
                  f"inner={check_count/1e6:.1f}M  found={len(results)}")

    return results


if __name__ == "__main__":
    print("Finding all 8×8 Barron Squares (fast BOT-derivation method)...")
    print()

    t0 = time.time()
    squares = find_all_8x8(verbose=True)
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

        print("Validating all found squares...")
        for i, M in enumerate(squares):
            assert is_valid_barron(M, k=2), f"Square {i+1} FAILED validation!"
        print("All valid!")
