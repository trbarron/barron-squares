"""
find_4x4.py — Enumerate all 4×4 Barron Squares (k=1).

For k=1 the four corners are single digits in 1–9, giving at most
9^4 = 6,561 corner combinations to check.  The search completes
in milliseconds.

Usage:
    python src/find_4x4.py
"""

from barron_core import build_matrix, display, is_valid_barron
from itertools import product as iproduct


def find_all_4x4(verbose: bool = True) -> list[list[list[int]]]:
    """Return every valid 4×4 Barron Square."""
    k = 1
    results = []
    for a, b, c, d in iproduct(range(1, 10), repeat=4):
        tl = [[a]]
        tr = [[b]]
        bl = [[c]]
        br = [[d]]
        M = build_matrix(tl, tr, bl, br, k)
        if M is not None:
            results.append(M)
    return results


def corner_signature(M: list[list[int]]) -> tuple[int, int, int, int]:
    """Return the four corner values of a 4×4 matrix."""
    return (M[0][0], M[0][3], M[3][0], M[3][3])


def summarize(squares: list[list[list[int]]]) -> dict:
    """Compute summary statistics over found squares."""
    from collections import Counter

    stats = {}
    stats["count"] = len(squares)

    # Corner distribution
    corners = [corner_signature(M) for M in squares]
    corner_flat = [v for c in corners for v in c]
    stats["corner_digit_freq"] = dict(sorted(Counter(corner_flat).items()))

    # Digit frequency across entire matrix
    all_digits = [M[r][c] for M in squares for r in range(4) for c in range(4)]
    stats["digit_freq_all"] = dict(sorted(Counter(all_digits).items()))

    # Digit frequency on edges only
    edge_digits = []
    for M in squares:
        for r in range(4):
            for c in range(4):
                if r in (0, 3) or c in (0, 3):
                    edge_digits.append(M[r][c])
    stats["digit_freq_edges"] = dict(sorted(Counter(edge_digits).items()))

    # Product distribution (value of TL×TR, TL×BL, TR×BR, BL×BR)
    products = []
    for M in squares:
        products += [
            M[0][0] * M[0][3],  # top row: TL × TR
            M[3][0] * M[3][3],  # bottom row: BL × BR
            M[0][0] * M[3][0],  # left col: TL × BL
            M[0][3] * M[3][3],  # right col: TR × BR
        ]
    stats["product_freq"] = dict(sorted(Counter(products).items()))

    # Symmetric squares (those invariant under 90° rotation)
    stats["symmetric_count"] = sum(
        1 for M in squares if M == rotate90(M)
    )

    # Palindromic squares (symmetric under transposition M = Mᵀ)
    stats["transposed_count"] = sum(
        1 for M in squares if M == transpose(M)
    )

    return stats


def rotate90(M: list[list[int]]) -> list[list[int]]:
    n = len(M)
    return [[M[n - 1 - c][r] for c in range(n)] for r in range(n)]


def transpose(M: list[list[int]]) -> list[list[int]]:
    n = len(M)
    return [[M[c][r] for c in range(n)] for r in range(n)]


if __name__ == "__main__":
    print("Finding all 4×4 Barron Squares...")
    squares = find_all_4x4()
    print(f"\nTotal found: {len(squares)}\n")

    print("=" * 50)
    print("Sample squares (first 5):")
    print("=" * 50)
    for M in squares[:5]:
        print(display(M, k=1))
        tl, tr, bl, br = M[0][0], M[0][3], M[3][0], M[3][3]
        print(f"  Corners: TL={tl} TR={tr} BL={bl} BR={br}")
        print(f"  Products: {tl}×{tr}={tl*tr}  {bl}×{br}={bl*br}  "
              f"{tl}×{bl}={tl*bl}  {tr}×{br}={tr*br}")
        assert is_valid_barron(M, k=1), "VALIDATION FAILED!"
        print()

    print("=" * 50)
    print("Statistics:")
    print("=" * 50)
    stats = summarize(squares)
    print(f"  Total squares:          {stats['count']:,}")
    print(f"  Rotationally symmetric: {stats['symmetric_count']}")
    print(f"  Transposition-symmetric:{stats['transposed_count']}")
    print()
    print("  Corner digit frequency:")
    for d, freq in stats["corner_digit_freq"].items():
        print(f"    {d}: {freq:5d}  ({100*freq/(4*stats['count']):.1f}%)")
    print()
    print("  Product frequency (all 4 products per square):")
    for p, freq in sorted(stats["product_freq"].items()):
        print(f"    {p:2d}: {freq:5d}")
    print()
    print("  All-digit frequency across all cells:")
    for d, freq in stats["digit_freq_all"].items():
        print(f"    {d}: {freq:6d}  ({100*freq/(16*stats['count']):.1f}%)")
