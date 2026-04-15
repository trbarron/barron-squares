#!/usr/bin/env python3
"""
verify_8x8.py — Independent verification of the 8x8 Barron Square count.

Two-phase verification:
  Phase 1: Validate all 1,248 stored squares using an independent checker
           (no shared code with barron8x8.c).
  Phase 2: Fresh exhaustive enumeration via verify_8x8.c (Full Corner
           Derivation algorithm), which uses a fundamentally different
           search decomposition from barron8x8.c's BOT-derivation.

Phase 2 details (verify_8x8.c):
  Algorithm: Full Corner Derivation (FCD)
    Free variables: TL (4 digits), TR (4 digits), BL (4 digits)
    Derived: BR from edge row/col constraints, inner block from consistency
  This differs from barron8x8.c's BOT-derivation:
    Free variables: TL (4), TR (4), col4_B (2), col5_B (2)
    Derived: BL, BR, inner block via bottom-of-table chain

  Verification result (2026-04-14/15):
    12 parallel workers, 160.8 total CPU hours, 19.2h max wall time.
    All 12 per-worker counts match expected, total = 1,248. PASSED.

Usage:
    # Phase 1 only (validation, seconds):
    python3 src/verify_8x8.py --validate-only

    # Phase 2: compile and run verify_8x8.c (see src/verify_8x8.c header)

    # Collect Phase 2 results:
    python3 src/collect_verify.py /tmp/verify_8x8/out_*.txt
"""

import json
import sys
import os
import time
import argparse


# ---------------------------------------------------------------------------
# Phase 1: Independent validation of stored squares
# ---------------------------------------------------------------------------

def validate_barron_8x8(M):
    """
    Validate that M is an 8x8 Barron Square (order k=2).

    Checks:
      - 8x8 dimensions
      - All 8 row constraints: left(2-digit) * right(2-digit) = interior(4-digit)
      - All 8 column constraints: top(2-digit) * bottom(2-digit) = interior(4-digit)
      - No zeros in edge cells (rows 0,1,6,7 or cols 0,1,6,7)

    This is a standalone implementation with no imports from barron_core.py.
    """
    if len(M) != 8 or any(len(row) != 8 for row in M):
        return False, "Wrong dimensions"

    # Check digit range
    for i in range(8):
        for j in range(8):
            if not (0 <= M[i][j] <= 9):
                return False, f"Cell ({i},{j}) = {M[i][j]} out of range"

    # Check no zeros on edges
    for i in range(8):
        for j in range(8):
            is_edge = (i < 2 or i >= 6 or j < 2 or j >= 6)
            if is_edge and M[i][j] == 0:
                return False, f"Zero at edge cell ({i},{j})"

    # Check row constraints
    for i in range(8):
        left = 10 * M[i][0] + M[i][1]
        right = 10 * M[i][6] + M[i][7]
        interior = 1000 * M[i][2] + 100 * M[i][3] + 10 * M[i][4] + M[i][5]
        if left * right != interior:
            return False, f"Row {i}: {left} * {right} = {left*right} != {interior}"

    # Check column constraints
    for j in range(8):
        top = 10 * M[0][j] + M[1][j]
        bottom = 10 * M[6][j] + M[7][j]
        interior = 1000 * M[2][j] + 100 * M[3][j] + 10 * M[4][j] + M[5][j]
        if top * bottom != interior:
            return False, f"Col {j}: {top} * {bottom} = {top*bottom} != {interior}"

    return True, "Valid"


def phase1_validate(squares_path):
    """Validate all stored 8x8 squares."""
    print("=" * 60)
    print("PHASE 1: Validating stored 8x8 Barron Squares")
    print("=" * 60)

    with open(squares_path) as f:
        squares = json.load(f)

    print(f"Loaded {len(squares)} squares from {squares_path}")

    t0 = time.time()
    failures = []
    for idx, sq in enumerate(squares):
        ok, msg = validate_barron_8x8(sq)
        if not ok:
            failures.append((idx, msg))

    elapsed = time.time() - t0

    if failures:
        print(f"\nFAILED: {len(failures)} squares failed validation:")
        for idx, msg in failures[:10]:
            print(f"  Square #{idx}: {msg}")
        return False
    else:
        print(f"\nPASSED: All {len(squares)} squares are valid 8x8 Barron Squares")
        print(f"Validation time: {elapsed:.3f}s")

        # Check for duplicates
        tuples = set()
        for sq in squares:
            tuples.add(tuple(tuple(row) for row in sq))
        if len(tuples) != len(squares):
            print(f"WARNING: {len(squares) - len(tuples)} duplicate squares found!")
            return False
        else:
            print(f"No duplicates: {len(tuples)} unique squares confirmed")
        return True


# ---------------------------------------------------------------------------
# Phase 2: Z3-based exhaustive enumeration
# ---------------------------------------------------------------------------

def phase2_enumerate(expected_count=1248):
    """
    Enumerate all 8x8 Barron Squares using Z3 bitvector SMT solver.

    Encodes each of the 64 cells as a BitVec(8) variable with:
      - Domain constraints: 0-9 for inner cells, 1-9 for edge cells
      - 8 row constraints: left * right = interior
      - 8 column constraints: top * bottom = interior

    Uses iterative blocking on the 16 corner variables to enumerate
    all solutions without redundancy.
    """
    print("\n" + "=" * 60)
    print("PHASE 2: Z3 exhaustive enumeration of 8x8 Barron Squares")
    print("=" * 60)

    try:
        from z3 import BitVec, BitVecVal, Solver, sat, Or, ZeroExt, UGE, ULE
    except ImportError:
        print("ERROR: z3-solver not available. Install with: pip install z3-solver")
        return None

    print("Building Z3 model...")
    t0 = time.time()

    s = Solver()

    # Create 64 cell variables (8-bit bitvectors, range 0-255)
    M = [[BitVec(f'm{i}{j}', 8) for j in range(8)] for i in range(8)]

    # Domain constraints
    for i in range(8):
        for j in range(8):
            s.add(ULE(M[i][j], BitVecVal(9, 8)))
            is_edge = (i < 2 or i >= 6 or j < 2 or j >= 6)
            if is_edge:
                s.add(UGE(M[i][j], BitVecVal(1, 8)))

    # Helper: zero-extend to 16-bit for multiplication
    def ext(v):
        return ZeroExt(8, v)

    ten = BitVecVal(10, 16)
    hundred = BitVecVal(100, 16)
    thousand = BitVecVal(1000, 16)

    # Row constraints: left * right = interior
    for i in range(8):
        left = ext(M[i][0]) * ten + ext(M[i][1])
        right = ext(M[i][6]) * ten + ext(M[i][7])
        interior = (ext(M[i][2]) * thousand + ext(M[i][3]) * hundred +
                    ext(M[i][4]) * ten + ext(M[i][5]))
        s.add(left * right == interior)

    # Column constraints: top * bottom = interior
    for j in range(8):
        top = ext(M[0][j]) * ten + ext(M[1][j])
        bottom = ext(M[6][j]) * ten + ext(M[7][j])
        interior = (ext(M[2][j]) * thousand + ext(M[3][j]) * hundred +
                    ext(M[4][j]) * ten + ext(M[5][j]))
        s.add(top * bottom == interior)

    # Corner variables (for blocking clauses)
    corners = []
    for i in (0, 1, 6, 7):
        for j in (0, 1, 6, 7):
            corners.append(M[i][j])

    build_time = time.time() - t0
    print(f"Model built in {build_time:.2f}s ({len(corners)} corner variables)")
    print(f"Enumerating solutions (blocking on {len(corners)} corner vars)...")
    print()

    t_enum = time.time()
    count = 0
    solutions = []

    while True:
        result = s.check()
        if result != sat:
            break

        model = s.model()
        count += 1

        # Extract the matrix
        matrix = []
        for i in range(8):
            row = []
            for j in range(8):
                val = model.eval(M[i][j]).as_long()
                row.append(val)
            matrix.append(row)
        solutions.append(matrix)

        # Verify this solution with our independent checker
        ok, msg = validate_barron_8x8(matrix)
        if not ok:
            print(f"  ERROR: Z3 solution #{count} fails validation: {msg}")
            print(f"  Matrix: {matrix}")
            return None

        # Block this solution (on corner variables only)
        block = Or([c != model.eval(c) for c in corners])
        s.add(block)

        # Progress reporting
        if count % 50 == 0:
            elapsed = time.time() - t_enum
            rate = count / elapsed if elapsed > 0 else 0
            print(f"  Found {count:,} squares ({rate:.1f}/s, {elapsed:.1f}s elapsed)")

    total_time = time.time() - t_enum

    print(f"\nEnumeration complete.")
    print(f"  Total squares found: {count:,}")
    print(f"  Enumeration time: {total_time:.1f}s ({total_time/60:.1f} min)")
    print(f"  Average rate: {count/total_time:.2f} squares/s" if total_time > 0 else "")

    if count == expected_count:
        print(f"\n  PASSED: Count matches expected {expected_count}")
    else:
        print(f"\n  FAILED: Found {count}, expected {expected_count}")

    return solutions


# ---------------------------------------------------------------------------
# Phase 3 (optional): Cross-check Z3 solutions against stored squares
# ---------------------------------------------------------------------------

def cross_check(z3_solutions, stored_path):
    """Verify Z3 solutions match stored squares exactly."""
    print("\n" + "=" * 60)
    print("CROSS-CHECK: Comparing Z3 solutions with stored squares")
    print("=" * 60)

    with open(stored_path) as f:
        stored = json.load(f)

    z3_set = set(tuple(tuple(r) for r in sq) for sq in z3_solutions)
    stored_set = set(tuple(tuple(r) for r in sq) for sq in stored)

    only_z3 = z3_set - stored_set
    only_stored = stored_set - z3_set
    common = z3_set & stored_set

    print(f"  Z3 found:     {len(z3_set)} unique squares")
    print(f"  Stored:       {len(stored_set)} unique squares")
    print(f"  In common:    {len(common)}")
    print(f"  Only in Z3:   {len(only_z3)}")
    print(f"  Only stored:  {len(only_stored)}")

    if only_z3:
        print("\n  Squares found by Z3 but not in stored file:")
        for sq in list(only_z3)[:3]:
            print(f"    {list(list(r) for r in sq)}")

    if only_stored:
        print("\n  Squares in stored file but not found by Z3:")
        for sq in list(only_stored)[:3]:
            print(f"    {list(list(r) for r in sq)}")

    if not only_z3 and not only_stored:
        print("\n  PASSED: Perfect match between Z3 enumeration and stored squares")
        return True
    else:
        print("\n  FAILED: Mismatch detected")
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Independent verification of 8x8 Barron Squares")
    parser.add_argument("--validate-only", action="store_true",
                        help="Only run Phase 1 (validate stored squares)")
    parser.add_argument("--enumerate-only", action="store_true",
                        help="Only run Phase 2 (Z3 enumeration)")
    parser.add_argument("--squares", default=None,
                        help="Path to 8x8_squares.json")
    args = parser.parse_args()

    # Find the squares file
    squares_path = args.squares
    if squares_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        squares_path = os.path.join(script_dir, "..", "results", "8x8_squares.json")

    t_start = time.time()
    all_passed = True

    if not args.enumerate_only:
        if not os.path.exists(squares_path):
            print(f"ERROR: Squares file not found: {squares_path}")
            sys.exit(1)
        passed = phase1_validate(squares_path)
        all_passed = all_passed and passed

    z3_solutions = None
    if not args.validate_only:
        z3_solutions = phase2_enumerate(expected_count=1248)
        if z3_solutions is None:
            all_passed = False
        elif len(z3_solutions) != 1248:
            all_passed = False

    if z3_solutions and not args.enumerate_only and os.path.exists(squares_path):
        passed = cross_check(z3_solutions, squares_path)
        all_passed = all_passed and passed

    total_time = time.time() - t_start
    print(f"\n{'='*60}")
    print(f"VERIFICATION {'PASSED' if all_passed else 'FAILED'}")
    print(f"Total time: {total_time:.1f}s ({total_time/3600:.2f} hours)")
    print(f"{'='*60}")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
