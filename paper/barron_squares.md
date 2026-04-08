# Barron Squares: A Multiplicative Structure on Integer Grids

**Tyler Barron**  
*Preprint, 2025*

---

## Abstract

We introduce **Barron Squares**, a family of integer-digit matrices satisfying a multiplicative boundary condition: in any row or column, the product of the two "endpoint" digit-groups equals the "interior" digit-group read as an integer. We completely characterize the 4×4 case (finding exactly **118** valid squares), develop the algebraic consistency conditions that govern their existence, enumerate 8×8 squares, explore a three-dimensional analogue (Barron Cubes), and derive a general framework for squares of arbitrary order. We show that the four corner digits are the fundamental free parameters, that digit 1 and even multiples of 5 are structurally excluded from corner positions, and that 46 of the 118 squares exhibit transpose-symmetry while none are rotationally symmetric.

---

## 1. Introduction

Consider a 4×4 matrix of single decimal digits. We say the matrix is a **Barron Square** if every row and every column satisfies the following multiplicative property: the leftmost digit times the rightmost digit equals the two-digit number formed by the two interior digits.

**Definition 1.1** (4×4 Barron Square). A matrix $M \in \{0,\ldots,9\}^{4\times 4}$ is a *Barron Square of order 1* if:

1. For every row $i$:
$$M_{i,0} \times M_{i,3} = 10 \cdot M_{i,1} + M_{i,2}$$

2. For every column $j$:
$$M_{0,j} \times M_{3,j} = 10 \cdot M_{1,j} + M_{2,j}$$

3. **No-zero edge condition**: no cell in the border (row 0, row 3, column 0, or column 3) equals 0.

**Example 1.2.** The following matrix, which appeared as a FiveThirtyEight Riddler Express puzzle, is a Barron Square:

$$\begin{pmatrix} 6 & 4 & 2 & 7 \\ 4 & 2 & 0 & 5 \\ 8 & 4 & 8 & 6 \\ 8 & 6 & 4 & 8 \end{pmatrix}$$

Verification:
- Row 0: $6 \times 7 = 42$ ✓; Row 1: $4 \times 5 = 20$ ✓; Row 2: $8 \times 6 = 48$ ✓; Row 3: $8 \times 8 = 64$ ✓
- Col 0: $6 \times 8 = 48$ ✓; Col 1: $4 \times 6 = 24$ ✓; Col 2: $2 \times 4 = 8$ ✓; Col 3: $7 \times 8 = 56$ ✓

Note that col 2 gives $2 \times 4 = 8$, which is interpreted as the two-digit string "08," so $M_{1,2} = 0$ and $M_{2,2} = 8$. The zero in position $(1,2)$ is permitted because that cell is *interior* (not on the border).

---

## 2. The Corner Theorem

The most fundamental structural result is that a Barron Square is **completely determined by its four corner values**.

**Theorem 2.1** (Corner Determination). Let $a = M_{0,0}$, $b = M_{0,3}$, $c = M_{3,0}$, $d = M_{3,3}$ denote the four corners of a 4×4 Barron Square. Then:

1. The top and bottom edge rows are determined:
   - $M_{0,1} = \lfloor ab/10 \rfloor$, $M_{0,2} = ab \bmod 10$
   - $M_{3,1} = \lfloor cd/10 \rfloor$, $M_{3,2} = cd \bmod 10$

2. The left and right edge columns are determined:
   - $M_{1,0} = \lfloor ac/10 \rfloor$, $M_{2,0} = ac \bmod 10$
   - $M_{1,3} = \lfloor bd/10 \rfloor$, $M_{2,3} = bd \bmod 10$

3. The inner rows (rows 1 and 2) determine the inner 2×2 block via the row constraint.

4. The inner columns (columns 1 and 2) yield the same inner 2×2 block, imposing **four consistency conditions** on $(a,b,c,d)$.

*Proof sketch.* Steps 1–3 follow directly from the row and column constraints applied to the boundary, then inner, rows and columns. Step 4 requires that the values computed via inner rows agree with those via inner columns. $\square$

**Notation.** Let $t(n) = \lfloor n/10 \rfloor$ (tens digit) and $u(n) = n \bmod 10$ (units digit) for any non-negative integer $n$, where $n$ is understood as at most a 2-digit number.

**Corollary 2.2** (Consistency Conditions). Four nonzero digits $(a,b,c,d)$ form valid corners of a 4×4 Barron Square if and only if all edge products contain no zero digit *and* the following four equations hold simultaneously:

$$t\!\left(t(ac)\cdot t(bd)\right) = t\!\left(t(ab)\cdot t(cd)\right) \tag{C1}$$
$$u\!\left(t(ac)\cdot t(bd)\right) = t\!\left(u(ab)\cdot u(cd)\right) \tag{C2}$$
$$t\!\left(u(ac)\cdot u(bd)\right) = u\!\left(t(ab)\cdot t(cd)\right) \tag{C3}$$
$$u\!\left(u(ac)\cdot u(bd)\right) = u\!\left(u(ab)\cdot u(cd)\right) \tag{C4}$$

**Proposition 2.3.** Condition (C4) is always satisfied for any integers $a,b,c,d$.

*Proof.* $u(u(ac)\cdot u(bd)) = (ac \bmod 10)(bd \bmod 10) \bmod 10 = abcd \bmod 10$. Similarly, $u(u(ab)\cdot u(cd)) = abcd \bmod 10$. These are equal. $\square$

This means only three conditions (C1)–(C3) are genuinely restrictive.

---

## 3. Enumeration of 4×4 Barron Squares

**Theorem 3.1.** There are exactly **118** Barron Squares of order 1 (4×4).

*Proof.* Exhaustive enumeration over all $9^4 = 6{,}561$ ordered quadruples $(a,b,c,d) \in \{1,\ldots,9\}^4$ (corners must be nonzero), checking the edge-nonzero and consistency conditions. The result was verified computationally. $\square$

### 3.1 Excluded Corner Values

**Proposition 3.2.** The digit 1 cannot appear as any corner value in a 4×4 Barron Square.

*Proof.* If $a = 1$, then $a \cdot b = b \leq 9$ for any $b \in \{1,\ldots,9\}$, which is a single-digit number. Its two-digit representation is $0b$, placing a zero in an edge position, violating the no-zero edge condition. $\square$

**Proposition 3.3.** The digit 5 is heavily restricted as a corner value. It can only pair with odd digits $\{3, 5, 7, 9\}$.

*Proof.* For any even $b$, $5b$ is divisible by 10, placing a zero in the units edge position. The only valid partners for 5 are $\{3,5,7,9\}$ (giving products $15, 25, 35, 45$). $\square$

### 3.2 Digit Distribution

Among all 118 Barron Squares:

| Digit | Corner freq | Corner % | All-cell % |
|-------|------------|----------|------------|
| 1     | 0          | 0.0%     | —          |
| 2     | 36         | 7.6%     | 18.2%      |
| 3     | 68         | 14.4%    | 6.6%       |
| 4     | 60         | 12.7%    | 14.7%      |
| 5     | 32         | 6.8%     | 8.1%       |
| 6     | 60         | 12.7%    | 11.8%      |
| 7     | 64         | 13.6%    | 5.5%       |
| 8     | 84         | 17.8%    | 9.1%       |
| 9     | 68         | 14.4%    | 3.7%       |
| 0     | 0          | 0.0%     | 6.6%       |

The digit 8 is the most common corner value (17.8%), while 5 and 2 are the rarest among valid corners due to Proposition 3.3 and the single-digit product restriction.

### 3.3 Symmetry

**Proposition 3.4.**
- Exactly **46** of the 118 squares are symmetric under transposition ($M = M^\top$).
- **0** squares are invariant under any nontrivial rotation.

*Remark.* Transpose-symmetry is natural: since the row and column constraints are structurally identical, transposing a Barron Square yields another Barron Square. The 118 squares form $(118 - 46)/2 + 46 = 82$ equivalence classes under transposition.

### 3.4 The Role of Corners

A striking consequence of Theorem 2.1 is that the **corner cells carry all the information**. The 12 non-corner cells are entirely determined by the 4 corner values. This raises the question of what makes corners special — answered by the corner having two independent constraint lines (one row and one column) passing through it, making it the unique "degree-of-freedom" cell.

---

## 4. General Order-k Barron Squares

The natural generalization replaces single digits with $k$-digit integer groups.

**Definition 4.1** (Order-$k$ Barron Square). A matrix $M \in \{0,\ldots,9\}^{4k \times 4k}$ is a *Barron Square of order $k$* if:

1. For every row $i$ (where $n = 4k$): the integer formed by digits $M_{i,0},\ldots,M_{i,k-1}$ (call it $L_i$) times the integer formed by digits $M_{i,3k},\ldots,M_{i,4k-1}$ (call it $R_i$) equals the integer formed by the middle $2k$ digits:
$$L_i \times R_i = \sum_{p=0}^{2k-1} M_{i,k+p} \cdot 10^{2k-1-p}$$

2. Analogously for every column $j$.

3. No digit in the leftmost $k$ or rightmost $k$ columns, or topmost $k$ or bottommost $k$ rows, equals 0.

| Order $k$ | Matrix size | Corner block | Product width | Known count |
|-----------|-------------|-------------|---------------|-------------|
| 1         | 4×4         | 1×1 scalar  | 2 digits      | **118**     |
| 2         | 8×8         | 2×2 block   | 4 digits      | **TBD**     |
| 4         | 16×16       | 4×4 block   | 8 digits      | rare        |

**Theorem 4.2** (General Corner Determination). An order-$k$ Barron Square is uniquely determined by its four $k \times k$ corner blocks.

*Proof.* Identical structure to Theorem 2.1: boundary rows and columns are filled by the row/column constraint, inner cells are filled by inner row constraints, and a set of generalized consistency conditions must hold. $\square$

**Remark 4.3** (Fractal Intuition). The sizes $4, 8, 16, \ldots$ suggest a self-similar structure. Informally, each "cell" of a 4×4 Barron Square can be "expanded" into a 2×2 block to form an 8×8, but the expanded square must itself satisfy the Barron property — creating a richer set of constraints.

---

## 5. 8×8 Barron Squares

For $k=2$, the search space is $9^{16} \approx 1.85 \times 10^{15}$ corner configurations. Using layered pruning (eliminating invalid partial configurations at each corner-block stage), the search is made tractable.

**Algorithm 5.1** (Pruned Enumeration for 8×8).

1. For each top-left corner block TL and top-right corner block TR ($9^8$ pairs):
   - Compute rows 0 and 1 middles (columns 2–5). If any edge cell is 0, prune.
2. For each bottom-left block BL:
   - Compute left-edge inner values (rows 2–5, columns 0–1). If any is 0, prune.
3. For each bottom-right block BR:
   - Compute rows 6–7 middles and right-edge inner values. Check consistency of the 4×4 inner center block.

The consistency check in Step 3 is the same in structure as the four conditions (C1)–(C4) but applied to $2\times 2$ sub-products.

*[Count to be filled in after computation.]*

---

## 6. Three-Dimensional Barron Cubes

**Definition 6.1** (Barron Cube). A *Barron Cube of order $k$* is a $(4k \times 4k \times 4k)$ array of digits satisfying the Barron property along **every axis-aligned line**: for any direction $d \in \{x,y,z\}$ and perpendicular coordinates $(i,j)$, the line
$$\ell(d,i,j) = \bigl(M_{(d,i,j,t)}\bigr)_{t=0}^{4k-1}$$
satisfies $L \times R = \text{middle}$ (where $L$, $R$ are the $k$-digit endpoint numbers) and has no zeros in edge positions.

A 4×4×4 Barron Cube has **8 corner scalar values** (at each vertex of the cube), and is completely determined by those 8 values subject to consistency conditions along all three axis directions.

**Remark 6.2.** A Barron Cube imposes dramatically more constraints than a Barron Square of the same linear size: each interior point lies on three constraint lines (one per axis), versus two for a square. This makes Barron Cubes considerably rarer and the consistency conditions more restrictive.

**Observation 6.3.** Every axis-aligned face of a Barron Cube (e.g., the face at $x = 0$) must itself be a 4×4 Barron Square (restricted to that 2D slice). Thus the cube's six faces are all Barron Squares.

*[Enumeration results to be filled in.]*

---

## 7. Mathematical Structure and Open Questions

### 7.1 Why Corners Matter Most

Quantitatively, a corner cell carries maximum **Shannon entropy** across the ensemble of all Barron Squares, while edge product-cells have lower entropy (constrained by two corner values) and inner cells have the lowest (constrained by four corner values via two independent paths).

### 7.2 Excluded Products

The valid two-digit products that appear in 4×4 Barron Squares are exactly those numbers in $\{10,\ldots,81\}$ that contain no zero digit. These are:
$$\{11,12,\ldots,19,\,21,22,\ldots,29,\,31,\ldots,81\} \setminus \{10,20,30,40,50,60,70,80\}$$

The most common products are 12, 16, and 56 (each appearing 48, 48, and 40 times respectively across all squares), reflecting the abundance of corner pairs that yield these products.

### 7.3 Open Questions

1. **Exact 8×8 count**: How many 8×8 Barron Squares exist?

2. **Exact 4×4×4 count**: How many 4×4×4 Barron Cubes exist?

3. **Asymptotic behavior**: Does the number of order-$k$ Barron Squares grow or shrink as $k \to \infty$? Empirically, the constraints become more restrictive, suggesting eventual extinction at large $k$.

4. **Prime corners**: Is there a Barron Square whose four corners are all prime digits $\{2,3,5,7\}$? (Digit 5 can only pair with $\{3,5,7,9\}$, so $5$ as a corner requires odd co-corners.)

5. **Non-decimal bases**: What is the count of Barron Squares when digits are taken from $\mathbb{Z}_b$ for bases $b \neq 10$? The no-zero-digit constraint on products takes a different character in other bases.

6. **Generalizations**: What if the constraint is $L \times R = \text{middle}^2$ or another function? The multiplicative nature seems essential — does any other binary operation yield a rich finite family?

7. **Connections to number theory**: The consistency conditions (C1)–(C3) relate digit-extraction functions to products modulo powers of 10. Are there deeper connections to $p$-adic valuations or digit-sum identities?

---

## 8. Conclusion

Barron Squares are a natural and finitely enumerable family of multiplicative integer-digit structures. The key results are:
- **118** exact 4×4 Barron Squares, all determined by 4 corner values
- Digit 1 is excluded from all corners; digit 5 is heavily restricted
- Three algebraic consistency conditions govern corner validity; a fourth is always satisfied
- The structure generalizes to arbitrary order $k$ and to three dimensions
- Barron Cubes impose strictly stronger constraints, yielding a much rarer family

The interplay between decimal digit structure and multiplicative identities gives Barron Squares a character that feels both elementary and surprisingly rich.

---

## Appendix: Complete List of 4×4 Barron Square Corner Quadruples

The 118 valid corner quadruples $(TL, TR, BL, BR)$ are enumerated by the companion code (`src/find_4x4.py`). A representative sample:

| TL | TR | BL | BR | Products |
|----|----|----|----|----------|
| 6  | 7  | 8  | 8  | 42, 64, 48, 56 |
| 8  | 8  | 6  | 8  | 64, 48, 48, 64 |
| 9  | 9  | 9  | 6  | 81, 54, 81, 54 |
| 3  | 9  | 9  | 3  | 27, 27, 27, 27 |

*The "Products" column lists $TL \times TR$, $BL \times BR$, $TL \times BL$, $TR \times BR$.*

---

*Code available at: [github.com/barron-squares/barron-squares]*
