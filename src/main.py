"""
main.py — Run the full Barron Squares analysis pipeline.

Stages:
  1. Find all 4×4 Barron Squares (exhaustive, instant)
  2. Analyze 4×4 squares statistically
  3. Find all 8×8 Barron Squares (exhaustive with pruning, minutes)
  4. Analyze 8×8 squares statistically
  5. Find 4×4×4 Barron Cubes (exhaustive, ~minutes)
  6. Search for 16×16 Barron Squares (random search)

Usage:
    python src/main.py [--skip-8x8] [--skip-cube] [--skip-16x16]
"""

import sys
import os
import time
import argparse

# Make the src/ directory importable
sys.path.insert(0, os.path.dirname(__file__))

from barron_core import display, is_valid_barron
from find_4x4 import find_all_4x4, summarize as summarize_4x4
from find_8x8 import find_all_8x8_fast
from find_nxn import random_search
from analyze import full_analysis
from barron_3d import find_all_barron_cubes_k1, is_valid_barron_cube


def section(title: str):
    print()
    print("╔" + "═" * (len(title) + 4) + "╗")
    print(f"║  {title}  ║")
    print("╚" + "═" * (len(title) + 4) + "╝")
    print()


def run_4x4():
    section("4×4 BARRON SQUARES  (k=1, exhaustive)")
    t0 = time.time()
    squares = find_all_4x4()
    elapsed = time.time() - t0
    print(f"Found {len(squares):,} valid 4×4 Barron Squares in {elapsed:.3f}s\n")

    # Verify the known example
    example = [[6,4,2,7],[4,2,0,5],[8,4,8,6],[8,6,4,8]]
    assert is_valid_barron(example, k=1), "Known example failed validation!"
    print("Known example from FiveThirtyEight Riddler:")
    print(display(example, k=1))
    print()

    # Show a few squares
    print("Sample squares:")
    for M in squares[:3]:
        print(display(M, k=1))
        print()

    full_analysis(squares, k=1, title="All 4×4 Barron Squares")
    return squares


def run_8x8(verbose=True):
    section("8×8 BARRON SQUARES  (k=2, exhaustive with pruning)")
    print("Note: This search may take several minutes.\n")
    t0 = time.time()
    squares = find_all_8x8_fast(verbose=verbose)
    elapsed = time.time() - t0
    print(f"\nFound {len(squares):,} valid 8×8 Barron Squares in {elapsed:.1f}s")

    if squares:
        full_analysis(squares, k=2, title="All 8×8 Barron Squares")
    return squares


def run_cube(verbose=True):
    section("4×4×4 BARRON CUBES  (3D, k=1)")
    print("Enumerating 9^8 = 43,046,721 corner octuplets...\n")
    t0 = time.time()
    cubes = find_all_barron_cubes_k1(verbose=verbose)
    elapsed = time.time() - t0
    print(f"\nFound {len(cubes)} valid 4×4×4 Barron Cubes in {elapsed:.1f}s")

    for i, cube in enumerate(cubes):
        assert is_valid_barron_cube(cube, k=1), f"Cube #{i+1} failed validation!"
    print("All cubes validated.")
    return cubes


def run_16x16(trials=500_000):
    section("16×16 BARRON SQUARES  (k=4, random search)")
    print(f"Running {trials:,} random trials...\n")
    t0 = time.time()
    squares = random_search(k=4, trials=trials, verbose=True)
    elapsed = time.time() - t0
    print(f"\nFound {len(squares)} valid 16×16 Barron Squares in {elapsed:.1f}s")

    if squares:
        print("\nFirst 16×16 square found:")
        print(display(squares[0], k=4))
    return squares


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-8x8",    action="store_true")
    parser.add_argument("--skip-cube",   action="store_true")
    parser.add_argument("--skip-16x16",  action="store_true")
    parser.add_argument("--quiet",       action="store_true")
    args = parser.parse_args()

    print("=" * 70)
    print("  BARRON SQUARES — COMPLETE ANALYSIS PIPELINE")
    print("=" * 70)

    squares_4x4 = run_4x4()

    if not args.skip_8x8:
        squares_8x8 = run_8x8(verbose=not args.quiet)

    if not args.skip_cube:
        cubes = run_cube(verbose=not args.quiet)

    if not args.skip_16x16:
        squares_16x16 = run_16x16()

    print("\nDone.")


if __name__ == "__main__":
    main()
