"""
barron_3d.py — 3D Barron Cubes (and higher-dimensional generalizations).

Definition
──────────
A Barron Cube of order k is a (4k × 4k × 4k) array of decimal digits (0–9)
such that EVERY axis-aligned line satisfies the Barron property:

  For any direction d ∈ {x, y, z} and any 2D position (i, j) perpendicular to d,
  the line L(d, i, j) of length 4k satisfies:

      from_digits(L[0..k-1]) × from_digits(L[3k..4k-1])
        = from_digits(L[k..3k-1])   (as a 2k-digit number)

  AND no edge element (first k or last k along any axis direction) is 0.

Equivalently, thinking of each "face" of the cube:
  - Every row in the xy-plane: satisfies Barron
  - Every row in the xz-plane: satisfies Barron
  - Every row in the yz-plane: satisfies Barron

Structure
──────────
The free parameters are the 8 corner k×k×k blocks (one at each vertex of the cube).
All other cells are overdetermined and subject to consistency conditions.

For k=1 (4×4×4 cube): 8 scalar corners (each 1–9), 8 free parameters.
  - Each face of the cube becomes a 4×4 Barron Square.
  - Internal consistency across faces is required.

This is a dramatically over-constrained system:
  - 3 axes × (4k)^2 lines each = 3 × 16 = 48 lines for k=1
  - Each line's middle 2k cells determined by its endpoints
  - Many cells are constrained by lines in multiple directions simultaneously

Finding Barron Cubes
──────────────────────
For k=1: enumerate all 9^8 = 43,046,721 corner octuplets.
For each, build the cube and check consistency.

This is the 3D analogue of finding 4×4 Barron Squares (9^4 combinations).

Usage:
    python src/barron_3d.py
"""

from barron_core import to_digits, from_digits
from itertools import product as iproduct
from typing import Optional


# ---------------------------------------------------------------------------
# 3D array helpers
# ---------------------------------------------------------------------------

def make_cube(n: int) -> list:
    """Return an n×n×n zero-initialized 3D list."""
    return [[[0] * n for _ in range(n)] for _ in range(n)]


def get_line(cube: list, axis: int, i: int, j: int) -> list[int]:
    """
    Extract a line from the cube along the given axis.

    axis=0 (x-axis): varies x, fixed (y=i, z=j) → cube[x][i][j]
    axis=1 (y-axis): varies y, fixed (x=i, z=j) → cube[i][y][j]
    axis=2 (z-axis): varies z, fixed (x=i, y=j) → cube[i][j][z]
    """
    n = len(cube)
    if axis == 0:
        return [cube[x][i][j] for x in range(n)]
    elif axis == 1:
        return [cube[i][y][j] for y in range(n)]
    else:
        return [cube[i][j][z] for z in range(n)]


def set_line(cube: list, axis: int, i: int, j: int, values: list[int]):
    """Set a line in the cube (inverse of get_line)."""
    n = len(cube)
    for idx, v in enumerate(values):
        if axis == 0:
            cube[idx][i][j] = v
        elif axis == 1:
            cube[i][idx][j] = v
        else:
            cube[i][j][idx] = v


def barron_fill_middle(line: list[int], k: int) -> Optional[list[int]]:
    """
    Given a line of length 4k with ends filled (positions 0..k-1 and 3k..4k-1),
    return the line with the 2k middle positions filled by the Barron constraint.
    Returns None if the product overflows (>2k digits).
    """
    n = 4 * k
    left  = from_digits(line[:k])
    right = from_digits(line[n-k:])
    mid   = to_digits(left * right, 2 * k)
    result = line[:]
    result[k:3*k] = mid
    return result


# ---------------------------------------------------------------------------
# Cube construction
# ---------------------------------------------------------------------------

def build_cube_k1(corners: list[int]) -> Optional[list]:
    """
    Build a 4×4×4 Barron Cube (k=1) from 8 corner values.

    corners = [c000, c001, c010, c011, c100, c101, c110, c111]
    Corner positions: corners[b0*4+b1*2+b2] = M[b0*3][b1*3][b2*3]
    i.e., corners[0]=M[0][0][0], corners[1]=M[0][0][3], corners[2]=M[0][3][0],
          corners[3]=M[0][3][3], corners[4]=M[3][0][0], corners[5]=M[3][0][3],
          corners[6]=M[3][3][0], corners[7]=M[3][3][3]

    Algorithm:
    1. Place corners
    2. Fill 12 cube edges (each edge = one axis-aligned line between 2 corners)
    3. Fill 6 face interiors using one axis, verify with second axis
    4. Fill 8 cube interior cells using x-axis, verify with y and z axes
    5. Check no-zero edge constraint

    Returns the 4×4×4 cube or None if inconsistent/invalid.
    """
    k = 1
    n = 4
    M = make_cube(n)

    def fill_and_check(axis, i, j) -> bool:
        """Fill middle of line using Barron constraint, check no-zero edge."""
        line = get_line(M, axis, i, j)
        filled = barron_fill_middle(line, k)
        # Check if any previously-set inner cell disagrees
        for pos in range(k, 3*k):
            if line[pos] != 0 and line[pos] != filled[pos]:
                return False  # inconsistency
        set_line(M, axis, i, j, filled)
        return True

    def verify_line(axis, i, j) -> bool:
        """Verify the inner cells of a line are consistent with Barron constraint."""
        line = get_line(M, axis, i, j)
        filled = barron_fill_middle(line, k)
        for pos in range(k, 3*k):
            if line[pos] != filled[pos]:
                return False
        return True

    # Step 1: Place corners
    c = corners
    M[0][0][0]=c[0]; M[0][0][3]=c[1]; M[0][3][0]=c[2]; M[0][3][3]=c[3]
    M[3][0][0]=c[4]; M[3][0][3]=c[5]; M[3][3][0]=c[6]; M[3][3][3]=c[7]

    # Step 2: Fill 12 edges of the cube
    # 4 z-axis edges (x,y both edge values)
    for x, y in [(0,0),(0,3),(3,0),(3,3)]:
        if not fill_and_check(2, x, y): return None
    # 4 x-axis edges (y,z both edge values)
    for y, z in [(0,0),(0,3),(3,0),(3,3)]:
        if not fill_and_check(0, y, z): return None
    # 4 y-axis edges (x,z both edge values)
    for x, z in [(0,0),(0,3),(3,0),(3,3)]:
        if not fill_and_check(1, x, z): return None

    # Step 3: Fill 6 face interiors
    # Face x=0, x=3: inner cells at (x_face, y∈{1,2}, z∈{1,2})
    # Fill using z-axis lines (y varies as index), verify with y-axis lines
    for x_face in [0, 3]:
        for y in [1, 2]:
            if not fill_and_check(2, x_face, y): return None  # sets M[x_face][y][1..2]
        for z in [1, 2]:
            if not verify_line(1, x_face, z): return None  # verify y-lines

    # Face y=0, y=3: inner cells at (x∈{1,2}, y_face, z∈{1,2})
    # Fill using z-axis lines, verify with x-axis lines
    for y_face in [0, 3]:
        for x in [1, 2]:
            if not fill_and_check(2, x, y_face): return None  # sets M[x][y_face][1..2]
        for z in [1, 2]:
            if not verify_line(0, y_face, z): return None  # verify x-lines

    # Face z=0, z=3: inner cells at (x∈{1,2}, y∈{1,2}, z_face)
    # Fill using x-axis lines, verify with y-axis lines
    for z_face in [0, 3]:
        for y in [1, 2]:
            if not fill_and_check(0, y, z_face): return None  # sets M[1..2][y][z_face]
        for x in [1, 2]:
            if not verify_line(1, x, z_face): return None  # verify y-lines

    # Step 4: Fill 8 interior cells at (x,y,z) ∈ {1,2}^3
    # Fill using x-axis lines for (y,z) ∈ {1,2}^2, verify with y and z axes
    for y in [1, 2]:
        for z in [1, 2]:
            if not fill_and_check(0, y, z): return None
    for x in [1, 2]:
        for z in [1, 2]:
            if not verify_line(1, x, z): return None
    for x in [1, 2]:
        for y in [1, 2]:
            if not verify_line(2, x, y): return None

    # Step 5: Check no-zero edge constraint
    for x in range(4):
        for y in range(4):
            for z in range(4):
                if (x in (0,3) or y in (0,3) or z in (0,3)) and M[x][y][z] == 0:
                    return None

    return M


def is_valid_barron_cube(M: list, k: int) -> bool:
    """Validate that every line in all 3 axis directions satisfies the Barron property."""
    n = 4 * k
    for axis in range(3):
        for i in range(n):
            for j in range(n):
                line = get_line(M, axis, i, j)
                left  = from_digits(line[:k])
                right = from_digits(line[n-k:])
                mid   = from_digits(line[k:3*k])
                if left * right != mid:
                    return False
                # No zeros on edges
                for pos in list(range(k)) + list(range(3*k, n)):
                    if line[pos] == 0:
                        return False
    return True


def find_all_barron_cubes_k1(verbose: bool = True) -> list:
    """
    Find all 4×4×4 Barron Cubes by enumerating all 9^8 = 43,046,721
    corner octuplets (each corner digit in 1–9).

    Returns list of valid 4×4×4 cubes.
    """
    results = []
    total = 0
    for corners in iproduct(range(1, 10), repeat=8):
        total += 1
        if verbose and total % 1_000_000 == 0:
            print(f"  Checked {total:,}, found {len(results)}")
        M = build_cube_k1(list(corners))
        if M is not None:
            results.append(M)
            if verbose:
                print(f"  Found cube #{len(results)}: corners={corners}")
    if verbose:
        print(f"  Total checked: {total:,}")
    return results


def display_cube_slice(M: list, axis: int, idx: int) -> str:
    """Display a 2D slice of a 3D cube."""
    n = len(M)
    if axis == 0:
        grid = M[idx]
    elif axis == 1:
        grid = [[M[x][idx][z] for z in range(n)] for x in range(n)]
    else:
        grid = [[M[x][y][idx] for y in range(n)] for x in range(n)]
    return "\n".join("  " + " ".join(str(v) for v in row) for row in grid)


if __name__ == "__main__":
    print("Finding all 4×4×4 Barron Cubes (k=1)...")
    print("Enumerating 9^8 = 43,046,721 corner combinations.\n")

    import time
    t0 = time.time()
    cubes = find_all_barron_cubes_k1(verbose=True)
    elapsed = time.time() - t0

    print(f"\n{'='*60}")
    print(f"Total 4×4×4 Barron Cubes found: {len(cubes)}")
    print(f"Time: {elapsed:.1f}s")
    print("=" * 60)

    for i, cube in enumerate(cubes[:3]):
        print(f"\nCube #{i+1}:")
        for ax in range(3):
            for sl in range(4):
                print(f"  Slice axis={ax}, index={sl}:")
                print(display_cube_slice(cube, ax, sl))
        assert is_valid_barron_cube(cube, k=1), "VALIDATION FAILED!"
