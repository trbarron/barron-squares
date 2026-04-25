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

We completely characterize the $4 \times 4$ case, finding exactly **118** valid squares by exhaustive enumeration, and develop the algebraic consistency conditions that govern their existence. For the $8 \times 8$ case we report an exhaustive parallel search over all $9^4 = 6{,}561$ top-left corner blocks that yields **1,248** valid squares, a count independently confirmed by a second search using a structurally distinct corner-derivation algorithm. We further show, by exhaustive enumeration over the full space of $9^8 = 43{,}046{,}721$ corner octuplets, that **no valid $4 \times 4 \times 4$ Barron Cube exists**.

Structurally, the central observation is that a Barron Square is determined entirely by its four corner blocks, reducing existence to a small system of digit-level algebraic conditions. Building on this, we show that the inner $4 \times 4$ center of every $8 \times 8$ Barron Square is symmetric, as a consequence of an *endpoint pairing* dichotomy on inner rows and columns that holds without exception across all 1,248 squares. We document a sharp qualitative shift between the two orders: digit 1 is forbidden as a corner at order 1 but permitted at order 2, the corner-digit distribution becomes markedly more uniform, and the self-transpose rate rises from $39\%$ to exactly $50\%$.

**Keywords.** Barron Square, digit matrix, multiplicative constraint, exhaustive enumeration, consistency conditions, recreational mathematics.

**MSC 2020.** 05A15 (Exact enumeration problems), 11A63 (Radix representation; digital problems), 05B15 (Orthogonal arrays, Latin squares, Room squares).

---

## 1. Introduction

### 1.1 Motivation

A single-row version of the problem first appeared as a *FiveThirtyEight Riddler Express* puzzle [1]: find a $4 \times 4$ grid of decimal digits such that every row and every column encodes a valid two-digit multiplication, with the leftmost digit times the rightmost digit equal to the two-digit number formed by the interior pair. The object is elementary to state and yet non-trivial to search: the full space of $9^4 = 6{,}561$ unconstrained corner assignments collapses, after consistency enforcement, to exactly $118$ valid boards. Small, finite answers of this kind are a classical target of *recreational number theory* [2, 5], joining families such as magic squares, cross-figures, and multiplicative alphametics. What distinguishes the present object is that the constraints are simultaneously *positional* (they depend on decimal place value) and *structural* (they couple boundaries to interiors), placing it in a hybrid regime between digit puzzles and constraint satisfaction on integer grids.

This paper formalizes the puzzle, generalizes it to a family of order-$k$ objects of size $4k \times 4k$, and studies its structure by a combination of exhaustive enumeration and algebraic reduction.

### 1.2 Definition

Write $\mathrm{val}(s)$ for the decimal-integer value of a digit sequence $s$, so that $\mathrm{val}(d_1 d_2 \cdots d_n) = \sum_{i=1}^{n} d_i\,10^{n-i}$. For a $4k$-length sequence $s$ we say $s$ has a *left endpoint* (the first $k$ digits), a *right endpoint* (the last $k$ digits), and an *interior* (the middle $2k$ digits).

**Definition 1.1** (Order-$k$ Barron Square). A matrix $M \in \{0,\ldots,9\}^{4k \times 4k}$ is a *Barron Square of order $k$* if:

1. *(Row condition.)* For every row index $i$, with $L_i, R_i$ the left and right endpoints of row $i$ and $I_i$ its interior,
   $$\mathrm{val}(L_i) \cdot \mathrm{val}(R_i) = \mathrm{val}(I_i).$$
2. *(Column condition.)* For every column index $j$, with $T_j, B_j$ the top and bottom endpoints of column $j$ and $J_j$ its interior,
   $$\mathrm{val}(T_j) \cdot \mathrm{val}(B_j) = \mathrm{val}(J_j).$$
3. *(Edge condition.)* No entry in the outermost $k$ rows or $k$ columns of $M$ is zero.

For order $k = 1$ the row and column conditions specialize to the elementary scalar forms
$$M_{i,0} \cdot M_{i,3} = 10\,M_{i,1} + M_{i,2}, \qquad M_{0,j} \cdot M_{3,j} = 10\,M_{1,j} + M_{2,j}.$$

| Order $k$ | Matrix size | Corner block | Edge product width |
|-----------|-------------|--------------|-------------------|
| 1 | $4 \times 4$ | $1 \times 1$ (scalar) | 2 digits |
| 2 | $8 \times 8$ | $2 \times 2$ block | 4 digits |
| 4 | $16 \times 16$ | $4 \times 4$ block | 8 digits |

````{=typst}
#block(breakable: false)[
*#strong[Example 1.2.]* The matrix below is a Barron Square of order 1. Horizontal and vertical separators mark the boundary between the endpoint blocks (each of width $k=1$) and the interior:

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

Verification: the rows give $6 times 7 = 42$, $4 times 5 = 20$, $8 times 6 = 48$, and $8 times 8 = 64$; the columns give $6 times 8 = 48$, $4 times 6 = 24$, $2 times 4 = 08$, and $7 times 8 = 56$. The inner zero in row 1 is permitted because it lies on a non-edge cell.
]
````

### 1.3 Contributions

Our results cover four aspects of Barron Squares — structural reduction, complete enumeration at order 1, exhaustive enumeration and new structural theorems at order 2, and higher-order / higher-dimensional behavior:

1. **Structural reduction.** We prove that an order-$k$ Barron Square is completely determined by its four $k \times k$ corner blocks (Theorems 2.1 and 2.4). For the order-1 case this reduction is sharp: it yields three genuinely restrictive algebraic consistency conditions on the corners $(a,b,c,d)$, with a fourth candidate condition shown to be automatic (Proposition 2.3).
2. **Complete enumeration at order 1.** We prove by exhaustive search that there are exactly $118$ Barron Squares of order 1 (Theorem 3.1), classify them by corner-digit frequency and transpose symmetry, identify the exclusion of digit $1$ and the parity restriction of digit $5$ as structural consequences of the constraint, and isolate a family of six *uniform-product* squares whose four edge products coincide.
3. **Exhaustive enumeration and structure at order 2.** Using a *BOT-derivation* algorithm that reduces the effective search space from $9^{16}$ to a tractable range, we enumerate $1{,}248$ Barron Squares of order 2 by exhaustive parallel search over all $9^4 = 6{,}561$ top-left corner blocks, a count we also independently verify by a second search using a structurally distinct *Full Corner Derivation* algorithm. On this data we establish two new structural results: an *endpoint pairing* dichotomy for inner rows and columns (Proposition 4.1), proven by two-case analysis combining a direct argument in the self-transpose case with a computer-assisted verification over the $624$ asymmetric squares, and, as a consequence, the *inner center symmetry* of every order-2 Barron Square (Theorem 4.2). Whether the endpoint-pairing dichotomy admits a uniform algebraic proof, or extends to higher orders $k \geq 3$, is left open.
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
M_{1,1} = t(M_{1,0}\,M_{1,3}) = t(M_{0,1}\,M_{3,1}), & M_{1,2} = u(M_{1,0}\,M_{1,3}) = t(M_{0,2}\,M_{3,2}), \\[0.25em]
M_{2,1} = t(M_{2,0}\,M_{2,3}) = u(M_{0,1}\,M_{3,1}), & M_{2,2} = u(M_{2,0}\,M_{2,3}) = u(M_{0,2}\,M_{3,2}).
\end{array}$$

*Proof.* Apply row 0's Barron condition: $ab = \mathrm{val}(M_{0,0})\cdot\mathrm{val}(M_{0,3})$ must equal the two-digit number $10\,M_{0,1} + M_{0,2}$, so $M_{0,1} = t(ab)$ and $M_{0,2} = u(ab)$. The same argument applied to row 3 and to columns 0 and 3 gives the eight edge cells displayed in the first block.

With all eight edge cells fixed, the four inner cells are determined by the inner rows and columns. Row 1 has endpoints $M_{1,0} = t(ac)$ and $M_{1,3} = t(bd)$, so its Barron condition requires
$$10\,M_{1,1} + M_{1,2} = t(ac)\cdot t(bd),$$
giving $M_{1,1} = t(t(ac)\,t(bd))$ and $M_{1,2} = u(t(ac)\,t(bd))$. Row 2 and the two inner columns yield the analogous expressions. $\square$

````{=typst}
#v(0.3em)
#figure(
  grid(
    columns: (auto, 2em, auto),
    gutter: 0pt,
    // Left: order-1 with formulas
    {
      let corner = rgb("#2d5016").lighten(70%)
      let edge = rgb("#1a5276").lighten(70%)
      let inner = rgb("#7d3c00").lighten(72%)
      table(
        columns: (2.8em, 2.8em, 2.8em, 2.8em),
        rows: (2em, 2em, 2em, 2em),
        align: center + horizon,
        stroke: 0.5pt,
        fill: (x, y) => {
          if (x == 0 or x == 3) and (y == 0 or y == 3) { corner }
          else if x == 0 or x == 3 or y == 0 or y == 3 { edge }
          else { inner }
        },
        [$a$], [$t(a b)$], [$u(a b)$], [$b$],
        [$t(a c)$], text(size: 7pt)[$M_(1,1)$], text(size: 7pt)[$M_(1,2)$], [$t(b d)$],
        [$u(a c)$], text(size: 7pt)[$M_(2,1)$], text(size: 7pt)[$M_(2,2)$], [$u(b d)$],
        [$c$], [$t(c d)$], [$u(c d)$], [$d$],
      )
    },
    // Spacer
    [],
    // Right: general order-k schematic
    {
      let corner = rgb("#2d5016").lighten(70%)
      let edge = rgb("#1a5276").lighten(70%)
      let inner = rgb("#7d3c00").lighten(72%)
      table(
        columns: (3.5em, 7em, 3.5em),
        rows: (3em, 6.2em, 3em),
        align: center + horizon,
        stroke: 0.5pt,
        fill: (x, y) => {
          if (x == 0 or x == 2) and (y == 0 or y == 2) { corner }
          else if x == 0 or x == 2 or y == 0 or y == 2 { edge }
          else { inner }
        },
        text(size: 8pt, weight: "bold")[$A$],
        text(size: 7pt)[row-forced\ from $A, B$],
        text(size: 8pt, weight: "bold")[$B$],
        text(size: 7pt)[col-forced\ from $A, C$],
        text(size: 7pt)[doubly\ determined\ (must be\ consistent)],
        text(size: 7pt)[col-forced\ from $B, D$],
        text(size: 8pt, weight: "bold")[$C$],
        text(size: 7pt)[row-forced\ from $C, D$],
        text(size: 8pt, weight: "bold")[$D$],
      )
    },
  ),
  kind: "figure",
  supplement: "Figure",
  caption: [Structure of a Barron Square.
    _Left:_ order 1 ($4 times 4$); each cell shows the formula from Theorem 2.1.
    #box(width: 0.8em, height: 0.8em, fill: rgb("#2d5016").lighten(70%), stroke: 0.5pt) corners (free),
    #box(width: 0.8em, height: 0.8em, fill: rgb("#1a5276").lighten(70%), stroke: 0.5pt) edge cells (singly determined),
    #box(width: 0.8em, height: 0.8em, fill: rgb("#7d3c00").lighten(72%), stroke: 0.5pt) inner cells (doubly determined).
    _Right:_ general order $k$ ($4k times 4k$); corners are $k times k$ blocks.],
) <fig-structure>
#v(0.3em)
````

### 2.2 Consistency conditions

The forcing in Theorem 2.1 pins each inner cell *twice* — once by its row and once by its column — so $M$ is a genuine Barron Square only when the two determinations agree.

**Corollary 2.2** (Algebraic consistency conditions for order 1). *A quadruple of non-zero digits $(a,b,c,d)$ extends to a $4 \times 4$ Barron Square if and only if all four edge products $ab, cd, ac, bd$ have non-zero tens and units digits and the following three identities hold:*

- **(C1)** $t(t(ac) \cdot t(bd)) = t(t(ab) \cdot t(cd))$
- **(C2)** $u(t(ac) \cdot t(bd)) = t(u(ab) \cdot u(cd))$
- **(C3)** $t(u(ac) \cdot u(bd)) = u(t(ab) \cdot t(cd))$

*Proof.* Each equation equates the row-determination and column-determination of one of the four inner cells: (C1) corresponds to $M_{1,1}$, (C2) to $M_{1,2}$, and (C3) to $M_{2,1}$. The no-zero-edge condition is exactly the requirement that each of $ab, cd, ac, bd$ be a two-digit number with no zero digit. $\square$

**Proposition 2.3** (Automatic fourth condition). *The candidate consistency equation for $M_{2,2}$, namely* **(C4)** $u(u(ac) \cdot u(bd)) = u(u(ab) \cdot u(cd))$, *is satisfied for every choice of digits $(a,b,c,d)$.*

*Proof.* For any integers $x,y$, $u(x)\,u(y) \equiv x\,y \pmod{10}$, so $u(u(x)\,u(y)) = u(xy)$. Applying this twice,
$$u(u(ac)\,u(bd)) = u((ac)(bd)) = u(abcd) = u((ab)(cd)) = u(u(ab)\,u(cd)). \qquad \square$$

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

The valid corner digits are therefore $\{2, 3, 4, 5, 6, 7, 8, 9\}$. Empirically, the eight admissible digits occur as corners with frequencies ranging from $6.8\%$ (digit $5$, suppressed by Proposition 3.3) to $17.8\%$ (digit $8$); the full frequency table is in Appendix A.

### 3.2 Valid products

The 22 zero-free two-digit numbers in $\{10,\ldots,81\}$ all appear as edge products across the 118 squares, with $12$ and $16$ the most frequent (each 48 times). The full distribution is in Appendix A.

### 3.3 Symmetry and transposition

**Proposition 3.4.** The transpose of a Barron Square is also a Barron Square.

*Proof.* Transposition swaps rows and columns, both of which satisfy the same multiplicative condition. $\square$

Among the 118 squares: **46 are transpose-symmetric** ($M = M^\top$) and **0 are rotationally symmetric**. The 72 non-self-transpose squares form 36 transpose pairs, giving **82 equivalence classes** under transposition.

````{=typst}
#block(breakable: false)[
=== 3.4 Uniform-product squares

Six of the 118 squares have the remarkable property that *all four edge products are equal*:

#align(center)[
#table(
  columns: 5,
  align: center,
  table.header[*TL*][*TR*][*BL*][*BR*][*Product*],
  [2], [7], [7], [2], [14],
  [7], [2], [2], [7], [14],
  [3], [9], [9], [3], [27],
  [9], [3], [3], [9], [27],
  [6], [8], [8], [6], [48],
  [8], [6], [6], [8], [48],
)
]

These form three transpose pairs. Note that in each pair, $a b = c d = a c = b d$, which forces $(a, b, c, d) = (a, b, b, a)$ — the corners must be anti-diagonal symmetric. The three eligible products are $\{14, 27, 48\}$.
]
````

---

## 4. The order-2 case: $8 \times 8$ Barron Squares

At order $k = 2$ the unconstrained corner space has size $9^{16} \approx 1.85 \times 10^{15}$, which is well beyond the reach of brute-force enumeration. We reduce the search to a tractable range via a *BOT-derivation algorithm* (§4.1), carry out an exhaustive parallel enumeration in C (§4.2), and observe two new structural phenomena — an *endpoint pairing* dichotomy for the inner rows and columns, and, as its immediate consequence, the symmetry of the inner $4 \times 4$ center block (§4.3). Section 4.4 exhibits a representative $8 \times 8$ square.

### 4.1 The BOT-derivation algorithm

The key observation is that once the two top corners $\mathrm{TL} = M_{[0,2),[0,2)}$ and $\mathrm{TR} = M_{[0,2),[6,8)}$ are fixed, the top two rows of $M$ are determined (via Theorem 2.4 applied row-wise), which in particular fixes the two-digit *top endpoints* of every column. If one additionally specifies the two-digit bottom endpoints of the two rightmost inner columns — that is, the entries $M_{[6,8),4}$ and $M_{[6,8),5}$, which we denote $\mathrm{col}_4^{\mathrm{B}}$ and $\mathrm{col}_5^{\mathrm{B}}$ — then the column Barron condition forces the four-digit interiors of inner columns 4 and 5, and with them the remaining entries of columns 4 and 5.

Once columns 4 and 5 are complete, each of the eight rows has its right endpoint pair fixed. Together with the left endpoint pair — which comes from $\mathrm{TL}$ for rows 0–1 and from the column-derived entries for rows 2–7 — the Barron row conditions produce the remaining interior entries by exact integer division. In particular, the bottom corners $\mathrm{BL}$ and $\mathrm{BR}$ are *derived* rather than searched. The overall effect is to reduce the search from $9^{16}$ to $9^4 \cdot 9^4 \cdot 9^4 = 9^{12}$ nominal configurations; in practice the effective branching is far smaller still, because each column derivation must return valid single-digit values at every step and fails otherwise.

The implementation in `src/barron8x8.c` achieves approximately $6 \times 10^7$ inner checks per second per core and is parallelized across $12$ disjoint TL ranges covering the full $9^4 = 6{,}561$-element TL space.

### 4.2 Numerical results

The exhaustive parallel search described in §4.1 covers all $9^4 = 6{,}561$ values of TL across $12$ disjoint workers and yields exactly $\mathbf{1{,}248}$ distinct Barron Squares of order 2. Total wall-clock time was approximately $50$ hours on a 12-core processor.

**Independent verification.** A second exhaustive search using a structurally different algorithm — *Full Corner Derivation* (FCD) — confirms the count of $1{,}248$. Where the BOT-derivation takes $(\mathrm{TL}, \mathrm{TR}, \mathrm{col}_4^{\mathrm{B}}, \mathrm{col}_5^{\mathrm{B}})$ as free variables and derives the bottom half of the matrix, the FCD algorithm takes $(\mathrm{TL}, \mathrm{TR}, \mathrm{BL})$ as free variables and derives the fourth corner $\mathrm{BR}$ by intersecting the edge-validity constraints of rows 6–7 and columns 6–7, then verifies inner-block consistency by comparing the $4 \times 4$ inner center as derived from inner rows against the one derived from inner columns. The FCD implementation (`src/verify_8x8.c`) shares no code with the BOT-derivation search. Across $12$ parallel workers partitioning the $6{,}561$ TL values, every per-worker subtotal matches the corresponding count from the canonical dataset, and the grand total agrees exactly. Total verification CPU time was approximately $161$ hours ($19$ hours wall time on $12$ cores). An additional spot check using the Z3 SMT solver [6] with a bitvector encoding of the full $64$-variable constraint system found $10$ solutions in approximately $13$ hours before being terminated, each of which matched a known square.

Two qualitative shifts distinguish order 2 from order 1. First, the structural digit exclusions of order 1 both disappear: digit $1$, forbidden as a $4 \times 4$ corner because $1 \cdot b = b$ is a single digit, functions fine as the tens digit of a 2-digit $8 \times 8$ corner block (values $10,\ldots,19$ all produce genuine two-digit factors), and similarly digit $5$ escapes its mod-10 restriction because partners like $51, 52, \ldots$ evade the parity collision. All nine digits therefore appear as corner cells at order 2 (full frequencies in Appendix B), and their distribution is markedly more uniform than at order 1. Second, the transpose-symmetry rate settles at exactly $50.0\%$ — $624$ self-transpose squares and $624$ asymmetric — a sharp jump from the order-1 rate of $39\%$ and a phenomenon we return to in §4.3.

### 4.3 Endpoint pairing and inner center symmetry

Label the inner column and row indices as $[2,6) = \{2,3,4,5\}$ and, for a short inner index $r \in \{0,1,2,3\}$, define the four *inner-band two-digit endpoints*
$$\begin{aligned}
L(r) &= 10\,M_{2+r,0} + M_{2+r,1}, & R(r) &= 10\,M_{2+r,6} + M_{2+r,7}, \\
T(r) &= 10\,M_{0,2+r} + M_{1,2+r}, & B(r) &= 10\,M_{6,2+r} + M_{7,2+r}.
\end{aligned}$$
Here $L(r)$ and $R(r)$ are the left and right endpoints of inner row $2+r$, while $T(r)$ and $B(r)$ are the top and bottom endpoints of inner column $2+r$. Each determines a four-digit interior via the Barron condition: $L(r)\cdot R(r)$ for the row and $T(r)\cdot B(r)$ for the column. These two interiors jointly fill the inner $4 \times 4$ center block $\mathrm{IC} = M_{[2,6),[2,6)}$.

````{=typst}
#pagebreak()
````

**Proposition 4.1** (Endpoint Pairing at order 2). *For every $8 \times 8$ Barron Square $M$ and every inner index $r \in \{0,1,2,3\}$, exactly one of the following cases holds:*

- *(Case A)* $L(r) = T(r)$ *and* $R(r) = B(r)$;
- *(Case B)* $L(r) = B(r)$ *and* $R(r) = T(r)$.

*In either case $L(r)\,R(r) = T(r)\,B(r)$.*

*Proof (case analysis).* We consider two cases on the transpose symmetry of $M$.

(i) *Self-transpose case ($M = M^\top$).* Then for each $r \in \{0,1,2,3\}$ and each $j \in \{0,1\}$ we have $M_{2+r,\,j} = M_{j,\,2+r}$, so
$$L(r) = 10\,M_{2+r,0} + M_{2+r,1} = 10\,M_{0,2+r} + M_{1,2+r} = T(r),$$
and similarly $M_{2+r,\,6} = M_{6,\,2+r}$ and $M_{2+r,\,7} = M_{7,\,2+r}$ give $R(r) = B(r)$. This is Case A.

(ii) *Asymmetric case ($M \neq M^\top$).* The order-2 enumeration in §4.2 yields exactly $624$ asymmetric Barron Squares (see Table of §4.3 case-pattern distribution below). We verify the dichotomy directly by computing $L(r), R(r), T(r), B(r)$ for each of the $4$ inner indices of each of the $624$ asymmetric squares, a total of $2{,}496$ (square, inner-index) pairs: in every pair, exactly one of Case A or Case B holds (Case A: $102$ pairs; Case B: $2{,}394$ pairs). The computation takes under a second; the verification script is included in the accompanying code.

Combining (i) and (ii) across all $1{,}248$ squares: Case A occurs $2{,}598$ times, Case B occurs $2{,}394$ times, and the dichotomy never fails. $\square$

**Remark 4.1a** (Scope of Proposition 4.1). The proof of (ii) is computer-assisted and valid only for order $k = 2$; it rests on the exhaustive enumeration of §4.2. Whether the analogous statement holds at higher orders — that is, whether the inner-band endpoints of an order-$k$ Barron Square always pair into a Case A / Case B dichotomy with respect to the corresponding edge bands — is formulated as Conjecture 6.1 in §6.2 and remains open. A uniform algebraic proof, i.e., one independent of the enumeration, is likewise open even at order 2.

**Theorem 4.2** (Inner Center Symmetry at order 2). *For every $8 \times 8$ Barron Square the inner center block $\mathrm{IC}$ is a symmetric $4 \times 4$ matrix: $\mathrm{IC}_{r,c} = \mathrm{IC}_{c,r}$ for all $r, c \in \{0,1,2,3\}$.*

*Proof.* By Proposition 4.1 each inner row $r$ and its matching inner column $r$ have endpoints whose (unordered) pair coincides, so their Barron-forced four-digit interiors are equal as digit sequences. Equivalently, the $r$-th row of $\mathrm{IC}$ is equal to the $r$-th column of $\mathrm{IC}$, which is the statement of symmetry. $\square$

**Corollary 4.3** (Necessary condition for transpose symmetry). *If an order-2 Barron Square $M$ is self-transpose, then Case A of Proposition 4.1 holds at every inner index $r \in \{0,1,2,3\}$.*

*Proof.* If $M = M^\top$ then $M_{2+r,\,j} = M_{j,\,2+r}$ for each $j \in \{0,1\}$ and each $r \in \{0,1,2,3\}$, so $L(r) = T(r)$ and $R(r) = B(r)$. $\square$

In particular, every one of the $624$ self-transpose squares contributes to Case A at all four inner indices, accounting for $4 \times 624 = 2{,}496$ of the $2{,}598$ observed Case-A inner-index pairs. The remaining $102$ Case-A pairs arise from asymmetric squares, so Case A at every inner index is a *necessary* but not *sufficient* condition for self-transpose. The tight empirical split $624 / 624$ between self-transpose and asymmetric squares is left as Open Question 4 in §6.2.

The full distribution of (transpose-class, per-inner-index case pattern) across the $1{,}248$ squares is the following:

| Transpose class | Pattern | Count |
|---|---|---|
| Self-transpose | AAAA | $624$ |
| Asymmetric | BBBB | $522$ |
| Asymmetric | ABBB | $56$ |
| Asymmetric | BBBA | $22$ |
| Asymmetric | BABB | $14$ |
| Asymmetric | BBAB | $10$ |

Every self-transpose square is AAAA; no asymmetric square is AAAA; and the dichotomy of Proposition 4.1 never fails. The $522$ purely-Case-B asymmetric squares are the natural counterpart to the AAAA self-transpose family.

*Case B example.* The following is one of the $522$ asymmetric squares in which Case B holds at every inner index. It is displayed in the same format as Example 1.2 and §4.4:

````{=typst}
#align(center)[
```
1 4 │ 1 3 8 6 │ 9 9
8 4 │ 8 1 4 8 │ 9 7
────┼─────────┼────
1 3 │ 0 2 3 4 │ 1 8
7 4 │ 2 2 9 4 │ 3 1
4 7 │ 3 9 4 8 │ 8 4
6 6 │ 4 4 8 8 │ 6 8
────┼─────────┼────
9 7 │ 1 7 4 6 │ 1 8
7 9 │ 3 4 7 6 │ 4 4
```
]
````

The row products ($14 \times 99 = 1386$, $84 \times 97 = 8148$, $13 \times 18 = 234$, $74 \times 31 = 2294$, $47 \times 84 = 3948$, $66 \times 68 = 4488$, $97 \times 18 = 1746$, $79 \times 44 = 3476$) and column products ($18 \times 97 = 1746$, $44 \times 79 = 3476$, $18 \times 13 = 234$, $31 \times 74 = 2294$, $84 \times 47 = 3948$, $68 \times 66 = 4488$, $99 \times 14 = 1386$, $97 \times 84 = 8148$) verify directly. The inner-band endpoints $L(r), R(r), T(r), B(r)$ are as follows:

| $r$ | $L(r)$ | $R(r)$ | $T(r)$ | $B(r)$ | Pairing |
|:---:|:---:|:---:|:---:|:---:|:---:|
| $0$ | $13$ | $18$ | $18$ | $13$ | Case B ($L=B$, $R=T$) |
| $1$ | $74$ | $31$ | $31$ | $74$ | Case B |
| $2$ | $47$ | $84$ | $84$ | $47$ | Case B |
| $3$ | $66$ | $68$ | $68$ | $66$ | Case B |

At every inner index the row-endpoint pair $(L, R)$ equals the column-endpoint pair $(T, B)$ reversed, and correspondingly the inner $4 \times 4$ center block agrees with its transpose (Theorem 4.2). Note that the square is *not* self-transpose — the corner blocks differ, $\mathrm{TL} = \left[\begin{smallmatrix}1 & 4 \\ 8 & 4\end{smallmatrix}\right] \neq \left[\begin{smallmatrix}1 & 8 \\ 4 & 4\end{smallmatrix}\right] = \mathrm{TL}^\top$ — yet the inner center symmetry forced by Proposition 4.1 still holds.

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

Verification (row products): $12\times93=1116$, $23\times72=1656$, $11\times91=1001$, $16\times39=624$, $15\times15=225$, $66\times22=1452$, $97\times96=9312$, $32\times61=1952$. Interiors are padded to the full $2k = 4$ digits with leading zeros when the product has fewer than four digits — so row 3 writes the 3-digit product $624$ as $\mathtt{0624}$ across cells $(3,2)$–$(3,5)$, and row 4 writes $225$ as $\mathtt{0225}$. Leading zeros are permitted in these positions because they are inner (non-edge) cells. All rows and columns verified.

---

## 5. The $4 \times 4 \times 4$ Barron Cube

The Barron condition extends naturally from rows and columns of a $4k \times 4k$ square to axis-aligned lines of a $4k \times 4k \times 4k$ cube. This section introduces the three-dimensional object and shows that, at order 1, no such cube exists.

**Definition 5.1** (Order-$k$ Barron Cube). Let $n = 4k$. An array $M \in \{0, \ldots, 9\}^{n \times n \times n}$ is a *Barron Cube of order $k$* if, for every axis direction $d \in \{x, y, z\}$ and every pair of perpendicular coordinates $(i, j)$, the length-$n$ axis-aligned line $\ell_{d, i, j}$ obtained by fixing the two coordinates perpendicular to $d$ satisfies the order-$k$ Barron condition — that is, the product of its outer $k$-endpoints, read as $k$-digit decimal integers, equals its interior $2k$-block read as a $2k$-digit decimal integer — and no cell in the outermost $k$ layers along any axis is zero.

At order $k = 1$ the object is a $4 \times 4 \times 4$ array whose $48$ axis-aligned lines (three axes $\times$ $16$ perpendicular positions) each satisfy the order-1 row/column Barron condition. The eight vertex cells are the only free parameters: once they are specified, each of the cube's $12$ edges, $6$ face interiors, and $8$ cube-interior cells is forced by at least one $4$-cell Barron line, and existence reduces to the consistency of these forced values across the three axis directions.

**Theorem 5.2.** *There are no $4 \times 4 \times 4$ Barron Cubes.*

*Proof.* Exhaustive enumeration over the full $9^8 = 43{,}046{,}721$-element space of vertex assignments (each vertex in $\{1, \ldots, 9\}$), propagating along each axis and checking consistency at every shared cell, produces zero valid cubes. The computation takes approximately $33.6$ minutes in the reference Python implementation `src/barron_3d.py`. $\square$

**Remark 5.3** (Heuristic probability argument). A $4 \times 4 \times 4$ Barron Cube must simultaneously satisfy (i) all $6$ face-squares being valid order-$1$ Barron Squares and (ii) three-way axis consistency at each of the $8$ cube-interior cells, where the $x$-, $y$-, and $z$-axis lines through the cell independently determine its value.

For a *single* face, the probability that $4$ vertices sampled uniformly from $\{1,\ldots,9\}^4$ form a valid order-$1$ corner quadruple is $p = 118 / 9^4 \approx 1.8 \times 10^{-2}$. The $6$ faces pair into $3$ *opposite-face* pairs, each pair using disjoint vertex quadruples; within a pair the two face-validity events are independent, but the $3$ pairs overlap through shared vertices. Under the simplifying — and optimistic — assumption that the $3$ opposite-face pairs are themselves independent, the expected number of $8$-vertex assignments satisfying the $6$ face-validity conditions alone is approximately
$$9^8 \cdot p^{3} = \frac{118^{3}}{9^{4}}  \approx  250.$$
This is an *upper-bound* heuristic: it ignores both the positive correlation between opposite-face pairs and the additional $8$ cube-interior consistency conditions of constraint (ii), each of which imposes a three-way digit-agreement with a naive probability on the order of $10^{-2}$. Applying even a fraction of the interior constraints drops the expected count by many orders of magnitude, making the exhaustive finding of zero qualitatively consistent with a fully-coupled expectation well below $1$. The heuristic is not a proof; an algebraic non-existence argument remains open as Question 2 of §6.2.

**Corollary 5.4.** *The Barron Cube construction is not a faithful dimensional lift of the Barron Square: $118$ order-1 Barron Squares exist, but no order-1 Barron Cube extends any subset of them to three dimensions.*

---

## 6. Discussion

This section collects the cross-order trends that emerge from Sections 3 through 5, records the open questions left unresolved by the present work, and concludes.

### 6.1 Cross-order trends

Three structural shifts distinguish order 2 from order 1.

*Digit exclusions disappear.* At order 1, digit $1$ is forbidden as a corner (Proposition 3.2) and digit $5$ is restricted to odd partners (Proposition 3.3). Both restrictions evaporate at order 2, where corners are 2-digit blocks rather than single digits: block values $10,\ldots,19$ produce legitimate two-digit factors, and 2-digit partners of $5$ such as $51, 52, \ldots$ evade the mod-10 collision. All nine digits accordingly appear as corner cells at order 2, and their distribution tightens to the range $[8.1\%, 13.5\%]$ from the order-1 range $[0\%, 17.8\%]$. The mechanism is generic: structural exclusions on individual digits are diluted when corners are blocks.

*Self-transpose rate jumps.* The order-1 self-transpose rate is $46/118 \approx 39\%$. The order-2 rate settles at exactly $624/1{,}248 = 50.0\%$. Proposition 4.1 and Theorem 4.2 give a partial explanation: the endpoint-pairing dichotomy forces the inner $4 \times 4$ center to be symmetric, which is a necessary condition for full-matrix transpose symmetry and ensures that every self-transpose square is in Case A at every inner index. What Proposition 4.1 does *not* explain is the exact $624/624$ split — an open question (§6.2, item 4). No square in either order has non-trivial rotational symmetry.

*Product spectrum flattens.* At order 1 the $22$ valid edge products are exactly the two-digit numbers in $[10, 81]$ with no zero digit, and the top two ($12$ and $16$) occur $48/472 \approx 10.2\%$ of the time each. At order 2 the pool of zero-free four-digit products is far larger, and no single product dominates: $668$ distinct values cover $1{,}248 \cdot 8 = 9{,}984$ edge positions, with the top product $1892$ occurring only $80$ times ($0.8\%$). Interiors at order 2 may contain zeros (only the edge cells are zero-restricted), further expanding the admissible interior-digit patterns.

These shifts fit a single picture: Theorem 2.4 makes the corner blocks the only genuine degrees of freedom, and at higher order the corner *space* is simply much larger — $9^{16}$ at order 2 versus $9^4$ at order 1 — so residue obstructions that bite at order 1 are averaged away.

### 6.2 Open questions

Several natural questions are left unresolved.

1. **Uniform algebraic proof of Proposition 4.1 (Endpoint Pairing), and extension to higher orders.** At order 2 the asymmetric case of Proposition 4.1 is established by direct enumeration over the $624$ asymmetric Barron Squares; a *uniform* algebraic derivation — one that does not depend on the enumeration — is open even at order 2. More strongly, **Conjecture 6.1** (Endpoint Pairing, general order). *For every order-$k$ Barron Square and every inner-band index $r \in \{0, 1, \ldots, 2k-1\}$, the row-endpoint pair $(L(r), R(r))$ and the column-endpoint pair $(T(r), B(r))$ coincide as unordered multisets.* A proof of Conjecture 6.1 from the order-$k$ analogue of the consistency conditions (Corollary 2.2) would in particular give Theorem 4.2 an enumeration-free proof and would extend Inner Center Symmetry to all orders.
2. **Algebraic proof of Theorem 5.2 (no $4 \times 4 \times 4$ Barron Cube).** The heuristic expected count of approximately $250$ from face-validity alone (which falls well below $1$ once the cube-interior consistency conditions are imposed) is suggestive but not rigorous. A proof would amount to showing that the three-dimensional consistency system has no digit solutions, presumably by a pigeonhole or residue argument on the shared vertices and edges.
3. **Asymptotic growth in $k$.** The $k = 1 \to k = 2$ transition shows growth by roughly an order of magnitude ($118 \to 1{,}248$), but a random probe of $5 \times 10^5$ configurations at $k = 4$ ($16 \times 16$) finds no valid square. Does the Barron family go extinct at some finite $k$, or does it become extremely sparse but non-empty? An exhaustive or targeted search at $k = 3$ ($12 \times 12$) would sharpen the trend.
4. **Transpose-symmetry rate.** The order-2 self-transpose rate is exactly $50.0\%$, substantially above the order-1 rate of $39\%$. Proposition 4.1 and Theorem 4.2 give a partial explanation — Case A implies row/column alignment at every inner index — but do not predict the exact rate, and in particular do not explain the remarkable precise split $624 / 624$.
5. **Base dependence.** The construction is tied to base $10$ through its use of place value. How does the count of Barron Squares depend on the base $b$? Bases $b \in \{2, \ldots, 9\}$ each yield a finite, computable problem at order 1, and bases $12$ or $16$ offer enough room to test whether the qualitative order-1 / order-2 story survives. The resulting count sequences — together with the order-$k$ count sequence at base $10$, currently known to begin $(118, 1{,}248, \ldots)$ — are natural OEIS entries [7].
6. **Alternative operations.** The multiplicative constraint can be replaced by $L + R = I$ (additive) or $L^2 = I$ (square), among others. The multiplicative form appears special: the additive form is much less constrained and yields infinite families, while most non-multiplicative operations yield either empty or trivial sets.

### 6.3 Concluding remarks

Barron Squares are a small, self-contained corner of recreational number theory that nonetheless exhibit enough structure to support a full paper of theorems and enumerations. The central structural observation — Theorem 2.4, that an order-$k$ Barron Square is completely determined by its four $k \times k$ corner blocks — reduces existence to a system of digit-level consistency conditions on those corners, which are cleanly explicit at order 1 (Corollary 2.2) and cleanly algorithmic at order 2 (the BOT-derivation search of §4.1).

The order-1 case is tight: exactly $118$ squares exist, digit $1$ is structurally excluded from corners, digit $5$ is restricted to odd partners, and $39\%$ of squares are self-transpose. The order-2 case is looser in every respect: the count grows by an order of magnitude (to $1{,}248$), all nine digits appear as corners, and the corner distribution approaches uniformity. Yet order 2 also introduces new rigidity: every $8 \times 8$ Barron Square has a symmetric inner $4 \times 4$ center (Theorem 4.2), forced by an endpoint-pairing dichotomy (Proposition 4.1) that holds across all $1{,}248$ squares via a two-case proof — direct in the self-transpose half, computer-assisted in the asymmetric half. These are the paper's main new structural results.

The three-dimensional generalization collapses completely: no $4 \times 4 \times 4$ Barron Cube exists. The corrected heuristic expected count — approximately $250$ from face-validity alone, and far lower after the cube-interior consistency conditions are imposed — is qualitatively consistent with the exhaustive finding of zero without explaining it proof-theoretically. Whether order-$k$ Barron Squares themselves eventually vanish as $k$ grows is — together with a uniform algebraic proof of the endpoint-pairing dichotomy (Conjecture 6.1) and its extension to higher orders — the most interesting question left open.

---

## References

1. Z. Wissner-Gross, *Can You Crack This Square's Hidden Code?*, FiveThirtyEight *Riddler* column, available at <https://fivethirtyeight.com/features/can-you-crack-this-squares-hidden-code/>. The original order-1 puzzle that motivated this work.
2. W. W. Rouse Ball and H. S. M. Coxeter, *Mathematical Recreations and Essays*, 13th ed., Dover, 1987. [Classical reference for magic squares and multiplicative digit puzzles.]
3. D. E. Knuth, *The Art of Computer Programming, Volume 4: Combinatorial Algorithms*, Addison-Wesley, 2011. [Constraint satisfaction and exact cover methods underlying the enumeration algorithms used here.]
4. P. J. Cameron, *Combinatorics: Topics, Techniques, Algorithms*, Cambridge University Press, 1994. [Symmetry groups acting on combinatorial objects, as used in §3.3 and §6.1.]
5. R. K. Guy, *Unsolved Problems in Number Theory*, 3rd ed., Springer-Verlag, 2004. [Standard reference for digit-pattern and radix-representation problems in the style of §3 and §6.2.]
6. L. de Moura and N. Bjørner, *Z3: An Efficient SMT Solver*, in *Tools and Algorithms for the Construction and Analysis of Systems* (TACAS 2008), LNCS 4963, Springer, 2008, pp. 337–340. [SMT solver used for the auxiliary bitvector spot-check in §4.2.]
7. OEIS Foundation Inc., *The On-Line Encyclopedia of Integer Sequences*, available at <https://oeis.org>. [Registration of the order-$k$ count sequence $(118, 1248, \ldots)$ is a natural follow-on item, noted in §6.2.]
8. T. Barron, *Barron Squares source code and data*, GitHub repository, available at <https://github.com/trbarron/barron-squares>. Python and C implementations referenced throughout §3, §4, and §5, together with the canonical enumeration output in `results/`.

---

## Appendix A: Representative order-1 Barron Squares

The complete list of all $118$ order-1 Barron Squares is available in machine-readable form as `results/4x4_squares.json` in the project repository [8]. By Theorem 2.1 each square is uniquely determined by its corner quadruple $(a,b,c,d) = (\mathrm{TL},\mathrm{TR},\mathrm{BL},\mathrm{BR})$, so the dataset is effectively a list of valid quadruples. The structural properties of the full set are summarized in §3.1–§3.4: digit $1$ is excluded and digit $5$ is restricted (Propositions 3.2–3.3), $46$ of the $118$ squares are self-transpose, the $22$ zero-free two-digit products that appear as edge values are enumerated in §3.2, and the six uniform-product squares are listed in §3.4.

Example 1.2 displays one canonical square. Below are three additional representatives, chosen to exhibit structural diversity — all three are asymmetric (not self-transpose), none are uniform-product, and they span a range of corner-digit patterns:

````{=typst}
#align(center)[
```
4 │ 1 6 │ 4          5 │ 3 5 │ 7          6 │ 2 4 │ 4
──┼─────┼──          ──┼─────┼──          ──┼─────┼──
2 │ 0 2 │ 1          4 │ 1 2 │ 3          4 │ 1 2 │ 3
4 │ 2 4 │ 6          5 │ 2 5 │ 5          2 │ 0 4 │ 2
──┼─────┼──          ──┼─────┼──          ──┼─────┼──
6 │ 2 4 │ 4          9 │ 4 5 │ 5          7 │ 5 6 │ 8

   (a)                    (b)                    (c)
```
]
````

Corner quadruples: (a) $(4,4,6,4)$; (b) $(5,7,9,5)$; (c) $(6,4,7,8)$. Row and column products are verified by direct arithmetic; e.g., in (b), row 0 gives $5 \cdot 7 = 35$ and column 3 gives $7 \cdot 5 = 35$.

**Corner-digit frequencies at order 1** (referenced in §3.1):

| Digit | Count | Frequency | Note |
|---|---|---|---|
| $1$ | $0$ | $0.0\%$ | excluded (Proposition 3.2) |
| $2$ | $36$ | $7.6\%$ | low — pairs only with $\{6,7,8,9\}$ |
| $3$ | $68$ | $14.4\%$ | |
| $4$ | $60$ | $12.7\%$ | |
| $5$ | $32$ | $6.8\%$ | restricted (Proposition 3.3) |
| $6$ | $60$ | $12.7\%$ | |
| $7$ | $64$ | $13.6\%$ | |
| $8$ | $84$ | $17.8\%$ | most common |
| $9$ | $68$ | $14.4\%$ | |

The 22 two-digit products with no zero digit that appear across all 118 squares are
$$\{12, 14, 15, 16, 18, 21, 24, 25, 27, 28, 32, 35, 36, 42, 45, 48, 54, 56, 63, 64, 72, 81\},$$
with $12$ and $16$ each appearing $48$ times (tied most frequent) and $24$ and $56$ each appearing $40$ times.

Readers seeking the full enumeration or wishing to reproduce any derived statistic can load `results/4x4_squares.json` directly or regenerate it in under a second via `python src/find_4x4.py`.

<!--

Legacy full 118-row table (preserved below as an HTML comment in the Markdown source; not rendered in the PDF). To restore the printed appendix, remove the surrounding comment markers.

| $a$ | $b$ | $c$ | $d$ | $ab$ | $cd$ | $ac$ | $bd$ | Notes |
|---|---|---|---|---|---|---|---|---|
| 2 | 6 | 6 | 3 | 12 | 18 | 12 | 18 | S |
| 2 | 6 | 8 | 2 | 12 | 16 | 16 | 12 |  |
| 2 | 6 | 9 | 2 | 12 | 18 | 18 | 12 |  |
| 2 | 7 | 7 | 2 | 14 | 14 | 14 | 14 | U, S |
| 2 | 8 | 6 | 2 | 16 | 12 | 12 | 16 |  |
| 2 | 8 | 8 | 3 | 16 | 24 | 16 | 24 | S |
| 2 | 8 | 8 | 6 | 16 | 48 | 16 | 48 | S |
| 2 | 9 | 6 | 2 | 18 | 12 | 12 | 18 |  |
| 2 | 9 | 9 | 5 | 18 | 45 | 18 | 45 | S |
| 3 | 4 | 4 | 4 | 12 | 16 | 12 | 16 | S |
| 3 | 4 | 5 | 3 | 12 | 15 | 15 | 12 |  |
| 3 | 4 | 6 | 3 | 12 | 18 | 18 | 12 |  |
| 3 | 5 | 4 | 3 | 15 | 12 | 12 | 15 |  |
| 3 | 5 | 5 | 5 | 15 | 25 | 15 | 25 | S |
| 3 | 5 | 8 | 3 | 15 | 24 | 24 | 15 |  |
| 3 | 6 | 4 | 3 | 18 | 12 | 12 | 18 |  |
| 3 | 6 | 6 | 2 | 18 | 12 | 18 | 12 | S |
| 3 | 7 | 7 | 8 | 21 | 56 | 21 | 56 | S |
| 3 | 7 | 8 | 8 | 21 | 64 | 24 | 56 |  |
| 3 | 7 | 9 | 8 | 21 | 72 | 27 | 56 |  |
| 3 | 8 | 5 | 3 | 24 | 15 | 15 | 24 |  |
| 3 | 8 | 7 | 8 | 24 | 56 | 21 | 64 |  |
| 3 | 8 | 8 | 2 | 24 | 16 | 24 | 16 | S |
| 3 | 9 | 7 | 8 | 27 | 56 | 21 | 72 |  |
| 3 | 9 | 9 | 3 | 27 | 27 | 27 | 27 | U, S |
| 3 | 9 | 9 | 7 | 27 | 63 | 27 | 63 | S |
| 4 | 3 | 3 | 5 | 12 | 15 | 12 | 15 | S |
| 4 | 3 | 3 | 6 | 12 | 18 | 12 | 18 | S |
| 4 | 3 | 4 | 4 | 12 | 16 | 16 | 12 |  |
| 4 | 4 | 3 | 4 | 16 | 12 | 12 | 16 |  |
| 4 | 4 | 4 | 3 | 16 | 12 | 16 | 12 | S |
| 4 | 4 | 4 | 6 | 16 | 24 | 16 | 24 | S |
| 4 | 4 | 4 | 9 | 16 | 36 | 16 | 36 | S |
| 4 | 4 | 6 | 4 | 16 | 24 | 24 | 16 |  |
| 4 | 4 | 9 | 4 | 16 | 36 | 36 | 16 |  |
| 4 | 6 | 4 | 4 | 24 | 16 | 16 | 24 |  |
| 4 | 6 | 8 | 7 | 24 | 56 | 32 | 42 |  |
| 4 | 7 | 7 | 9 | 28 | 63 | 28 | 63 | S |
| 4 | 8 | 6 | 7 | 32 | 42 | 24 | 56 |  |
| 4 | 9 | 4 | 4 | 36 | 16 | 16 | 36 |  |
| 4 | 9 | 9 | 8 | 36 | 72 | 36 | 72 | S |
| 5 | 3 | 3 | 4 | 15 | 12 | 15 | 12 | S |
| 5 | 3 | 3 | 8 | 15 | 24 | 15 | 24 | S |
| 5 | 3 | 5 | 5 | 15 | 25 | 25 | 15 |  |
| 5 | 5 | 3 | 5 | 25 | 15 | 15 | 25 |  |
| 5 | 5 | 5 | 3 | 25 | 15 | 25 | 15 | S |
| 5 | 7 | 9 | 5 | 35 | 45 | 45 | 35 |  |
| 5 | 9 | 7 | 5 | 45 | 35 | 35 | 45 |  |
| 5 | 9 | 9 | 2 | 45 | 18 | 45 | 18 | S |
| 6 | 2 | 2 | 8 | 12 | 16 | 12 | 16 | S |
| 6 | 2 | 2 | 9 | 12 | 18 | 12 | 18 | S |
| 6 | 2 | 3 | 6 | 12 | 18 | 18 | 12 |  |
| 6 | 3 | 2 | 6 | 18 | 12 | 12 | 18 |  |
| 6 | 3 | 3 | 4 | 18 | 12 | 18 | 12 | S |
| 6 | 4 | 4 | 4 | 24 | 16 | 24 | 16 | S |
| 6 | 4 | 7 | 8 | 24 | 56 | 42 | 32 |  |
| 6 | 7 | 4 | 8 | 42 | 32 | 24 | 56 |  |
| 6 | 7 | 8 | 8 | 42 | 64 | 48 | 56 |  |
| 6 | 7 | 9 | 6 | 42 | 54 | 54 | 42 |  |
| 6 | 8 | 7 | 8 | 48 | 56 | 42 | 64 |  |
| 6 | 8 | 8 | 2 | 48 | 16 | 48 | 16 | S |
| 6 | 8 | 8 | 6 | 48 | 48 | 48 | 48 | U, S |
| 6 | 9 | 7 | 6 | 54 | 42 | 42 | 54 |  |
| 6 | 9 | 9 | 9 | 54 | 81 | 54 | 81 | S |
| 7 | 2 | 2 | 7 | 14 | 14 | 14 | 14 | U, S |
| 7 | 3 | 8 | 7 | 21 | 56 | 56 | 21 |  |
| 7 | 3 | 8 | 8 | 21 | 64 | 56 | 24 |  |
| 7 | 3 | 8 | 9 | 21 | 72 | 56 | 27 |  |
| 7 | 4 | 9 | 7 | 28 | 63 | 63 | 28 |  |
| 7 | 5 | 5 | 9 | 35 | 45 | 35 | 45 | S |
| 7 | 6 | 6 | 9 | 42 | 54 | 42 | 54 | S |
| 7 | 6 | 8 | 4 | 42 | 32 | 56 | 24 |  |
| 7 | 6 | 8 | 8 | 42 | 64 | 56 | 48 |  |
| 7 | 8 | 3 | 7 | 56 | 21 | 21 | 56 |  |
| 7 | 8 | 3 | 8 | 56 | 24 | 21 | 64 |  |
| 7 | 8 | 3 | 9 | 56 | 27 | 21 | 72 |  |
| 7 | 8 | 6 | 4 | 56 | 24 | 42 | 32 |  |
| 7 | 8 | 6 | 8 | 56 | 48 | 42 | 64 |  |
| 7 | 9 | 4 | 7 | 63 | 28 | 28 | 63 |  |
| 7 | 9 | 9 | 3 | 63 | 27 | 63 | 27 | S |
| 8 | 2 | 2 | 6 | 16 | 12 | 16 | 12 | S |
| 8 | 2 | 3 | 8 | 16 | 24 | 24 | 16 |  |
| 8 | 2 | 6 | 8 | 16 | 48 | 48 | 16 |  |
| 8 | 3 | 2 | 8 | 24 | 16 | 16 | 24 |  |
| 8 | 3 | 3 | 5 | 24 | 15 | 24 | 15 | S |
| 8 | 3 | 8 | 7 | 24 | 56 | 64 | 21 |  |
| 8 | 4 | 7 | 6 | 32 | 42 | 56 | 24 |  |
| 8 | 6 | 2 | 8 | 48 | 16 | 16 | 48 |  |
| 8 | 6 | 6 | 8 | 48 | 48 | 48 | 48 | U, S |
| 8 | 6 | 8 | 7 | 48 | 56 | 64 | 42 |  |
| 8 | 7 | 4 | 6 | 56 | 24 | 32 | 42 |  |
| 8 | 7 | 7 | 3 | 56 | 21 | 56 | 21 | S |
| 8 | 7 | 8 | 3 | 56 | 24 | 64 | 21 |  |
| 8 | 7 | 8 | 6 | 56 | 48 | 64 | 42 |  |
| 8 | 7 | 9 | 3 | 56 | 27 | 72 | 21 |  |
| 8 | 8 | 3 | 7 | 64 | 21 | 24 | 56 |  |
| 8 | 8 | 6 | 7 | 64 | 42 | 48 | 56 |  |
| 8 | 8 | 7 | 3 | 64 | 21 | 56 | 24 |  |
| 8 | 8 | 7 | 6 | 64 | 42 | 56 | 48 |  |
| 8 | 9 | 7 | 3 | 72 | 21 | 56 | 27 |  |
| 8 | 9 | 9 | 4 | 72 | 36 | 72 | 36 | S |
| 9 | 2 | 2 | 6 | 18 | 12 | 18 | 12 | S |
| 9 | 2 | 5 | 9 | 18 | 45 | 45 | 18 |  |
| 9 | 3 | 3 | 9 | 27 | 27 | 27 | 27 | U, S |
| 9 | 3 | 7 | 9 | 27 | 63 | 63 | 27 |  |
| 9 | 3 | 8 | 7 | 27 | 56 | 72 | 21 |  |
| 9 | 4 | 4 | 4 | 36 | 16 | 36 | 16 | S |
| 9 | 4 | 8 | 9 | 36 | 72 | 72 | 36 |  |
| 9 | 5 | 2 | 9 | 45 | 18 | 18 | 45 |  |
| 9 | 5 | 5 | 7 | 45 | 35 | 45 | 35 | S |
| 9 | 6 | 6 | 7 | 54 | 42 | 54 | 42 | S |
| 9 | 6 | 9 | 9 | 54 | 81 | 81 | 54 |  |
| 9 | 7 | 3 | 9 | 63 | 27 | 27 | 63 |  |
| 9 | 7 | 7 | 4 | 63 | 28 | 63 | 28 | S |
| 9 | 8 | 3 | 7 | 72 | 21 | 27 | 56 |  |
| 9 | 8 | 4 | 9 | 72 | 36 | 36 | 72 |  |
| 9 | 9 | 6 | 9 | 81 | 54 | 54 | 81 |  |
| 9 | 9 | 9 | 6 | 81 | 54 | 81 | 54 | S |

-->


## Appendix B: Computational details

- **Order-1 enumeration.** Python (`src/find_4x4.py`), exhaustive over $9^4 = 6{,}561$ corner quadruples. Runtime $< 0.1$ s.
- **Order-2 enumeration.** C (`src/barron8x8.c`), using the BOT-derivation algorithm of §4.1. Throughput approximately $6 \times 10^7$ inner checks per second per core. The search is parallelized across $12$ disjoint TL ranges (each covering $9^4 / 12 \approx 547$ values of TL) that together exhaust the full $9^4 = 6{,}561$-element TL space. Total wall-clock time is approximately $50$ hours on a 12-core processor, yielding $1{,}248$ distinct squares.
- **Order-2 independent verification.** C (`src/verify_8x8.c`), using the Full Corner Derivation (FCD) algorithm. Free variables are TL, TR, BL (12 digits); BR is derived by intersecting the edge-validity constraints of rows 6–7 and columns 6–7, and the inner $4 \times 4$ center is cross-checked between row and column derivations. The FCD search is parallelized identically ($12$ workers partitioning the TL space). Total CPU time approximately $161$ hours ($19$ hours wall time on $12$ cores), confirming $1{,}248$ squares with per-worker counts matching exactly.
- **Order-1 cube enumeration.** Python (`src/barron_3d.py`), exhaustive over $9^8 = 43{,}046{,}721$ vertex octuplets. Runtime $33.6$ minutes.
- **Order-4 random probe.** $5 \times 10^5$ random corner configurations of $16 \times 16$ matrices, no valid squares found.
- **Reproducibility.** All code, search outputs, and the TeX/Markdown source of this paper are available in the project repository.

**Corner-cell frequencies at order 2** (referenced in §4.2 and §6.1). Corner *cells* rather than corner *digits*: each square has $4$ $2 \times 2$ corner blocks containing $16$ digit positions in total, giving $1{,}248 \cdot 16 = 19{,}968$ corner-cell observations.

| Digit | Count | Frequency |
|---|---|---|
| $1$ | $1{,}624$ | $8.1\%$ |
| $2$ | $1{,}908$ | $9.6\%$ |
| $3$ | $2{,}160$ | $10.8\%$ |
| $4$ | $2{,}564$ | $12.8\%$ |
| $5$ | $1{,}760$ | $8.8\%$ |
| $6$ | $2{,}188$ | $11.0\%$ |
| $7$ | $2{,}696$ | $13.5\%$ |
| $8$ | $2{,}480$ | $12.4\%$ |
| $9$ | $2{,}588$ | $13.0\%$ |

**Top edge products at order 2** (referenced in §6.1). Of $668$ distinct four-digit products across $9{,}984$ edge positions, the fifteen most frequent are:

| Rank | Product | Count | Rank | Product | Count | Rank | Product | Count |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|  1 | $1892$ | $80$ |  6 | $2475$ | $56$ | 11 | $1632$ | $48$ |
|  2 | $1782$ | $72$ |  7 | $3168$ | $56$ | 12 | $1365$ | $48$ |
|  3 | $1596$ | $64$ |  8 | $1197$ | $56$ | 13 | $2496$ | $48$ |
|  4 | $2376$ | $64$ |  9 | $1274$ | $48$ | 14 | $1155$ | $40$ |
|  5 | $1116$ | $56$ | 10 | $1224$ | $48$ | 15 | $3243$ | $40$ |

---

### Acknowledgments

The original order-1 puzzle appeared in the FiveThirtyEight *Riddler Express* column, which motivated the generalization and systematic study presented here. The $8 \times 8$ search was executed on macOS with a 12-core processor.
