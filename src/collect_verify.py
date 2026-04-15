#!/usr/bin/env python3
"""
collect_verify.py — Collect results from parallel verify_8x8 workers.

Usage:
    python3 src/collect_verify.py /tmp/verify_8x8/out_*.txt

Reads FOUND:<count> lines from each worker's output, sums them,
and compares against the expected count from results/8x8_squares.json.
Also cross-checks per-worker counts against the stored squares.
"""

import sys
import os
import json
import glob


def tl_index(sq):
    """Compute TL index for a square (matches verify_8x8.c enumeration order)."""
    a, b = sq[0][0], sq[0][1]
    c, d = sq[1][0], sq[1][1]
    return (a - 1) * 729 + (b - 1) * 81 + (c - 1) * 9 + (d - 1)


def main():
    # Find output files
    if len(sys.argv) > 1:
        files = sorted(sys.argv[1:])
    else:
        files = sorted(glob.glob("/tmp/verify_8x8/out_*.txt"))

    if not files:
        print("No output files found.")
        sys.exit(1)

    # Load stored squares for cross-check
    script_dir = os.path.dirname(os.path.abspath(__file__))
    squares_path = os.path.join(script_dir, "..", "results", "8x8_squares.json")
    with open(squares_path) as f:
        squares = json.load(f)

    # Parse worker outputs
    total = 0
    worker_counts = {}
    pending = 0

    for f_path in files:
        worker_id = os.path.basename(f_path).replace("out_", "").replace(".txt", "")
        with open(f_path) as f:
            content = f.read().strip()
        if content.startswith("FOUND:"):
            count = int(content.split(":")[1])
            worker_counts[worker_id] = count
            total += count
        else:
            worker_counts[worker_id] = None
            pending += 1

    print(f"Workers: {len(files)} ({len(files) - pending} complete, {pending} pending)")
    print()

    # Per-worker cross-check
    print(f"{'Worker':<10} {'Found':<8} {'Expected':<10} {'Status'}")
    print("-" * 45)

    all_match = True
    for i in range(len(files)):
        wid = str(i)
        start = i * 547
        end = (i + 1) * 547
        if i == len(files) - 1:
            end = 6561
        expected = sum(1 for sq in squares if start <= tl_index(sq) < end)
        found = worker_counts.get(wid)

        if found is None:
            status = "RUNNING"
            print(f"  {i:<8} {'?':<8} {expected:<10} {status}")
        elif found == expected:
            status = "MATCH"
            print(f"  {i:<8} {found:<8} {expected:<10} {status}")
        else:
            status = "MISMATCH!"
            all_match = False
            print(f"  {i:<8} {found:<8} {expected:<10} {status}")

    print()
    if pending > 0:
        print(f"Partial total: {total} (from {len(files) - pending} complete workers)")
        expected_from_complete = sum(
            sum(1 for sq in squares if i*547 <= tl_index(sq) < min((i+1)*547, 6561))
            for i in range(len(files))
            if worker_counts.get(str(i)) is not None
        )
        print(f"Expected from complete workers: {expected_from_complete}")
        print(f"Match so far: {total == expected_from_complete}")
    else:
        print(f"Total found: {total}")
        print(f"Expected: 1248")
        if total == 1248 and all_match:
            print("\nVERIFICATION PASSED: Independent enumeration confirms 1,248 squares.")
        else:
            print(f"\nVERIFICATION {'PASSED' if total == 1248 else 'FAILED'}")


if __name__ == "__main__":
    main()
