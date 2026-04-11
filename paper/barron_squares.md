# Barron Squares: A Multiplicative Structure on Integer Grids

**Tyler Barron**

*Independent Researcher*

*April 11, 2026*

---

## Abstract

We introduce **Barron Squares**, a family of integer-digit matrices satisfying a multiplicative boundary condition: in any row or column, the product of the two *endpoint* digit-groups equals the *interior* digit-group read as a decimal integer. A small example (read the first row as $6 \times 7 = 42$, the first column as $6 \times 8 = 48$, and so on):

````{=typst}
#align(center)[
```
6 │ 4 2 │ 7
──┼─────┼──
4 │ 2 0 │ 5
8 │ 4 8 │ 6
──┼─────┼──
8 │ 6 4 │ 8
```
]
````

We completely characterize the $4 \times 4$ case, finding exactly **118** valid squares by exhaustive enumeration, and develop the algebraic consistency conditions that govern their existence. For the $8 \times 8$ case we report an exhaustive parallel search over all $9^4 = 6{,}561$ top-left corner blocks that yields **1,248** valid squares. We show computationally that **no valid $4 \times 4 \times 4$ Barron Cube exists**, verified over the full space of $9^8 = 43{,}046{,}721$ corner octuplets. The central structural result is that a Barron Square is determined entirely by its four corner blocks, reducing existence to a small system of digit-level algebraic conditions. As a second structural theorem we prove that the inner $4 \times 4$ center of every $8 \times 8$ Barron Square is symmetric — a consequence of an *endpoint pairing* property that holds without exception in the enumerated data — and we document a sharp qualitative shift between the two orders: digit 1 is forbidden as a corner at order 1 but permitted at order 2, the corner-digit distribution becomes markedly more uniform, and the self-transpose rate rises from $39\%$ to exactly $50\%$.

**Keywords.** Barron Square, digit matrix, multiplicative constraint, exhaustive enumeration, consistency conditions, recreational mathematics.

**MSC 2020.** 05A15 (Exact enumeration problems), 11A63 (Radix representation; digital problems), 05B15 (Orthogonal arrays, Latin squares, Room squares).

---

## 1. Introduction

### 1.1 Motivation

A single-row version of the problem first appeared as a *FiveThirtyEight Riddler Express* puzzle: find a $4 \times 4$ grid of decimal digits such that every row and every column encodes a valid two-digit multiplication, with the leftmost digit times the rightmost digit equal to the two-digit number formed by the interior pair. The object is elementary to state and yet non-trivial to search: the full space of $9^4 = 6{,}561$ unconstrained corner assignments collapses, after consistency enforcement, to exactly $118$ valid boards. Small, finite answers of this kind are a classical target of *recreational number theory*, joining families such as magic squares, cross-figures, and multiplicative alphametics. What distinguishes the present object is that the constraints are simultaneously *positional* (they depend on decimal place value) and *structural* (they couple boundaries to interiors), placing it in a hybrid regime between digit puzzles and constraint satisfaction on integer grids.

This paper formalizes the puzzle, generalizes it to a family of order-$k$ objects of size $4k \times 4k$, and studies its structure by a combination of exhaustive enumeration and algebraic reduction.

### 1.2 Definition

Write $\mathrm{val}(s)$ for the decimal-integer value of a digit sequence $s$, so that $\mathrm{val}(d_1 d_2 \cdots d_n) = \sum_{i=1}^{n} d_i\,10^{n-i}$. For a $4k$-length sequence $s$ we say $s$ has a *left endpoint* (the first $k$ digits), a *right endpoint* (the last $k$ digits), and an *interior* (the middle $2k$ digits).

**Definition 1.1** (Order-$k$ Barron Square). A matrix $M \in \{0,\ldots,9\}^{4k \times 4k}$ is a *Barron Square of order $k$* if:

1. *(Row condition.)* For every row index $i$, with $L_i, R_i$ the left and right endpoints of row $i$ and $I_i$ its interior,
   $$\mathrm{val}(L_i) \cdot \mathrm{val}(R_i) \;=\; \mathrm{val}(I_i).$$
2. *(Column condition.)* For every column index $j$, with $T_j, B_j$ the top and bottom endpoints of column $j$ and $J_j$ its interior,
   $$\mathrm{val}(T_j) \cdot \mathrm{val}(B_j) \;=\; \mathrm{val}(J_j).$$
3. *(Edge condition.)* No entry in the outermost $k$ rows or $k$ columns of $M$ is zero.

For order $k = 1$ the row and column conditions specialize to the elementary scalar forms
$$M_{i,0} \cdot M_{i,3} \;=\; 10\,M_{i,1} + M_{i,2}, \qquad M_{0,j} \cdot M_{3,j} \;=\; 10\,M_{1,j} + M_{2,j}.$$

| Order $k$ | Matrix size | Corner block | Edge product width |
|-----------|-------------|--------------|-------------------|
| 1 | $4 \times 4$ | $1 \times 1$ (scalar) | 2 digits |
| 2 | $8 \times 8$ | $2 \times 2$ block | 4 digits |
| 4 | $16 \times 16$ | $4 \times 4$ block | 8 digits |

**Example 1.2.** The matrix below is a Barron Square of order 1. Horizontal and vertical separators mark the boundary between the endpoint blocks (each of width $k=1$) and the interior:

````{=typst}
#align(center)[
```
6 │ 4 2 │ 7
──┼─────┼──
4 │ 2 0 │ 5
8 │ 4 8 │ 6
──┼─────┼──
8 │ 6 4 │ 8
```
]
````

Verification: the rows give $6 \times 7 = 42$, $4 \times 5 = 20$, $8 \times 6 = 48$, and $8 \times 8 = 64$; the columns give $6 \times 8 = 48$, $4 \times 6 = 24$, $2 \times 4 = 08$, and $7 \times 8 = 56$. The inner zero in row 1 is permitted because it lies on a non-edge cell.

### 1.3 Contributions

Our results cover three aspects of Barron Squares — structure, enumeration, and higher-dimensional extension:

1. **Structural reduction.** We prove that an order-$k$ Barron Square is completely determined by its four $k \times k$ corner blocks (Theorems 2.1 and 2.4). For the order-1 case this reduction is sharp: it yields three genuinely restrictive algebraic consistency conditions on the corners $(a,b,c,d)$, with a fourth candidate condition shown to be automatic (Proposition 2.3).
2. **Complete enumeration at order 1.** We prove by exhaustive search that there are exactly $118$ Barron Squares of order 1 (Theorem 3.1), classify them by corner-digit frequency and transpose symmetry, identify the exclusion of digit $1$ and the parity restriction of digit $5$ as structural consequences of the constraint, and isolate a family of six *uniform-product* squares whose four edge products coincide.
3. **Exhaustive enumeration and structure at order 2.** Using a *BOT-derivation* algorithm that reduces the effective search space from $9^{16}$ to a tractable range, we enumerate $1{,}248$ Barron Squares of order 2 by exhaustive parallel search over all $9^4 = 6{,}561$ top-left corner blocks. On this data we prove (computationally, verified without exception) two new structural results: an *endpoint pairing* dichotomy for inner rows and columns (Theorem 4.1), and, as a consequence, the *inner center symmetry* of every order-2 Barron Square (Theorem 4.2).
4. **Higher-order and higher-dimensional behavior.** We show that no $4 \times 4 \times 4$ Barron Cube exists, by exhaustive search over all $9^8 = 43{,}046{,}721$ corner octuplets (Theorem 5.2), and give a heuristic probabilistic explanation for this non-existence. We further document that $500{,}000$ random trials at order 4 ($16 \times 16$) produce no valid squares, suggesting extreme sparsity or extinction at higher orders.

### 1.4 Paper outline

Section 2 establishes the notation and the corner-determination theorem that underlies all later sections. Section 3 presents the complete enumeration of order-1 ($4 \times 4$) Barron Squares, including corner-digit exclusions, the valid-product spectrum, and the uniform-product family. Section 4 treats the order-2 ($8 \times 8$) case: we describe the BOT-derivation algorithm used for the exhaustive search, report numerical results for all $1{,}248$ squares, and prove the endpoint-pairing and inner-center-symmetry theorems. Section 5 extends the construction to three dimensions and establishes the non-existence of $4 \times 4 \times 4$ Barron Cubes. Section 6 collects a cross-order comparison, open questions, and concluding remarks. Code and search outputs are described in Appendix B.

---

## 2. Preliminaries

This section collects the definitions, notation, and single structural theorem (the *Corner Determination Theorem*) that is used throughout the rest of the paper. The central observation is that a Barron Square is *completely determined* by its four corner entries — or, at order $k$, its four $k \times k$ corner blocks — so that every other cell is forced by the row and column constraints. Existence of a Barron Square with prescribed corners thus reduces to the question of whether the forced cell values are internally consistent.

**Notation.** For a non-negative integer $n < 100$ write $t(n) = \lfloor n/10 \rfloor$ (the tens digit) and $u(n) = n \bmod 10$ (the units digit), so that $n = 10\,t(n) + u(n)$. For a $k$-digit sequence $s$, write $\mathrm{val}(s)$ for its integer value.

### 2.1 The order-1 case

**Theorem 2.1** (Corner Determination, order 1). *Let $M$ be a $4 \times 4$ Barron Square with corner entries $a = M_{0,0}$, $b = M_{0,3}$, $c = M_{3,0}$, and $d = M_{3,3}$. Then every entry of $M$ is uniquely determined by $(a,b,c,d)$, and is given explicitly by:*
$$\begin{array}{ll}
M_{0,1} = t(ab), & M_{0,2} = u(ab), \\
M_{3,1} = t(cd), & M_{3,2} = u(cd), \\
M_{1,0} = t(ac), & M_{2,0} = u(ac), \\
M_{1,3} = t(bd), & M_{2,3} = u(bd).
\end{array}$$
*The four inner cells are then forced by both the inner rows and the inner columns:*
$$\begin{array}{ll}
M_{1,1} = t\!\left(M_{1,0}\,M_{1,3}\right) = t\!\left(M_{0,1}\,M_{3,1}\right), & M_{1,2} = u\!\left(M_{1,0}\,M_{1,3}\right) = t\!\left(M_{0,2}\,M_{3,2}\right), \\[0.25em]
M_{2,1} = t\!\left(M_{2,0}\,M_{2,3}\right) = u\!\left(M_{0,1}\,M_{3,1}\right), & M_{2,2} = u\!\left(M_{2,0}\,M_{2,3}\right) = u\!\left(M_{0,2}\,M_{3,2}\right).
\end{array}$$

*Proof.* Apply row 0's Barron condition: $ab = \mathrm{val}(M_{0,0})\cdot\mathrm{val}(M_{0,3})$ must equal the two-digit number $10\,M_{0,1} + M_{0,2}$, so $M_{0,1} = t(ab)$ and $M_{0,2} = u(ab)$. The same argument applied to row 3 and to columns 0 and 3 gives the eight edge cells displayed in the first block.

With all eight edge cells fixed, the four inner cells are determined by the inner rows and columns. Row 1 has endpoints $M_{1,0} = t(ac)$ and $M_{1,3} = t(bd)$, so its Barron condition requires
$$10\,M_{1,1} + M_{1,2} \;=\; t(ac)\cdot t(bd),$$
giving $M_{1,1} = t(t(ac)\,t(bd))$ and $M_{1,2} = u(t(ac)\,t(bd))$. Row 2 and the two inner columns yield the analogous expressions. $\square$

### 2.2 Consistency conditions

The forcing in Theorem 2.1 pins each inner cell *twice* — once by its row and once by its column — so $M$ is a genuine Barron Square only when the two determinations agree.

**Corollary 2.2** (Algebraic consistency conditions for order 1). *A quadruple of non-zero digits $(a,b,c,d)$ extends to a $4 \times 4$ Barron Square if and only if all four edge products $ab, cd, ac, bd$ have non-zero tens and units digits and the following three identities hold:*
$$t\!\left(t(ac)\cdot t(bd)\right) \;=\; t\!\left(t(ab)\cdot t(cd)\right) \tag{C1}$$
$$u\!\left(t(ac)\cdot t(bd)\right) \;=\; t\!\left(u(ab)\cdot u(cd)\right) \tag{C2}$$
$$t\!\left(u(ac)\cdot u(bd)\right) \;=\; u\!\left(t(ab)\cdot t(cd)\right) \tag{C3}$$

*Proof.* Each equation equates the row-determination and column-determination of one of the four inner cells: (C1) corresponds to $M_{1,1}$, (C2) to $M_{1,2}$, and (C3) to $M_{2,1}$. The no-zero-edge condition is exactly the requirement that each of $ab, cd, ac, bd$ be a two-digit number with no zero digit. $\square$

**Proposition 2.3** (Automatic fourth condition). *The candidate consistency equation for $M_{2,2}$, namely*
$$u\!\left(u(ac)\cdot u(bd)\right) \;=\; u\!\left(u(ab)\cdot u(cd)\right), \tag{C4}$$
*is satisfied for every choice of digits $(a,b,c,d)$.*

*Proof.* For any integers $x,y$, $u(x)\,u(y) \equiv x\,y \pmod{10}$, so $u(u(x)\,u(y)) = u(xy)$. Applying this twice,
$$u(u(ac)\,u(bd)) \;=\; u((ac)(bd)) \;=\; u(abcd) \;=\; u((ab)(cd)) \;=\; u(u(ab)\,u(cd)). \qquad \square$$

Only three of the four inner cells thus impose genuine restrictions on $(a,b,c,d)$.

### 2.3 The general-order case

**Theorem 2.4** (Corner Determination, general order). *Let $M$ be an order-$k$ Barron Square with $k \times k$ corner blocks $A = M_{[0,k),[0,k)}$, $B = M_{[0,k),[3k,4k)}$, $C = M_{[3k,4k),[0,k)}$, and $D = M_{[3k,4k),[3k,4k)}$. Every entry of $M$ is uniquely determined by $(A,B,C,D)$, as follows:*

- *The $2k$-digit interior of row $0$ is $\mathrm{val}(A)\cdot\mathrm{val}(B)$, laid out in the $k$ cells to the right of $A$ and the $k$ cells to the left of $B$; rows $1,\ldots,k-1$ and rows $3k,\ldots,4k-1$ are determined analogously.*
- *The $2k$-digit interior of column $0$ is $\mathrm{val}(A)\cdot\mathrm{val}(C)$, and columns $1,\ldots,k-1$ and columns $3k,\ldots,4k-1$ are determined analogously.*
- *Each of the $4k^2$ inner cells lies at the intersection of an inner row and an inner column whose endpoints are all fixed by the preceding steps, and is therefore forced by either the row or the column constraint.*

*The square exists iff all row- and column-determinations of each inner cell agree and no edge cell is zero.*

*Proof sketch.* The endpoint blocks of every edge row and edge column are sub-blocks of the corners, so each such row or column has both endpoints fixed and its interior is determined by the Barron constraint. Iterating, every inner row has both endpoints determined (they are columns of edge-row interiors) and similarly for inner columns, so every inner cell is doubly determined. Existence is exactly the consistency of these $k \times 2k$ inner cells' row- and column-determinations, together with the non-zero-edge requirement. $\square$

In the order-1 case this reduces to the three conditions (C1)–(C3). For $k \geq 2$ the analogous system has many more conditions and is not practical to write down explicitly; in Section 4 we instead exploit it algorithmically via the BOT-derivation search.

---

## 3. The order-1 case: $4 \times 4$ Barron Squares

At order $k = 1$ the corner space $\{1,\ldots,9\}^4$ has only $9^4 = 6{,}561$ elements, so the existence question is settled by direct enumeration. This section reports the complete count, identifies the two structural digit exclusions that shape the enumeration, lists the 22 products that appear as edge values, and isolates the six *uniform-product* squares in which all four edges carry the same product.

**Theorem 3.1.** *There are exactly $118$ Barron Squares of order 1.*

*Proof.* Exhaustive enumeration over all $9^4 = 6{,}561$ nonzero corner quadruples $(a, b, c, d)$, checking the algebraic consistency conditions (C1)–(C3) of Corollary 2.2 at each. The Python script `src/find_4x4.py` performs this enumeration in $< 0.1$ seconds. $\square$

### 3.1 Excluded corner values

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

### 3.2 Valid products

The 22 distinct products that appear as edge values across all 118 squares are exactly those numbers in $\{10,\ldots,81\}$ with no zero digit:
$$\{12, 14, 15, 16, 18, 21, 24, 25, 27, 28, 32, 35, 36, 42, 45, 48, 54, 56, 63, 64, 72, 81\}$$

The most frequent products are **12** and **16** (each appearing 48 times), followed by **56** (40 times).

### 3.3 Symmetry and transposition

**Proposition 3.4.** The transpose of a Barron Square is also a Barron Square.

*Proof.* Transposition swaps rows and columns, both of which satisfy the same multiplicative condition. $\square$

Among the 118 squares: **46 are transpose-symmetric** ($M = M^\top$) and **0 are rotationally symmetric**. The 72 non-self-transpose squares form 36 transpose pairs, giving **82 equivalence classes** under transposition.

### 3.4 Uniform-product squares

Six of the 118 squares have the remarkable property that **all four edge products are equal**:

| TL | TR | BL | BR | Product |
|----|----|----|-----|---------|
| 2 | 7 | 7 | 2 | 14 |
| 7 | 2 | 2 | 7 | 14 |
| 3 | 9 | 9 | 3 | 27 |
| 9 | 3 | 3 | 9 | 27 |
| 6 | 8 | 8 | 6 | 48 |
| 8 | 6 | 6 | 8 | 48 |

These form three transpose pairs. Note that in each pair, $ab = cd = ac = bd$, which forces $(a,b,c,d) = (a,b,b,a)$ — the corners must be anti-diagonal symmetric. The three eligible products are $\{14, 27, 48\}$.

---

## 4. The order-2 case: $8 \times 8$ Barron Squares

At order $k = 2$ the unconstrained corner space has size $9^{16} \approx 1.85 \times 10^{15}$, which is well beyond the reach of brute-force enumeration. We reduce the search to a tractable range via a *BOT-derivation algorithm* (§4.1), carry out an exhaustive parallel enumeration in C (§4.2), and observe two new structural phenomena — an *endpoint pairing* dichotomy for the inner rows and columns, and, as its immediate consequence, the symmetry of the inner $4 \times 4$ center block (§4.3). Section 4.4 exhibits a representative $8 \times 8$ square.

### 4.1 The BOT-derivation algorithm

The key observation is that once the two top corners $\mathrm{TL} = M_{[0,2),[0,2)}$ and $\mathrm{TR} = M_{[0,2),[6,8)}$ are fixed, the top two rows of $M$ are determined (via Theorem 2.4 applied row-wise), which in particular fixes the two-digit *top endpoints* of every column. If one additionally specifies the two-digit bottom endpoints of the two rightmost inner columns — that is, the entries $M_{[6,8),4}$ and $M_{[6,8),5}$, which we denote $\mathrm{col}_4^{\mathrm{B}}$ and $\mathrm{col}_5^{\mathrm{B}}$ — then the column Barron condition forces the four-digit interiors of inner columns 4 and 5, and with them the remaining entries of columns 4 and 5.

Once columns 4 and 5 are complete, each of the eight rows has its right endpoint pair fixed. Together with the left endpoint pair — which comes from $\mathrm{TL}$ for rows 0–1 and from the column-derived entries for rows 2–7 — the Barron row conditions produce the remaining interior entries by exact integer division. In particular, the bottom corners $\mathrm{BL}$ and $\mathrm{BR}$ are *derived* rather than searched. The overall effect is to reduce the search from $9^{16}$ to $9^4 \cdot 9^4 \cdot 9^4 = 9^{12}$ nominal configurations; in practice the effective branching is far smaller still, because each column derivation must return valid single-digit values at every step and fails otherwise.

The implementation in `src/barron8x8.c` achieves approximately $6 \times 10^7$ inner checks per second per core and is parallelized across $12$ disjoint TL ranges covering the full $9^4 = 6{,}561$-element TL space.

### 4.2 Numerical results

The exhaustive parallel search described in §4.1 covers all $9^4 = 6{,}561$ values of TL across $12$ disjoint workers and yields exactly $1{,}248$ distinct Barron Squares of order 2. Total wall-clock time was approximately $50$ hours on a 12-core processor. In what follows we treat $1{,}248$ as the order-2 count, pending an independent verification.

| Metric | $4 \times 4$ | $8 \times 8$ |
|---|---|---|
| Total squares | $118$ | $1{,}248$ |
| Transpose-symmetric | $46$ ($39\%$) | $624$ ($50.0\%$) |
| Rotationally symmetric | $0$ | $0$ |
| Excluded corner digits | $\{1\}$ | $\varnothing$ |
| Most frequent corner digit | $8$ ($17.8\%$) | $7$ ($13.5\%$) |
| Least frequent corner digit | $5$ ($6.8\%$) | $1$ ($8.1\%$) |

Two qualitative changes stand out. First, the structural digit exclusions of order 1 both disappear at order 2. Digit $1$ is forbidden as a $4 \times 4$ corner because $1 \cdot b = b$ is a single digit, but as the tens digit of a 2-digit $8 \times 8$ corner block (values $10,\ldots,19$) it produces genuine two-digit factors and so appears with frequency $8.1\%$. Digit $5$ is only restricted at order 1 because $5 \cdot (\text{even}) \equiv 0 \pmod{10}$; as the tens digit of a 2-digit corner block it has partners $51, 52, \ldots$ that evade this constraint, and its order-2 frequency rises to $8.8\%$. Second, the corner-digit distribution becomes markedly more uniform: at order 1 it ranges over $0\%$–$17.8\%$, whereas at order 2 all nine digits occur with frequencies confined to the interval $[8.1\%, 13.5\%]$.

The transpose-symmetry rate, which rose erratically through the early stages of the search — from $69\%$ at $n = 157$ to $54\%$ at $n = 644$ to $49.7\%$ at $n = 1{,}232$ — settles at exactly $50.0\%$ at the full count $n = 1{,}248$. This is substantially higher than the order-1 rate of $39\%$, a phenomenon we address in §4.3.

### 4.3 Endpoint pairing and inner center symmetry

Label the inner column and row indices as $[2,6) = \{2,3,4,5\}$ and, for a short inner index $r \in \{0,1,2,3\}$, define the four *inner-band two-digit endpoints*
$$\begin{aligned}
L(r) &= 10\,M_{2+r,0} + M_{2+r,1}, & R(r) &= 10\,M_{2+r,6} + M_{2+r,7}, \\
T(r) &= 10\,M_{0,2+r} + M_{1,2+r}, & B(r) &= 10\,M_{6,2+r} + M_{7,2+r}.
\end{aligned}$$
Here $L(r)$ and $R(r)$ are the left and right endpoints of inner row $2+r$, while $T(r)$ and $B(r)$ are the top and bottom endpoints of inner column $2+r$. Each determines a four-digit interior via the Barron condition: $L(r)\cdot R(r)$ for the row and $T(r)\cdot B(r)$ for the column. These two interiors jointly fill the inner $4 \times 4$ center block $\mathrm{IC} = M_{[2,6),[2,6)}$.

**Theorem 4.1** (Endpoint Pairing). *For every $8 \times 8$ Barron Square and every inner index $r \in \{0,1,2,3\}$, exactly one of the following cases holds:*

- *(Case A)* $L(r) = T(r)$ *and* $R(r) = B(r)$;
- *(Case B)* $L(r) = B(r)$ *and* $R(r) = T(r)$.

*In either case $L(r)\,R(r) = T(r)\,B(r)$.*

*Computational verification.* Across all $1{,}248$ order-2 Barron Squares and all $4 \times 1{,}248 = 4{,}992$ (square, inner index) pairs, Case A occurs $2{,}598$ times, Case B occurs $2{,}394$ times, and the dichotomy never fails. In self-transpose squares Case A is forced by $M_{i,j} = M_{j,i}$, which gives $M_{2+r,0} = M_{0,2+r}$ and $M_{2+r,1} = M_{1,2+r}$ and hence $L(r) = T(r)$ and $R(r) = B(r)$; a purely algebraic proof for asymmetric squares remains open. $\square$

**Theorem 4.2** (Inner Center Symmetry). *For every $8 \times 8$ Barron Square the inner center block $\mathrm{IC}$ is a symmetric $4 \times 4$ matrix: $\mathrm{IC}_{r,c} = \mathrm{IC}_{c,r}$ for all $r, c \in \{0,1,2,3\}$.*

*Proof.* By Theorem 4.1 each inner row $r$ and its matching inner column $r$ have endpoints whose (unordered) pair coincides, so their Barron-forced four-digit interiors are equal as digit sequences. Equivalently, the $r$-th row of $\mathrm{IC}$ is equal to the $r$-th column of $\mathrm{IC}$, which is the statement of symmetry. $\square$

**Corollary 4.3.** *The transpose-symmetry rate of order-2 Barron Squares is bounded below by the endpoint-pairing distribution: every square in which Case A holds at every inner index and whose edge rows and columns are consistent under transposition is itself self-transpose.* This gives a structural reason (though not a closed-form explanation) for the elevated $\sim\!50\%$ self-transpose rate observed in §4.2.

### 4.4 An 8×8 example

The following is a Barron Square of order 2, displayed in the same format as Example 1.2:

````{=typst}
#align(center)[
```
1 2 │ 1 1 1 6 │ 9 3
2 3 │ 1 6 5 6 │ 7 2
────┼─────────┼────
1 1 │ 1 0 0 1 │ 9 1
1 6 │ 0 6 2 4 │ 3 9
1 5 │ 0 2 2 5 │ 1 5
6 6 │ 1 4 5 2 │ 2 2
────┼─────────┼────
9 7 │ 9 3 1 2 │ 9 6
3 2 │ 1 9 5 2 │ 6 1
```
]
````

Verification (row products): $12\times93=1116$, $23\times72=1656$, $11\times91=1001$, $16\times39=624$ (as "0624"), $15\times15=225$ (as "0225"), $66\times22=1452$, $97\times96=9312$, $32\times61=1952$. All rows and columns verified.

---

## 5. The $4 \times 4 \times 4$ Barron Cube

The Barron condition extends naturally from rows and columns of a $4k \times 4k$ square to axis-aligned lines of a $4k \times 4k \times 4k$ cube. This section introduces the three-dimensional object and shows that, at order 1, no such cube exists.

**Definition 5.1** (Order-$k$ Barron Cube). Let $n = 4k$. An array $M \in \{0, \ldots, 9\}^{n \times n \times n}$ is a *Barron Cube of order $k$* if, for every axis direction $d \in \{x, y, z\}$ and every pair of perpendicular coordinates $(i, j)$, the length-$n$ axis-aligned line $\ell_{d, i, j}$ obtained by fixing the two coordinates perpendicular to $d$ satisfies the order-$k$ Barron condition — that is, the product of its outer $k$-endpoints, read as $k$-digit decimal integers, equals its interior $2k$-block read as a $2k$-digit decimal integer — and no cell in the outermost $k$ layers along any axis is zero.

At order $k = 1$ the object is a $4 \times 4 \times 4$ array whose $48$ axis-aligned lines (three axes $\times$ $16$ perpendicular positions) each satisfy the order-1 row/column Barron condition. The eight vertex cells are the only free parameters: once they are specified, each of the cube's $12$ edges, $6$ face interiors, and $8$ cube-interior cells is forced by at least one $4$-cell Barron line, and existence reduces to the consistency of these forced values across the three axis directions.

**Theorem 5.2.** *There are no $4 \times 4 \times 4$ Barron Cubes.*

*Proof.* Exhaustive enumeration over the full $9^8 = 43{,}046{,}721$-element space of vertex assignments (each vertex in $\{1, \ldots, 9\}$), propagating along each axis and checking consistency at every shared cell, produces zero valid cubes. The computation takes approximately $33.6$ minutes in the reference Python implementation `src/barron_3d.py`. $\square$

**Remark 5.3** (Heuristic probability argument). A $4 \times 4 \times 4$ Barron Cube requires all $6$ face squares (along with all $12$ axis-aligned interior lines) to satisfy the order-1 Barron condition simultaneously. The density of valid order-1 corner quadruples is $118 / 9^4 \approx 1.8 \times 10^{-2}$. Of the $8$ cube vertices, each of the $6$ faces uses $4$, and the faces share vertices in a pattern that gives roughly $3$ effective degrees of independence. Treating face validities as approximately independent after this adjustment gives an expected count of valid cubes of order
$$9^8 \cdot (118 / 9^4)^3 \;\approx\; 4.3 \times 10^7 \cdot 5.8 \times 10^{-6} \;\approx\; 0.25,$$
consistent with the exhaustive finding of zero. The heuristic is not a proof of non-existence, and an algebraic proof remains open.

**Corollary 5.4.** *The Barron Cube construction is not a faithful dimensional lift of the Barron Square: $118$ order-1 Barron Squares exist, but no order-1 Barron Cube extends any subset of them to three dimensions.*

---

## 6. Discussion

This section collects the cross-order trends that emerge from Sections 3 through 5, records the open questions left unresolved by the present work, and concludes.

### 6.1 Cross-order trends

*Corner digit distribution.* The shift from order 1 to order 2 redistributes the corner-digit frequencies as shown below.

| Digit | $4 \times 4$ frequency | $8 \times 8$ frequency | Trend |
|---|---|---|---|
| 1 | $0.0\%$ | $8.1\%$ | excluded $\to$ allowed |
| 2 | $7.6\%$ | $9.6\%$ | |
| 3 | $14.4\%$ | $10.8\%$ | |
| 4 | $12.7\%$ | $12.8\%$ | |
| 5 | $6.8\%$ | $8.8\%$ | restricted $\to$ unrestricted |
| 6 | $12.7\%$ | $11.0\%$ | |
| 7 | $13.6\%$ | $13.5\%$ | |
| 8 | $17.8\%$ | $12.4\%$ | dominant $\to$ average |
| 9 | $14.4\%$ | $13.0\%$ | |

The order-2 distribution is markedly more uniform (range $8.1\%$–$13.5\%$) than the order-1 distribution (range $0\%$–$17.8\%$). The mechanism is the one identified in §4.2: order-$k$ corner *blocks* contain many more factor pairs than single digits, so structural exclusions on individual digits are diluted at higher order.

*Symmetry.* The dihedral group $D_4$ acts on square matrices, and a Barron Square of any order is automatically invariant under transposition because the row and column Barron conditions are identical. No Barron Square in either order is invariant under a non-trivial rotation.

| Symmetry group | $4 \times 4$ ($n = 118$) | $8 \times 8$ ($n = 1{,}248$) |
|---|---|---|
| $|G| = 1$ (no non-trivial symmetry) | $72$ ($61.0\%$) | $624$ ($50.0\%$) |
| $|G| = 2$ (transpose only) | $46$ ($39.0\%$) | $624$ ($50.0\%$) |
| $|G| \geq 4$ | $0$ | $0$ |

The $8 \times 8$ count splits exactly evenly into asymmetric and transpose-symmetric squares. Theorems 4.1 and 4.2 explain part of the order-2 rise: the endpoint pairing dichotomy forces the inner $4 \times 4$ center to be symmetric, which is a *necessary* condition for full-matrix transpose symmetry. Consistent with this, every self-transpose square at order 2 is in Case A of Theorem 4.1 at every inner index, and Case A accounts for $2{,}598$ of the $4{,}992$ observed (square, inner index) pairs — well above the $2{,}394$ of Case B.

*Product structure.* At order 1 the $22$ valid edge products are exactly the two-digit numbers in $[10, 81]$ with no zero digit. At order 2 the valid edge products are four-digit numbers in $[1000, 9801]$ with no zero digit; interiors may contain zeros (only the edge cells are zero-restricted). The order-1 distribution is concentrated: the top two products $12$ and $16$ each occur $48$ times over $118 \times 4 = 472$ edge positions, a frequency of $10.2\%$. At order 2 the most common product, $1892$, occurs only $80$ times over $1{,}248 \times 8 = 9{,}984$ edge positions — a frequency of $0.8\%$. The factor-of-$\sim\!13$ drop in peak product frequency reflects the much larger pool of valid four-digit products.

*Information flow.* The corner blocks are the only genuine degrees of freedom: by Theorem 2.4 every other cell is a deterministic function of the four corner blocks. The data-processing inequality then gives, in the ensemble of order-$k$ Barron Squares under the uniform distribution,
$$H(\text{corner cell}) \;\geq\; H(\text{edge cell}) \;\geq\; H(\text{inner cell}),$$
where $H$ denotes Shannon entropy. The boundary acts as a lossy channel to the interior, and the interior is fully determined by the boundary.

### 6.2 Open questions

Several natural questions are left unresolved.

1. **Independent verification at order 2.** The count of $1{,}248$ Barron Squares at order 2 is produced by a single implementation (`barron8x8.c`) using the BOT-derivation reduction. An independent reimplementation — ideally using a different search strategy, such as constraint propagation or a SAT/SMT encoding — would strengthen confidence in the count.
2. **Algebraic proof of Theorem 4.1 (Endpoint Pairing).** The Case A / Case B dichotomy is verified without exception across all $4{,}992$ observed (square, inner index) pairs but has no closed-form proof. A derivation from the order-2 analogue of the consistency conditions (Corollary 2.2) would explain the dichotomy directly, rather than as an experimental regularity, and would in particular give Theorem 4.2 a fully algebraic proof.
3. **Algebraic proof of Theorem 5.2 (no $4 \times 4 \times 4$ Barron Cube).** The heuristic estimate of $\sim\!0.25$ expected cubes is suggestive but not rigorous. A proof would amount to showing that the three-dimensional consistency system has no digit solutions, presumably by a pigeonhole or residue argument on the shared vertices and edges.
4. **Asymptotic growth in $k$.** The $k = 1 \to k = 2$ transition shows growth by roughly an order of magnitude ($118 \to 1{,}248$), but a random probe of $5 \times 10^5$ configurations at $k = 4$ ($16 \times 16$) finds no valid square. Does the Barron family go extinct at some finite $k$, or does it become extremely sparse but non-empty? An exhaustive or targeted search at $k = 3$ ($12 \times 12$) would sharpen the trend.
5. **Transpose-symmetry rate.** The order-2 self-transpose rate is exactly $50.0\%$, substantially above the order-1 rate of $39\%$. Theorems 4.1 and 4.2 give a partial explanation — Case A implies row/column alignment at every inner index — but do not predict the exact rate, and in particular do not explain the remarkable precise split $624 / 624$.
6. **Base dependence.** The construction is tied to base $10$ through its use of place value. How does the count of Barron Squares depend on the base $b$? Bases $b \in \{2, \ldots, 9\}$ each yield a finite, computable problem at order 1, and bases $12$ or $16$ offer enough room to test whether the qualitative order-1 / order-2 story survives.
7. **Alternative operations.** The multiplicative constraint can be replaced by $L + R = I$ (additive) or $L^2 = I$ (square), among others. The multiplicative form appears special: the additive form is much less constrained and yields infinite families, while most non-multiplicative operations yield either empty or trivial sets.

### 6.3 Concluding remarks

Barron Squares are a small, self-contained corner of recreational number theory that nonetheless exhibit enough structure to support a full paper of theorems and enumerations. The central structural observation — Theorem 2.4, that an order-$k$ Barron Square is completely determined by its four $k \times k$ corner blocks — reduces existence to a system of digit-level consistency conditions on those corners, which are cleanly explicit at order 1 (Corollary 2.2) and cleanly algorithmic at order 2 (the BOT-derivation search of §4.1).

The order-1 case is tight: exactly $118$ squares exist, digit $1$ is structurally excluded from corners, digit $5$ is restricted to odd partners, and $39\%$ of squares are self-transpose. The order-2 case is looser in every respect: the count grows by an order of magnitude (to $1{,}248$), all nine digits appear as corners, and the corner distribution approaches uniformity. Yet order 2 also introduces new rigidity: every $8 \times 8$ Barron Square has a symmetric inner $4 \times 4$ center (Theorem 4.2), forced by an endpoint pairing dichotomy (Theorem 4.1) that holds without exception in $1{,}248$ tested cases. These two theorems are the paper's main new structural results.

The three-dimensional generalization collapses completely: no $4 \times 4 \times 4$ Barron Cube exists, consistent with a heuristic expected count of $\sim\!0.25$. Whether order-$k$ Barron Squares themselves eventually vanish as $k$ grows is — together with an algebraic proof of the endpoint pairing theorem — the most interesting question left open.

---

## References

1. FiveThirtyEight, *The Riddler* column. Puzzle sourced from the "Riddler Express" series, which features short combinatorial and number-theoretic puzzles.
2. W. W. Rouse Ball and H. S. M. Coxeter, *Mathematical Recreations and Essays*, 13th ed., Dover, 1987. [Classical reference for magic squares and multiplicative digit puzzles.]
3. D. E. Knuth, *The Art of Computer Programming, Volume 4: Combinatorial Algorithms*, Addison-Wesley, 2011. [Constraint satisfaction and exact cover methods underlying the enumeration algorithms used here.]
4. P. J. Cameron, *Combinatorics: Topics, Techniques, Algorithms*, Cambridge University Press, 1994. [Symmetry groups acting on combinatorial objects, as used in §3.3 and §6.1.]
5. Source code and data for this paper: `https://github.com/tbarron/barron-squares` (Python and C implementations referenced throughout §3, §4, and §5).

---

## Appendix A: Order-1 corner quadruples

All $118$ valid corner quadruples $(a, b, c, d) = (TL, TR, BL, BR)$ at order 1 are enumerated by `src/find_4x4.py`. The table below records the six *uniform-product* squares of §3.4 (all four edge products equal), as a representative extract; the full list is produced by the enumeration script and is available in the companion code repository.

| $a$ | $b$ | $c$ | $d$ | $ab$ | $cd$ | $ac$ | $bd$ |
|---|---|---|---|---|---|---|---|
| 2 | 7 | 7 | 2 | 14 | 14 | 14 | 14 |
| 7 | 2 | 2 | 7 | 14 | 14 | 14 | 14 |
| 3 | 9 | 9 | 3 | 27 | 27 | 27 | 27 |
| 9 | 3 | 3 | 9 | 27 | 27 | 27 | 27 |
| 6 | 8 | 8 | 6 | 48 | 48 | 48 | 48 |
| 8 | 6 | 6 | 8 | 48 | 48 | 48 | 48 |

These six quadruples form the three transpose pairs $\{14, 27, 48\}$ and realize the only three values of the uniform product that are compatible with the order-1 consistency conditions (C1)–(C3).

## Appendix B: Computational details

- **Order-1 enumeration.** Python (`src/find_4x4.py`), exhaustive over $9^4 = 6{,}561$ corner quadruples. Runtime $< 0.1$ s.
- **Order-2 enumeration.** C (`src/barron8x8.c`), using the BOT-derivation algorithm of §4.1. Throughput $\sim\!6 \times 10^7$ inner checks per second per core. The search is parallelized across $12$ disjoint TL ranges (each covering $9^4 / 12 \approx 547$ values of TL) that together exhaust the full $9^4 = 6{,}561$-element TL space. Total wall-clock time is approximately $50$ hours on a 12-core processor, yielding $1{,}248$ distinct squares.
- **Order-1 cube enumeration.** Python (`src/barron_3d.py`), exhaustive over $9^8 = 43{,}046{,}721$ vertex octuplets. Runtime $33.6$ minutes.
- **Order-4 random probe.** $5 \times 10^5$ random corner configurations of $16 \times 16$ matrices, no valid squares found.
- **Reproducibility.** All code, search outputs, and the TeX/Markdown source of this paper are available in the project repository.

---

### Acknowledgments

The original order-1 puzzle appeared in the FiveThirtyEight *Riddler Express* column, which motivated the generalization and systematic study presented here. The $8 \times 8$ search was executed on macOS with a 12-core processor.
