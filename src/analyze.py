"""
analyze.py — Statistical analysis of Barron Squares of any order k.

Produces:
  - Digit frequency tables (all cells, edge cells, corner cells, center)
  - Corner value distributions and most/least common corners
  - Product frequency (which 2-digit / 4-digit / ... products appear most)
  - Symmetry classification (identity, 90°, 180°, 270° rotation; reflection)
  - Uniqueness under symmetry (equivalence classes)
  - Corner correlation analysis (which corner values co-occur most)

Usage:
    from find_4x4 import find_all_4x4
    from analyze import full_analysis
    squares = find_all_4x4()
    full_analysis(squares, k=1)
"""

from collections import Counter, defaultdict
from barron_core import from_digits, to_digits
import math


# ---------------------------------------------------------------------------
# Matrix symmetries
# ---------------------------------------------------------------------------

def rotate90(M):
    n = len(M)
    return [[M[n - 1 - c][r] for c in range(n)] for r in range(n)]

def rotate180(M):
    return rotate90(rotate90(M))

def rotate270(M):
    return rotate90(rotate90(rotate90(M)))

def reflect_h(M):
    return [row[::-1] for row in M]

def reflect_v(M):
    return M[::-1]

def transpose(M):
    n = len(M)
    return [[M[c][r] for c in range(n)] for r in range(n)]

def antitranspose(M):
    n = len(M)
    return [[M[n-1-c][n-1-r] for c in range(n)] for r in range(n)]

SYMMETRY_OPS = {
    "identity":    lambda M: M,
    "rot90":       rotate90,
    "rot180":      rotate180,
    "rot270":      rotate270,
    "reflect_h":   reflect_h,
    "reflect_v":   reflect_v,
    "transpose":   transpose,
    "antitranspose": antitranspose,
}

def canonical_form(M) -> tuple:
    """Return the lexicographically smallest flat tuple among all 8 dihedral transforms."""
    flat = lambda m: tuple(v for row in m for v in row)
    return min(flat(op(M)) for op in SYMMETRY_OPS.values())

def symmetry_group(M) -> list[str]:
    """Return the names of symmetry operations that map M to itself."""
    flat = lambda m: tuple(v for row in m for v in row)
    orig = flat(M)
    return [name for name, op in SYMMETRY_OPS.items() if flat(op(M)) == orig]


# ---------------------------------------------------------------------------
# Cell region helpers
# ---------------------------------------------------------------------------

def cell_regions(n: int, k: int):
    """
    Return sets of (row, col) for each region:
      'corner', 'edge_noncorner', 'inner'
    """
    corners = set()
    for r in list(range(k)) + list(range(3*k, 4*k)):
        for c in list(range(k)) + list(range(3*k, 4*k)):
            corners.add((r, c))

    edges = set()
    for r in range(n):
        for c in range(n):
            if r < k or r >= 3*k or c < k or c >= 3*k:
                if (r, c) not in corners:
                    edges.add((r, c))

    inner = set()
    for r in range(k, 3*k):
        for c in range(k, 3*k):
            inner.add((r, c))

    return corners, edges, inner


# ---------------------------------------------------------------------------
# Core analysis
# ---------------------------------------------------------------------------

def digit_frequency(squares, positions=None):
    """Count digit occurrences. positions: set of (r,c) to restrict to."""
    counts = Counter()
    for M in squares:
        n = len(M)
        for r in range(n):
            for c in range(n):
                if positions is None or (r, c) in positions:
                    counts[M[r][c]] += 1
    return dict(sorted(counts.items()))

def corner_pair_frequency(squares, k):
    """
    For each pair of opposite corners (TL×TR, TL×BL, TR×BR, BL×BR),
    count how often each product value appears.
    """
    n = 4 * k
    products = Counter()
    for M in squares:
        L_top   = from_digits([M[0][c] for c in range(k)])
        R_top   = from_digits([M[0][n-k+c] for c in range(k)])
        L_bot   = from_digits([M[n-k][c] for c in range(k)])
        R_bot   = from_digits([M[n-k][n-k+c] for c in range(k)])
        products[L_top * R_top] += 1
        products[L_bot * R_bot] += 1
        products[L_top * L_bot] += 1
        products[R_top * R_bot] += 1
    return dict(sorted(products.items()))

def equivalence_classes(squares):
    """Group squares into dihedral symmetry equivalence classes."""
    seen = {}
    classes = []
    for M in squares:
        key = canonical_form(M)
        if key not in seen:
            seen[key] = len(classes)
            classes.append([M])
        else:
            classes[seen[key]].append(M)
    return classes

def symmetry_histogram(squares):
    """Count squares by size of their symmetry group (1 = asymmetric, 8 = fully symmetric)."""
    hist = Counter()
    for M in squares:
        hist[len(symmetry_group(M))] += 1
    return dict(sorted(hist.items()))

def corner_value_heatmap(squares, k):
    """
    For a 4×4 (k=1): return a 4×9 table:
      rows = corner position (TL, TR, BL, BR)
      cols = digit value 1–9
      cell = count
    """
    n = 4 * k
    positions = [
        (0, 0),        # TL
        (0, n - 1),    # TR  (for k=1 this is correct; for k>1 adapt)
        (n - 1, 0),    # BL
        (n - 1, n - 1) # BR
    ]
    table = defaultdict(Counter)
    for M in squares:
        for i, (r, c) in enumerate(positions):
            table[i][M[r][c]] += 1
    return table

def product_digit_distribution(squares, k):
    """
    For every edge product in every square, record which digit values appear
    in the product's digit positions. Returns Counter of digit values seen
    specifically in product positions (edges excluding corners).
    """
    n = 4 * k
    counts = Counter()
    for M in squares:
        # Top edge row 0, cols k..3k-1
        for c in range(k, 3*k):
            counts[M[0][c]] += 1
        # Bottom edge row n-1, cols k..3k-1
        for c in range(k, 3*k):
            counts[M[n-1][c]] += 1
        # Left edge col 0, rows k..3k-1
        for r in range(k, 3*k):
            counts[M[r][0]] += 1
        # Right edge col n-1, rows k..3k-1
        for r in range(k, 3*k):
            counts[M[r][n-1]] += 1
    return dict(sorted(counts.items()))


# ---------------------------------------------------------------------------
# Corner importance analysis
# ---------------------------------------------------------------------------

def corner_importance(squares, k):
    """
    Show that the corners are the "most important" cells:
    compute entropy of each cell's digit distribution across all squares.
    High entropy = more varied = more constrained / informative.

    Returns: n×n matrix of Shannon entropy values.
    """
    n = 4 * k
    cell_counts = [[Counter() for _ in range(n)] for _ in range(n)]
    for M in squares:
        for r in range(n):
            for c in range(n):
                cell_counts[r][c][M[r][c]] += 1

    N = len(squares)
    entropy = [[0.0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            for cnt in cell_counts[r][c].values():
                p = cnt / N
                if p > 0:
                    entropy[r][c] -= p * math.log2(p)
    return entropy


# ---------------------------------------------------------------------------
# Full analysis report
# ---------------------------------------------------------------------------

def full_analysis(squares: list, k: int, title: str = ""):
    """Print a comprehensive analysis report for a set of Barron Squares."""
    if not squares:
        print("No squares to analyze.")
        return

    n = 4 * k
    N = len(squares)
    corners, edges, inner = cell_regions(n, k)

    print("=" * 70)
    print(f"BARRON SQUARE ANALYSIS  (k={k}, matrix size {n}×{n})")
    if title:
        print(f"  {title}")
    print("=" * 70)
    print(f"\nTotal squares found: {N:,}")

    # --- Digit frequencies ---
    print("\n── Digit frequency: ALL cells ──")
    freq_all = digit_frequency(squares)
    total_cells = N * n * n
    for d, cnt in freq_all.items():
        bar = "█" * (cnt * 40 // max(freq_all.values()))
        print(f"  {d}: {cnt:8,}  ({100*cnt/total_cells:5.1f}%)  {bar}")

    print("\n── Digit frequency: CORNER cells ──")
    freq_corners = digit_frequency(squares, corners)
    total_corner = N * len(corners)
    for d, cnt in freq_corners.items():
        bar = "█" * (cnt * 40 // max(freq_corners.values()))
        print(f"  {d}: {cnt:8,}  ({100*cnt/total_corner:5.1f}%)  {bar}")

    print("\n── Digit frequency: EDGE (non-corner) cells ──")
    freq_edges = digit_frequency(squares, edges)
    total_edge = N * len(edges)
    for d, cnt in freq_edges.items():
        bar = "█" * (cnt * 40 // max(freq_edges.values()))
        print(f"  {d}: {cnt:8,}  ({100*cnt/total_edge:5.1f}%)  {bar}")

    print("\n── Digit frequency: INNER cells ──")
    freq_inner = digit_frequency(squares, inner)
    total_inner = N * len(inner)
    for d, cnt in freq_inner.items():
        bar = "█" * (cnt * 40 // max(freq_inner.values()))
        print(f"  {d}: {cnt:8,}  ({100*cnt/total_inner:5.1f}%)  {bar}")

    # --- Product (corner-pair) distribution ---
    print("\n── Product distribution (all edge products per square) ──")
    prod_freq = corner_pair_frequency(squares, k)
    max_pf = max(prod_freq.values())
    for p, cnt in sorted(prod_freq.items()):
        bar = "█" * (cnt * 30 // max_pf)
        print(f"  {p:4d}: {cnt:6,}  {bar}")

    # --- Symmetry ---
    print("\n── Symmetry group size distribution ──")
    sym_hist = symmetry_histogram(squares)
    for size, cnt in sym_hist.items():
        sym_names = {1: "asymmetric", 2: "one axis", 4: "two axes",
                     8: "fully symmetric (dihedral D4)"}
        label = sym_names.get(size, f"|G|={size}")
        print(f"  |G|={size}  ({label}): {cnt:,} squares")

    # --- Equivalence classes ---
    classes = equivalence_classes(squares)
    print(f"\n── Equivalence classes under dihedral symmetry ──")
    print(f"  {len(classes):,} distinct squares up to rotation/reflection")
    class_sizes = Counter(len(c) for c in classes)
    for size, cnt in sorted(class_sizes.items()):
        print(f"  Class size {size}: {cnt} classes ({cnt * size} squares)")

    # --- Corner entropy ---
    print("\n── Per-cell Shannon entropy (bits) across all squares ──")
    print("  (Higher entropy → more variation in that cell → more 'free')")
    ent = corner_importance(squares, k)
    for r in range(n):
        row_str = "  "
        for c in range(n):
            row_str += f"{ent[r][c]:.2f} "
        print(row_str)
    print()
    max_ent_cell = max((ent[r][c], r, c) for r in range(n) for c in range(n))
    min_ent_cell = min((ent[r][c], r, c) for r in range(n) for c in range(n))
    print(f"  Highest entropy: cell ({max_ent_cell[1]},{max_ent_cell[2]}) = "
          f"{max_ent_cell[0]:.3f} bits")
    print(f"  Lowest entropy:  cell ({min_ent_cell[1]},{min_ent_cell[2]}) = "
          f"{min_ent_cell[0]:.3f} bits")

    print("\n" + "=" * 70)
