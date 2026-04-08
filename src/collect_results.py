"""
collect_results.py — Collect and analyze 8×8 Barron Squares from parallel search output.

Usage:
    python src/collect_results.py /tmp/barron8x8_results/out_*.txt
    python src/collect_results.py /tmp/barron8x8_results/out_*.txt --analyze
"""

import sys, os, re, glob
sys.path.insert(0, os.path.dirname(__file__))

from barron_core import is_valid_barron, display
from analyze import full_analysis


def parse_output_file(path):
    """Parse a barron8x8 C output file, return list of (corners_str, matrix)."""
    squares = []
    with open(path) as f:
        text = f.read()

    # Find all squares
    pattern = r'TL=\([^)]+\)[^\n]*\n((?:[^\n]+\n){8})'
    for m in re.finditer(r'(TL=\([^)]+\)[^\n]*\n)', text):
        corners_line = m.group(1).strip()
        start = m.end()
        lines = text[start:].split('\n')
        # Parse next 8 matrix rows (filtering separators)
        matrix = []
        for line in lines:
            line = line.strip().replace('│', '').replace('┼', '').replace('─', '').replace('  ', ' ').strip()
            if not line or '┼' in line or '─' in line:
                continue
            digits = line.split()
            if len(digits) == 8:
                try:
                    matrix.append([int(d) for d in digits])
                except ValueError:
                    continue
            if len(matrix) == 8:
                break
        if len(matrix) == 8:
            squares.append((corners_line, matrix))

    return squares


def collect_all(output_dir_or_files):
    """Collect all squares from output files."""
    if isinstance(output_dir_or_files, str):
        files = sorted(glob.glob(output_dir_or_files))
    else:
        files = sorted(output_dir_or_files)

    all_squares = []
    seen = set()

    for path in files:
        if not os.path.exists(path):
            continue
        for corners, M in parse_output_file(path):
            key = tuple(M[r][c] for r in range(8) for c in range(8))
            if key not in seen:
                seen.add(key)
                all_squares.append(M)
                if not is_valid_barron(M, k=2):
                    print(f"WARNING: invalid square in {path}!")

    return all_squares


def summarize_search_progress(progress_dir):
    """Parse progress files to estimate completion."""
    prog_files = sorted(glob.glob(os.path.join(progress_dir, 'prog_*.txt')))
    print("=== Search Progress ===")
    total_found = 0
    for f in prog_files:
        with open(f) as fp:
            lines = [l.strip() for l in fp if l.strip()]
        if not lines:
            print(f"  {f}: no progress yet")
            continue
        last = lines[-1]
        # Parse: TL[99]  elapsed=27s  outer=6M  inner=1770M  found=1
        m = re.search(r'TL\[(\d+)\].*elapsed=(\d+)s.*found=(\d+)', last)
        if m:
            tl_idx = int(m.group(1))
            elapsed = int(m.group(2))
            found = int(m.group(3))
            total_found += found
            pct = tl_idx / 6561 * 100
            print(f"  {os.path.basename(f)}: TL[{tl_idx}] ({pct:.1f}%)  {elapsed}s  found={found}")
        else:
            print(f"  {os.path.basename(f)}: {last}")

    print(f"  Total found in progress logs: {total_found}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', default=['/tmp/barron8x8_results/out_*.txt'],
                        help='Output files or glob pattern')
    parser.add_argument('--analyze', action='store_true', help='Run full statistical analysis')
    parser.add_argument('--progress-dir', default='/tmp/barron8x8_results',
                        help='Directory containing progress files')
    args = parser.parse_args()

    # Collect all files
    all_files = []
    for pattern in args.files:
        all_files.extend(glob.glob(pattern))
    all_files = sorted(set(all_files))

    print(f"Collecting from {len(all_files)} files...")
    squares = collect_all(all_files)
    print(f"Unique valid 8×8 squares found: {len(squares)}")
    print()

    if args.progress_dir:
        summarize_search_progress(args.progress_dir)
        print()

    if squares:
        print("=== First 3 squares ===")
        for M in squares[:3]:
            print(display(M, k=2))
            print()

        if args.analyze and len(squares) > 10:
            full_analysis(squares, k=2, title=f"8×8 Barron Squares (partial: {len(squares)} found)")
