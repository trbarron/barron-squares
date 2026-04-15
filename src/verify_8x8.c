/*
 * verify_8x8.c — Independent exhaustive enumeration of 8×8 Barron Squares.
 *
 * This is a VERIFICATION implementation, structurally independent of
 * barron8x8.c. It uses a different search decomposition to confirm
 * the count of 1,248 order-2 Barron Squares.
 *
 * Algorithm: Full Corner Derivation (FCD)
 *   Free variables: TL (4 digits), TR (4 digits), BL (4 digits)  [= 12 free]
 *   Derived:        BR from edge row/col constraints, inner block from consistency
 *
 * This differs from barron8x8.c's BOT-derivation, which uses:
 *   Free variables: TL (4), TR (4), col4_B (2), col5_B (2)       [= 12 free]
 *   Derived:        BL, BR, inner block via bottom-of-table chain
 *
 * The two implementations share no code and use different derivation
 * strategies, so agreement on the count constitutes independent verification.
 *
 * Compile:  gcc -O3 -o src/verify_8x8 src/verify_8x8.c
 * Run (single core, ~30h):
 *           ./src/verify_8x8
 * Run (12 parallel workers, ~3h wall):
 *           mkdir -p /tmp/verify_8x8
 *           for i in $(seq 0 11); do
 *             S=$((i*547)); E=$(((i+1)*547));
 *             [ $i -eq 11 ] && E=6561;
 *             ./src/verify_8x8 $S $E > /tmp/verify_8x8/out_$i.txt 2>/dev/null &
 *           done
 *           wait
 *           grep "^FOUND:" /tmp/verify_8x8/out_*.txt | \
 *             awk -F: '{s+=$NF} END {print "Total:", s}'
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* ------------------------------------------------------------------ */
/* Pre-computed tables                                                 */
/* ------------------------------------------------------------------ */

/*
 * edge_valid[L][R] = 1 iff L*R is in [1000,9999] with all 4 digits nonzero,
 *                    AND both L and R have nonzero digits.
 * edge_prod[L][R][0..3] = the 4 digits of L*R when edge_valid.
 */
static int edge_valid[100][100];
static int edge_prod[100][100][4];

/* For each L, sorted list of valid R values for edge constraints. */
static int edge_R_list[100][90];
static int edge_R_count[100];

static void precompute_tables(void) {
    memset(edge_valid, 0, sizeof(edge_valid));
    memset(edge_R_count, 0, sizeof(edge_R_count));

    for (int L = 11; L <= 99; L++) {
        if (L % 10 == 0) continue;
        for (int R = 11; R <= 99; R++) {
            if (R % 10 == 0) continue;
            int p = L * R;
            if (p < 1000 || p > 9999) continue;
            int d0 = p / 1000;
            int d1 = (p / 100) % 10;
            int d2 = (p / 10) % 10;
            int d3 = p % 10;
            if (d0 == 0 || d1 == 0 || d2 == 0 || d3 == 0) continue;

            edge_valid[L][R] = 1;
            edge_prod[L][R][0] = d0;
            edge_prod[L][R][1] = d1;
            edge_prod[L][R][2] = d2;
            edge_prod[L][R][3] = d3;
            edge_R_list[L][edge_R_count[L]++] = R;
        }
    }
}

/* ------------------------------------------------------------------ */
/* Inner-block consistency check with early exit                       */
/* ------------------------------------------------------------------ */

/*
 * Check that the 4×4 inner center derived from row products matches
 * the one derived from column products. Returns 1 if consistent.
 *
 * Row derivation: for inner row r, product = L_r * R_r → 4 digits
 * Col derivation: for inner col c, product = T_c * B_c → 4 digits
 * Cell (r,c) must agree: row_digit[r][c-2] == col_digit[c][r-2]
 *
 * Uses early-exit: check one product at a time, bail on first mismatch.
 */
static inline int check_inner_consistency(
    int L2, int R2, int L3, int R3, int L4, int R4, int L5, int R5,
    int T2, int B2, int T3, int B3, int T4, int B4, int T5, int B5)
{
    /* Compute all 8 products */
    int pr2 = L2 * R2, pr3 = L3 * R3, pr4 = L4 * R4, pr5 = L5 * R5;
    int pc2 = T2 * B2, pc3 = T3 * B3, pc4 = T4 * B4, pc5 = T5 * B5;

    if (pr2 > 9999 || pr3 > 9999 || pr4 > 9999 || pr5 > 9999) return 0;
    if (pc2 > 9999 || pc3 > 9999 || pc4 > 9999 || pc5 > 9999) return 0;

    /* Extract row digits: row_d[r][c] where r=0..3, c=0..3 */
    /* Row r gives digits of pr{r+2} */
    int rd[4][4];
    rd[0][0] = pr2/1000; rd[0][1] = (pr2/100)%10; rd[0][2] = (pr2/10)%10; rd[0][3] = pr2%10;
    rd[1][0] = pr3/1000; rd[1][1] = (pr3/100)%10; rd[1][2] = (pr3/10)%10; rd[1][3] = pr3%10;
    rd[2][0] = pr4/1000; rd[2][1] = (pr4/100)%10; rd[2][2] = (pr4/10)%10; rd[2][3] = pr4%10;
    rd[3][0] = pr5/1000; rd[3][1] = (pr5/100)%10; rd[3][2] = (pr5/10)%10; rd[3][3] = pr5%10;

    /* Check column by column with early exit */
    /* Col 2 (c=0): digits of pc2 should match rd[0..3][0] */
    if (rd[0][0] != pc2/1000) return 0;
    if (rd[1][0] != (pc2/100)%10) return 0;
    if (rd[2][0] != (pc2/10)%10) return 0;
    if (rd[3][0] != pc2%10) return 0;

    /* Col 3 */
    if (rd[0][1] != pc3/1000) return 0;
    if (rd[1][1] != (pc3/100)%10) return 0;
    if (rd[2][1] != (pc3/10)%10) return 0;
    if (rd[3][1] != pc3%10) return 0;

    /* Col 4 */
    if (rd[0][2] != pc4/1000) return 0;
    if (rd[1][2] != (pc4/100)%10) return 0;
    if (rd[2][2] != (pc4/10)%10) return 0;
    if (rd[3][2] != pc4%10) return 0;

    /* Col 5 */
    if (rd[0][3] != pc5/1000) return 0;
    if (rd[1][3] != (pc5/100)%10) return 0;
    if (rd[2][3] != (pc5/10)%10) return 0;
    if (rd[3][3] != pc5%10) return 0;

    return 1;
}

/* ------------------------------------------------------------------ */
/* Main search                                                         */
/* ------------------------------------------------------------------ */

int main(int argc, char **argv) {
    int tl_start = 0, tl_end = 6561;

    if (argc >= 3) {
        tl_start = atoi(argv[1]);
        tl_end   = atoi(argv[2]);
    }

    fprintf(stderr, "verify_8x8: Independent 8x8 Barron Square enumeration\n");
    fprintf(stderr, "Algorithm: Full Corner Derivation (TL -> TR -> BL -> derive BR)\n");
    fprintf(stderr, "TL range: [%d, %d) of 6561\n\n", tl_start, tl_end);

    precompute_tables();

    int total_edge_pairs = 0;
    for (int L = 11; L <= 99; L++)
        if (L % 10 != 0)
            total_edge_pairs += edge_R_count[L];
    fprintf(stderr, "Pre-computed %d valid edge (L,R) pairs.\n", total_edge_pairs);

    clock_t t_start_cpu = clock();
    time_t  t_start_wall = time(NULL);

    long long total_found = 0;
    int tl_idx = 0;

    for (int a = 1; a <= 9; a++)
    for (int b = 1; b <= 9; b++) {
        int L0 = 10*a + b;
        if (edge_R_count[L0] == 0) { tl_idx += 81; continue; }

        for (int c = 1; c <= 9; c++) {
            int T0 = 10*a + c;
            if (edge_R_count[T0] == 0) { tl_idx += 9; continue; }

            for (int d = 1; d <= 9; d++) {
                /* Skip TL values outside our assigned range */
                if (tl_idx < tl_start || tl_idx >= tl_end) {
                    tl_idx++;
                    continue;
                }
                tl_idx++;

                int L1 = 10*c + d;
                int T1 = 10*b + d;

                if (edge_R_count[L1] == 0) continue;
                if (edge_R_count[T1] == 0) continue;

                /* Iterate valid TR (from rows 0,1 edge constraints) */
                for (int ir0 = 0; ir0 < edge_R_count[L0]; ir0++) {
                    int R0 = edge_R_list[L0][ir0];
                    int e = R0 / 10, f = R0 % 10;
                    int *row0 = edge_prod[L0][R0];

                    for (int ir1 = 0; ir1 < edge_R_count[L1]; ir1++) {
                        int R1 = edge_R_list[L1][ir1];
                        int g = R1 / 10, h = R1 % 10;
                        int *row1 = edge_prod[L1][R1];

                        int T6 = 10*e + g;
                        int T7 = 10*f + h;

                        /* Skip if no valid bottom endpoints for cols 6 or 7 */
                        if (edge_R_count[T6] == 0 || edge_R_count[T7] == 0)
                            continue;

                        /* Inner col top endpoints (from row 0,1 interiors) */
                        int T2 = 10*row0[0] + row1[0];
                        int T3 = 10*row0[1] + row1[1];
                        int T4 = 10*row0[2] + row1[2];
                        int T5 = 10*row0[3] + row1[3];

                        /* Iterate valid BL (from cols 0,1 edge constraints) */
                        for (int ib0 = 0; ib0 < edge_R_count[T0]; ib0++) {
                            int B0 = edge_R_list[T0][ib0];
                            int *col0 = edge_prod[T0][B0];
                            int bi = B0 / 10, bk = B0 % 10;

                            for (int ib1 = 0; ib1 < edge_R_count[T1]; ib1++) {
                                int B1 = edge_R_list[T1][ib1];
                                int *col1 = edge_prod[T1][B1];
                                int bj = B1 / 10, bl_ = B1 % 10;

                                int left6 = 10*bi + bj;
                                int left7 = 10*bk + bl_;

                                if (edge_R_count[left6] == 0 || edge_R_count[left7] == 0)
                                    continue;

                                /* Inner row left endpoints (from col 0,1 interiors) */
                                int L2 = 10*col0[0] + col1[0];
                                int L3 = 10*col0[1] + col1[1];
                                int L4 = 10*col0[2] + col1[2];
                                int L5 = 10*col0[3] + col1[3];

                                /* Derive BR from 4 edge constraints */
                                for (int br00 = 1; br00 <= 9; br00++) {
                                    for (int br01 = 1; br01 <= 9; br01++) {
                                        int right6 = 10*br00 + br01;
                                        if (!edge_valid[left6][right6]) continue;

                                        for (int br10 = 1; br10 <= 9; br10++) {
                                            int bottom6 = 10*br00 + br10;
                                            if (!edge_valid[T6][bottom6]) continue;

                                            for (int br11 = 1; br11 <= 9; br11++) {
                                                int right7 = 10*br10 + br11;
                                                if (!edge_valid[left7][right7]) continue;

                                                int bottom7 = 10*br01 + br11;
                                                if (!edge_valid[T7][bottom7]) continue;

                                                /* BR passes all 4 edge checks.
                                                 * Derive inner endpoints and check consistency. */
                                                int *c6 = edge_prod[T6][bottom6];
                                                int *c7 = edge_prod[T7][bottom7];
                                                int *r6 = edge_prod[left6][right6];
                                                int *r7 = edge_prod[left7][right7];

                                                /* Check cols 6,7 interior digits nonzero (edge) */
                                                if (c6[0]==0||c7[0]==0||c6[1]==0||c7[1]==0||
                                                    c6[2]==0||c7[2]==0||c6[3]==0||c7[3]==0)
                                                    continue;
                                                /* Check rows 6,7 interior digits nonzero (edge) */
                                                if (r6[0]==0||r7[0]==0||r6[1]==0||r7[1]==0||
                                                    r6[2]==0||r7[2]==0||r6[3]==0||r7[3]==0)
                                                    continue;

                                                /* Inner row right endpoints */
                                                int R2 = 10*c6[0]+c7[0];
                                                int R3 = 10*c6[1]+c7[1];
                                                int R4 = 10*c6[2]+c7[2];
                                                int R5 = 10*c6[3]+c7[3];

                                                /* Inner col bottom endpoints */
                                                int B2 = 10*r6[0]+r7[0];
                                                int B3 = 10*r6[1]+r7[1];
                                                int B4 = 10*r6[2]+r7[2];
                                                int B5 = 10*r6[3]+r7[3];

                                                if (check_inner_consistency(
                                                        L2,R2,L3,R3,L4,R4,L5,R5,
                                                        T2,B2,T3,B3,T4,B4,T5,B5))
                                                {
                                                    total_found++;
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

                /* Progress every 100 TL values */
                if ((tl_idx - tl_start) % 100 == 0 && tl_idx > tl_start) {
                    double elapsed = difftime(time(NULL), t_start_wall);
                    int done = tl_idx - tl_start;
                    int total = tl_end - tl_start;
                    double pct = 100.0 * done / total;
                    fprintf(stderr, "  TL %d/%d (%.1f%%), found %lld, %.0fs elapsed\n",
                            done, total, pct, total_found, elapsed);
                }
            }
        }
    }

    double cpu_secs = (double)(clock() - t_start_cpu) / CLOCKS_PER_SEC;
    double wall_secs = difftime(time(NULL), t_start_wall);

    printf("FOUND:%lld\n", total_found);
    fprintf(stderr, "\n========================================\n");
    fprintf(stderr, "TL range: [%d, %d)\n", tl_start, tl_end);
    fprintf(stderr, "Squares found: %lld\n", total_found);
    fprintf(stderr, "CPU time:  %.1f seconds (%.2f hours)\n", cpu_secs, cpu_secs/3600);
    fprintf(stderr, "Wall time: %.0f seconds (%.2f hours)\n", wall_secs, wall_secs/3600);
    fprintf(stderr, "========================================\n");

    return 0;
}
