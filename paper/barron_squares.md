# Barron Squares: A Multiplicative Structure on Integer Grids

**Tyler Barron**  
*Preprint, 2026*

---

## Abstract

We introduce **Barron Squares**, a family of integer-digit matrices satisfying a multiplicative boundary condition: in any row or column, the product of the two "endpoint" digit-groups equals the "interior" digit-group read as an integer. We completely characterize the 4×4 case (finding exactly **118** valid squares via exhaustive enumeration), develop the algebraic consistency conditions that govern their existence, partially enumerate the 8×8 case (finding **≥ 157** squares with an ongoing C implementation), and prove that **no valid 4×4×4 Barron Cubes exist** (verified by exhaustive search over 9^8 = 43,046,721 corner combinations). Key structural results include: the corner values are the sole free parameters; digit 1 is excluded from 4×4 corners but appears in 8×8; none of the found squares exhibit rotational symmetry; and 8×8 squares show dramatically higher transpose-symmetry rates (≥69%) than 4×4 squares (39%).

---

## 1. Introduction

Consider a 4×4 matrix of single decimal digits. We say the matrix is a **Barron Square** if every row and every column satisfies a multiplicative property: the leftmost digit times the rightmost digit equals the two-digit number formed by the two interior digits.

**Definition 1.1** (4×4 Barron Square). A matrix $M \in \{0,\ldots,9\}^{4\times 4}$ is a *Barron Square of order 1* if:

1. For every row $i$: $M_{i,0} \times M_{i,3} = 10 \cdot M_{i,1} + M_{i,2}$
2. For every column $j$: $M_{0,j} \times M_{3,j} = 10 \cdot M_{1,j} + M_{2,j}$
3. **No-zero edge condition**: no cell in the border (row 0, row 3, column 0, or column 3) equals 0.

**Example 1.2.** The following matrix, which appeared as a FiveThirtyEight Riddler Express puzzle, is a Barron Square:

$$\begin{pmatrix} 6 & 4 & 2 & 7 \\ 4 & 2 & 0 & 5 \\ 8 & 4 & 8 & 6 \\ 8 & 6 & 4 & 8 \end{pmatrix}$$

Verification: rows give $6\times7=42$, $4\times5=20$, $8\times6=48$, $8\times8=64$; columns give $6\times8=48$, $4\times6=24$, $2\times4=8$ (read as "08"), $7\times8=56$. Note that the inner zero in row 1 is permitted because it lies on a non-edge cell.

---

## 2. The Corner Theorem

The most fundamental structural result is that a Barron Square is **completely determined by its four corner values**.

**Theorem 2.1** (Corner Determination). Let $a = M_{0,0}$, $b = M_{0,3}$, $c = M_{3,0}$, $d = M_{3,3}$ be the four corners of a 4×4 Barron Square. Then every cell is uniquely determined:

- **Edge rows**: $M_{0,1} = \lfloor ab/10 \rfloor$, $M_{0,2} = ab \bmod 10$ and analogously for row 3.
- **Edge columns**: $M_{1,0} = \lfloor ac/10 \rfloor$, $M_{2,0} = ac \bmod 10$ and analogously for column 3.
- **Inner rows**: $M_{1,1}$, $M_{1,2}$ are determined by the row-1 product $M_{1,0} \times M_{1,3}$.
- **Inner columns**: $M_{1,1}$, $M_{2,1}$ are determined by the col-1 product $M_{0,1} \times M_{3,1}$.

*Proof.* Apply the row and column constraints inductively from the boundary inward. $\square$

**Notation.** Let $t(n) = \lfloor n/10 \rfloor$ (tens digit) and $u(n) = n \bmod 10$ (units digit).

**Corollary 2.2** (Algebraic Consistency Conditions). Four nonzero digits $(a,b,c,d)$ yield a valid 4×4 Barron Square if and only if all four edge products $ab$, $cd$, $ac$, $bd$ have nonzero digits **and** the following hold:

$$t\!\left(t(ac)\cdot t(bd)\right) = t\!\left(t(ab)\cdot t(cd)\right) \tag{C1}$$
$$u\!\left(t(ac)\cdot t(bd)\right) = t\!\left(u(ab)\cdot u(cd)\right) \tag{C2}$$
$$t\!\left(u(ac)\cdot u(bd)\right) = u\!\left(t(ab)\cdot t(cd)\right) \tag{C3}$$

**Proposition 2.3.** The fourth potential consistency condition $u(u(ac)\cdot u(bd)) = u(u(ab)\cdot u(cd))$ is **always satisfied** for any $(a,b,c,d)$, since both sides equal $abcd \bmod 10$.

This means only three genuinely restrictive conditions govern corner validity.

---

## 3. Enumeration of 4×4 Barron Squares

**Theorem 3.1.** There are exactly **118** Barron Squares of order 1 (4×4).

*Proof.* Exhaustive enumeration over all $9^4 = 6{,}561$ nonzero corner quadruples $(a,b,c,d)$. $\square$

### 3.1 Excluded Corner Values

**Proposition 3.2.** The digit **1 cannot appear** as any corner value in a 4×4 Barron Square.

*Proof.* If $a = 1$, then $a \cdot b = b \leq 9$ for any $b \in \{1,\ldots,9\}$. The two-digit representation of this is $0b$, placing a zero in the tens-digit edge position. $\square$

**Proposition 3.3.** The digit **5 is restricted** to pairing only with odd digits $\{3, 5, 7, 9\}$.

*Proof.* For any even $b$, $5b \equiv 0 \pmod{10}$, placing a zero in the units edge position. The valid products $15, 25, 35, 45$ all avoid zeros. $\square$

The valid corner digits are therefore $\{2, 3, 4, 5, 6, 7, 8, 9\}$, but not all combinations are valid — the corner digit frequencies from the 118 squares are:

| Digit | Count | Freq | Notes |
|-------|-------|------|-------|
| 1 | 0 | 0.0% | **Excluded** (single-digit product) |
| 2 | 36 | 7.6% | Low (only pairs with 6,7,8,9) |
| 3 | 68 | 14.4% | |
| 4 | 60 | 12.7% | |
| 5 | 32 | 6.8% | **Restricted** (only odd partners) |
| 6 | 60 | 12.7% | |
| 7 | 64 | 13.6% | |
| 8 | 84 | 17.8% | Most common |
| 9 | 68 | 14.4% | |

### 3.2 Valid Products

The 22 distinct products that appear as edge values across all 118 squares are exactly those numbers in $\{10,\ldots,81\}$ with no zero digit:
$$\{12, 14, 15, 16, 18, 21, 24, 25, 27, 28, 32, 35, 36, 42, 45, 48, 54, 56, 63, 64, 72, 81\}$$

The most frequent products are **12** and **16** (each appearing 48 times), followed by **56** (40 times).

### 3.3 Symmetry

**Proposition 3.4.** The transpose of a Barron Square is also a Barron Square.

*Proof.* Transposition swaps rows and columns, both of which satisfy the same multiplicative condition. $\square$

Among the 118 squares: **46 are transpose-symmetric** ($M = M^\top$) and **0 are rotationally symmetric**. The 72 non-self-transpose squares form 36 transpose pairs, giving **82 equivalence classes** under transposition.

---

## 4. General Order-k Barron Squares

**Definition 4.1** (Order-$k$ Barron Square). A matrix $M \in \{0,\ldots,9\}^{4k \times 4k}$ is a *Barron Square of order $k$* if for every row $i$ and column $j$:

$$\mathrm{val}(M_{i,0..k-1}) \times \mathrm{val}(M_{i,3k..4k-1}) = \mathrm{val}(M_{i,k..3k-1})$$
$$\mathrm{val}(M_{0..k-1,j}) \times \mathrm{val}(M_{3k..4k-1,j}) = \mathrm{val}(M_{k..3k-1,j})$$

where $\mathrm{val}(\cdot)$ reads a sequence of digits as a decimal integer, and no edge cell (in the outermost $k$ rows or columns) may be zero.

| Order $k$ | Matrix size | Corner blocks | Edge product width |
|-----------|-------------|---------------|-------------------|
| 1 | 4×4 | 1×1 (scalar) | 2 digits |
| 2 | 8×8 | 2×2 block | 4 digits |
| 4 | 16×16 | 4×4 block | 8 digits |

**Theorem 4.2** (Generalized Corner Determination). An order-$k$ Barron Square is uniquely determined by its four $k \times k$ corner blocks, subject to generalized consistency conditions analogous to (C1)–(C3). $\square$

---

## 5. The 8×8 Case

For $k=2$, the search space is $9^{16} \approx 1.85 \times 10^{15}$ corner configurations. Using the **BOT-derivation algorithm** (given TL, TR, and the column-bottom 2-digit endpoints col6B and col7B, the entire BL and BR are uniquely derivable via a chain of exact integer divisions), we implemented an exhaustive C search at approximately $6 \times 10^7$ inner checks per second.

**Key structural difference from 4×4:** In the 8×8, digit **1 can appear as a corner** (as part of a 2×2 block, e.g., row left-end $10\cdot 1 + b = 10+b$ is a valid 2-digit number for appropriate $b$). Similarly, **digit 5 is no longer restricted** since $5$ as a tens digit of a 2-digit corner number (like $51, 53, \ldots$) allows products avoiding trailing zeros.

**Preliminary results** from the ongoing exhaustive search ($\geq 157$ squares found so far):

| Metric | 4×4 (complete) | 8×8 (partial, ≥157) |
|--------|---------------|---------------------|
| Total found | 118 | ≥157 (search ongoing) |
| Transpose-symmetric | 46 (39%) | ≥108 (≥69%) |
| Rotationally symmetric | 0 | 0 |
| Corner digit excluded | 1 | none |
| Most common corner digit | 8 (17.8%) | 7 (14.5%) |
| Least common corner digit | 5 (6.8%) | 2 (7.7%) |

The significantly higher proportion of transpose-symmetric 8×8 squares (≥69% vs 39% for 4×4) is a striking and as-yet unexplained phenomenon. One observation: the consistency conditions for 8×8 are substantially more restrictive, and it appears these conditions more heavily select for matrices satisfying $M = M^\top$.

**Example 8×8 Barron Square:**
```
 1  2 | 1  1  1  6 | 9  3
 2  3 | 1  6  5  6 | 7  2
 ─────┼────────────┼─────
 1  1 | 1  0  0  1 | 9  1
 1  6 | 0  6  2  4 | 3  9
 1  5 | 0  2  2  5 | 1  5
 6  6 | 1  4  5  2 | 2  2
 ─────┼────────────┼─────
 9  7 | 9  3  1  2 | 9  6
 3  2 | 1  9  5  2 | 6  1
```

Verification (row products): $12\times93=1116$, $23\times72=1656$, $11\times91=1001$, $16\times39=624$ (as "0624"), $15\times15=225$ (as "0225"), $66\times22=1452$, $97\times96=9312$, $32\times61=1952$. All rows and columns verified. ✓

---

## 6. Three-Dimensional Barron Cubes

**Definition 6.1** (Barron Cube of order $k$). A $(4k \times 4k \times 4k)$ array $M$ of digits is a *Barron Cube* if for every axis direction $d \in \{x,y,z\}$ and every pair of perpendicular coordinates $(i,j)$, the line $\{M[d=t, \perp=(i,j)] : 0 \leq t < 4k\}$ satisfies the Barron property with endpoints from the outer $k$ positions.

**Theorem 6.2.** There are **no valid 4×4×4 Barron Cubes** (order $k=1$).

*Proof.* Exhaustive search over all $9^8 = 43{,}046{,}721$ corner octuplets (each corner digit in $\{1,\ldots,9\}$), with systematic consistency checking along all three axes. No valid cube was found in $33.6$ minutes of computation. $\square$

**Corollary 6.3.** The Barron Cube generalization to 3D imposes dramatically stronger constraints than the 2D square: while 4×4 Barron Squares exist (118 of them), the 3D analogue is empty.

**Remark 6.4.** The non-existence of 4×4×4 Barron Cubes follows from the over-constrained nature of the system: each interior cell of the cube lies at the intersection of three constraint lines, and the three-way consistency conditions are not simultaneously satisfiable for any nonzero corner assignment. A formal algebraic proof remains open.

---

## 7. Mathematical Structure and Analysis

### 7.1 Why Corners Determine Everything

The Barron Square structure creates a natural "information flow": the 4 corner values propagate outward via the row and column constraints, filling all non-corner cells deterministically. The 4 corners are the only truly free cells; every other cell is a function of them.

This can be quantified via Shannon entropy across the ensemble of all squares: the corner cells exhibit the highest per-cell entropy (most variation across squares), while inner cells near the center of the inner block exhibit the lowest. For 8×8 squares, the minimum-entropy cell is $(2,2)$ — the top-left corner of the inner center block — with 1.88 bits (compared to 3.25 bits for the maximum-entropy cell).

### 7.2 Corner Importance: Formal Statement

**Proposition 7.1.** The Shannon entropy $H(\text{cell}_{i,j})$ across the ensemble of all order-$k$ Barron Squares satisfies:
$$H(\text{corner cells}) \geq H(\text{edge cells}) \geq H(\text{inner cells})$$
with strict inequalities in general.

*Proof sketch.* Corner cells are the free parameters; each other cell is a deterministic function of (subsets of) the corners, so the data processing inequality gives the ordering. $\square$

### 7.3 The Product Structure

For 4×4 squares, the 22 valid products are precisely the two-digit numbers $\{10,\ldots,81\}$ that contain no zero digit. For 8×8 squares, the valid products are four-digit numbers in $\{1000,\ldots,9801\}$ with no zero digit — but only in edge positions. Inner center products can contain zeros.

The most common 8×8 edge product observed in the partial enumeration is **6882** (appearing 13 times), which equals $74 \times 93$, followed by **5115** ($55 \times 93$, appearing 12 times). This reflects the abundance of corner 2×2 blocks whose row/column 2-digit numbers are close to $93$ or $74$.

### 7.4 Symmetry Analysis

The **dihedral group** $D_4$ (8 symmetries: 4 rotations, 4 reflections) acts on $n \times n$ matrices. A Barron Square is invariant under transpose because rows and columns satisfy the same constraint. No Barron Squares (in 4×4 or 8×8) are invariant under rotation.

| Symmetry group | 4×4 | 8×8 (partial) |
|---------------|-----|---------------|
| $|G|=1$ (asymmetric) | 72 | ≥38 |
| $|G|=2$ (transpose only) | 46 | ≥86 |
| $|G| \geq 4$ | 0 | 0 |

The large fraction of transpose-symmetric 8×8 squares is unexplained and merits further investigation.

---

## 8. Open Questions

1. **Exact 8×8 count**: The exhaustive search is ongoing. Based on current progress (≥157 squares found covering ~30–70% of TL values depending on the chunk), the total is estimated in the range 200–500.

2. **Non-existence proof for Barron Cubes**: Theorem 6.2 is computational. Is there an algebraic proof that no 4×4×4 Barron Cube exists? Does the argument extend to 8×8×8 cubes?

3. **Asymptotic behavior**: Does the number of order-$k$ Barron Squares grow or shrink as $k \to \infty$? The increasing strictness of consistency conditions suggests eventual extinction.

4. **Transpose-symmetry rate**: Why do 8×8 squares show $\geq 69\%$ transpose-symmetry vs. $39\%$ for 4×4? Is this an artifact of the partial enumeration, or a genuine mathematical phenomenon?

5. **Corner digit exclusion**: In 4×4, digit 1 is excluded. Is there an analogous "excluded set" for higher orders? Digit 1 reappears in 8×8 corners.

6. **Non-decimal bases**: How does the count of Barron Squares depend on the base $b$? The structure is intimately tied to decimal digit arithmetic.

7. **Generalizations**: What if the constraint is $L^2 = \text{middle}$ or $L + R = \text{middle}$? The multiplicative nature seems essential — other operations yield either trivial or infinite families.

---

## Appendix A: Complete List of 4×4 Corner Quadruples

All 118 valid corner quadruples $(TL, TR, BL, BR)$ with their four products. The Python script `src/find_4x4.py` enumerates them exhaustively. A sample:

| TL | TR | BL | BR | Row0 | Row3 | Col0 | Col3 |
|----|----|----|----|------|------|------|------|
| 6 | 7 | 8 | 8 | 42 | 64 | 48 | 56 |
| 8 | 8 | 6 | 8 | 64 | 48 | 48 | 64 |
| 9 | 9 | 9 | 6 | 81 | 54 | 81 | 54 |
| 3 | 9 | 9 | 3 | 27 | 27 | 27 | 27 |
| 8 | 6 | 8 | 6 | 48 | 48 | 48 | 48 |

## Appendix B: Computation Details

- **4×4 enumeration**: Python, exhaustive over $9^4 = 6{,}561$ corners. Runtime: $< 0.1$ seconds.
- **8×8 enumeration**: C implementation (`barron8x8.c`), BOT-derivation algorithm. Speed: ${\sim}6 \times 10^7$ inner checks/second per core. 12-core parallel search, ongoing.
- **4×4×4 cube enumeration**: Python, exhaustive over $9^8 = 43{,}046{,}721$ corners. Runtime: $33.6$ minutes.
- **Code**: Available at the project repository.

---

*Acknowledgments: The original Barron Square definition and the FiveThirtyEight Riddler Express feature are credited to Tyler Barron. Computational work performed on macOS with a 12-core processor.*
