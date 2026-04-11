# Barron Squares

A **Barron Square of order $k$** is a $(4k \times 4k)$ matrix of decimal digits in which every row and every column satisfies a single multiplicative rule:

> the $k$-digit number on the left, times the $k$-digit number on the right, equals the $2k$-digit number in the middle.

No zeros are allowed in the outermost $k$ rows and columns. A small order-1 example (row 1: $6 \times 7 = 42$; column 1: $6 \times 8 = 48$):

```
6 │ 4 2 │ 7
──┼─────┼──
4 │ 2 0 │ 5
8 │ 4 8 │ 6
──┼─────┼──
8 │ 6 4 │ 8
```

The construction generalizes a single-row digit-multiplication puzzle from the FiveThirtyEight *Riddler Express* column (see `paper/barron_squares.md`, reference [1]) to a family of $4k \times 4k$ objects, and extends naturally to three dimensions via $4k \times 4k \times 4k$ *Barron Cubes*. This repository contains the accompanying research paper, the code that enumerates the objects, and the canonical datasets produced by those enumerations.

## What's here

- **`paper/`** — The paper `barron_squares.md` (Markdown source) and `barron_squares.pdf` (compiled via `pandoc --pdf-engine=typst`). The paper is structured as a standard arXiv-style preprint: introduction, preliminaries, order 1, order 2, the 3D cube, and a discussion with open questions.
- **`src/`** — All enumeration and analysis code.
- **`results/`** — Canonical datasets: every known Barron Square of order 1 and order 2, plus summary statistics that match every figure cited in the paper.

## Key results (current state of the paper)

| Object | Result | Method |
|---|---|---|
| Order-1 ($4 \times 4$) Barron Squares | **Exactly 118 exist** | Exhaustive enumeration over $9^4 = 6{,}561$ corner quadruples |
| Order-2 ($8 \times 8$) Barron Squares | **Exactly 1,248 exist** | Exhaustive parallel C search (BOT-derivation) over all $9^4$ top-left corners; ~50 wall-clock hours on 12 cores |
| $4 \times 4 \times 4$ Barron Cubes | **None exist** | Exhaustive over $9^8 = 43{,}046{,}721$ vertex octuplets |
| Order-4 ($16 \times 16$) | None found in $500{,}000$ random trials | Random probe only |

Two new structural theorems for the order-2 case:

- **Theorem 4.1 (Endpoint Pairing).** For every $8 \times 8$ Barron Square and every inner index $r \in \{0,1,2,3\}$, the row-endpoint pair $(L(r), R(r))$ is either equal or reversed relative to the column-endpoint pair $(T(r), B(r))$. The dichotomy holds without exception across all 4,992 observed (square, inner-index) pairs: Case A occurs 2,598 times, Case B 2,394 times, failures zero.
- **Theorem 4.2 (Inner Center Symmetry).** As a corollary of Theorem 4.1, the inner $4 \times 4$ center of every $8 \times 8$ Barron Square is a symmetric matrix. This holds for all 1,248 squares.

Both theorems are currently computationally verified without algebraic proof. Closing that gap is one of the primary items in the roadmap below.

## Repository layout

```
barron-squares/
├── paper/
│   ├── barron_squares.md          Markdown source of the paper
│   └── barron_squares.pdf         Compiled PDF (15 pages)
├── src/
│   ├── barron_core.py             build_matrix, is_valid_barron, display
│   ├── find_4x4.py                Complete order-1 enumeration
│   ├── barron8x8.c                Canonical order-2 enumeration (C, BOT-derivation)
│   ├── find_8x8_fast.py           Python BOT-derivation reference (not practical for full search)
│   ├── find_nxn.py                Random search for k ≥ 3
│   ├── barron_3d.py               4×4×4 Barron Cube enumeration
│   ├── analyze.py                 Statistical analysis shared by all orders
│   ├── collect_results.py         Parse parallel C-worker output into a unified square list
│   └── main.py                    Pipeline runner (4×4 → 8×8 → cube → 16×16)
└── results/
    ├── 4x4_squares.json           All 118 order-1 squares, sorted
    ├── 4x4_summary.json           Matches paper §3
    ├── 8x8_squares.json           All 1,248 order-2 squares, sorted
    ├── 8x8_summary.json           Matches paper §4 and §6
    └── 8x8_raw_output/            Raw barron8x8.c per-worker output and progress logs
```

## Reproducing the results

### Order 1 ($4 \times 4$) — instant

```bash
python src/find_4x4.py
```

Produces all 118 squares in well under a second.

### Order 2 ($8 \times 8$) — several hours to ~50 hours depending on cores

```bash
gcc -O3 -o src/barron8x8 src/barron8x8.c
mkdir -p /tmp/barron8x8_results
for i in {0..11}; do
    START=$((i*546)); END=$(((i+1)*546))
    [ $i -eq 11 ] && END=6561
    ./src/barron8x8 $START $END \
        > /tmp/barron8x8_results/out_$i.txt \
        2> /tmp/barron8x8_results/prog_$i.txt &
done
wait
python src/collect_results.py /tmp/barron8x8_results/out_*.txt --analyze
```

The canonical output is already committed under `results/8x8_squares.json` — you don't need to rerun the search unless you want to independently verify the 1,248 count.

### 3D cube — ~34 minutes

```bash
python src/barron_3d.py
```

Confirms zero $4 \times 4 \times 4$ Barron Cubes.

## Regenerating the PDF

```bash
pandoc paper/barron_squares.md -o paper/barron_squares.pdf \
    --pdf-engine=typst \
    -V papersize=us-letter \
    -V margin-top=1in -V margin-bottom=1in \
    -V margin-left=1in -V margin-right=1in
```

Requires `pandoc` ≥ 3.1 and `typst` installed locally.

## Roadmap: next steps to improve the paper and research

The paper is in reasonable shape as a self-contained preprint, but several concrete additions would meaningfully strengthen it before submission to a peer-reviewed journal. Roughly in decreasing order of impact:

1. **Prove Theorem 4.1 (Endpoint Pairing) algebraically.**
   Currently the theorem's support is "verified without exception across all 4,992 (square, inner-index) pairs." A referee will correctly ask for a proof. Case A is forced in self-transpose squares by $M_{i,j} = M_{j,i}$; the open case is asymmetric squares, where a derivation from the order-2 analogue of the consistency conditions (Corollary 2.2) would explain the dichotomy directly rather than as an experimental regularity. Closing this would upgrade Theorems 4.1 and 4.2 from computational observations to genuine structural theorems.

2. **Independent verification of the 1,248 count.**
   The count is produced by a single implementation (`barron8x8.c`) using the BOT-derivation reduction. An independent reimplementation — ideally a constraint-propagation or SAT/SMT encoding in Python — would corroborate the count without sharing the C search's assumptions. This is already listed as open question #1 in the paper.

3. **Register the counts with OEIS.**
   The sequence of order-$k$ counts — currently known to begin $(118, 1248, \ldots)$ — and the existence-versus-size profile for the 3D cube are natural OEIS entries. Registering them gives the paper an external citation anchor and is a near-zero-cost step with real signaling value.

4. **Engage with the adjacent literature.**
   The paper currently cites a small set of general combinatorics references. A targeted pass through MathSciNet for prior work on digit-pattern enumerations, multiplicative alphametics, cross-figures, and recreational digit puzzles would strengthen the framing and pre-empt standard referee questions. Even 2–4 well-chosen citations would materially change how the paper reads.

5. **Push order $k=3$ (the $12 \times 12$ case) at least partially.**
   The current jump from exhaustive order-2 data to a $5 \times 10^5$ random probe at order 4 leaves a gap. Even a bounded partial count at $k=3$ — or a rigorous non-existence argument — would turn "the family may be going extinct" from speculation into data and would sharpen the cross-order narrative in §6.1.

6. **Algebraic proof (or tighter heuristic) for the absence of $4 \times 4 \times 4$ Barron Cubes.**
   The current heuristic expected count of ~0.25 is suggestive but non-rigorous. A pigeonhole or residue argument on shared vertices and edges — or a clean reduction showing that the three-dimensional consistency system has no digit solutions — would replace exhaustive search with proof and is a natural companion to item 1.

7. **Base dependence and alternative operations.**
   Items 6 and 7 of the open-questions section in the paper (bases other than 10, and replacing multiplication with addition or squaring) are natural follow-on papers rather than additions to this one. They are included here as pointers for future work.

## License and citation

See `paper/barron_squares.md` for the full reference list and author information. The code and data are free to use for research and educational purposes; if you use them in published work, a citation to the paper is appreciated.
