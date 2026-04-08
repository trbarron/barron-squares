/*
 * barron8x8.c — Fast 8x8 Barron Square finder in C.
 *
 * Compile:  gcc -O3 -o barron8x8 barron8x8.c
 * Usage:    ./barron8x8 [tl_start tl_end]
 *
 * The search enumerates all valid (TL, TR, col6B, col7B) combinations and for
 * each derives the unique candidate BL and BR via the BOT-derivation algorithm.
 * All 16 corner values (4 per 2x2 block) are in {1,...,9} (nonzero).
 *
 * Algorithm summary (see find_8x8_fast.py for detailed explanation):
 *   Given TL=(a,b,c,d), TR=(e,f,g,h), col6B, col7B:
 *     row6R = 10*(col6B//10) + col7B//10
 *     row7R = 10*(col6B%10) + col7B%10
 *     col6_inner = digits of col6T * col6B
 *     col7_inner = digits of col7T * col7B
 *     RIGHT[ri] = 10*col6_inner[ri] + col7_inner[ri]
 *     TOP[ci] = 10*row0_mid[ci] + row1_mid[ci]   (from TL x TR)
 *   Then for each valid (col0B, col1B):
 *     LEFT[ri] = 10*col0_inner[ri] + col1_inner[ri]
 *     IC[ri][ci] = digit(ci) of LEFT[ri] * RIGHT[ri]
 *     BOT[ci] = from_digits(IC[*][ci]) / TOP[ci]  (must be exact)
 *     row6L = from_digits(BOT[*]//10) / row6R
 *     row7L = from_digits(BOT[*]%10) / row7R
 *     check: 10*(row6L//10)+(row7L//10)==col0B and 10*(row6L%10)+(row7L%10)==col1B
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* -------------------------------------------------------------------------- */
/* Precomputed tables                                                          */
/* -------------------------------------------------------------------------- */

/* PROD4[A][B] = A*B as a packed integer where each byte holds one digit.
   packed = d0<<24 | d1<<16 | d2<<8 | d3  (d0=thousands, d3=units)
   Set to -1 for invalid (non-2-digit-no-zero) inputs. */
static int PROD4[100][100];

/* VALID_R[A] = list of valid B (2-digit no-zero) where A*B is 4-digit no-zero.
   Terminated by 0. */
static int VALID_R[100][100];
static int VALID_R_N[100];  /* count of valid B for each A */

/* VALID_ANY[A] = list of valid B where A*B can have zeros (for inner center).
   These are used when A is a "LEFT" or "RIGHT" value (inner col/row endpoint).
   All B in {11..99} with no-zero digits; A*B can be any 4-digit number.
   Terminated by 0. */
static int VALID_ANY[100][100];
static int VALID_ANY_N[100];

static void init_tables(void) {
    int A, B, p, d0, d1, d2, d3;

    memset(PROD4, -1, sizeof(PROD4));
    memset(VALID_R_N, 0, sizeof(VALID_R_N));
    memset(VALID_ANY_N, 0, sizeof(VALID_ANY_N));

    for (A = 11; A < 100; A++) {
        if (A/10 == 0 || A%10 == 0) continue;
        for (B = 11; B < 100; B++) {
            if (B/10 == 0 || B%10 == 0) continue;
            p = A * B;
            d0 = p / 1000;
            d1 = (p / 100) % 10;
            d2 = (p / 10) % 10;
            d3 = p % 10;
            PROD4[A][B] = (d0 << 24) | (d1 << 16) | (d2 << 8) | d3;

            /* VALID_ANY: B is always valid if A has no zero */
            VALID_ANY[A][VALID_ANY_N[A]++] = B;

            /* VALID_R: product must be 4-digit (d0 >= 1) and all digits nonzero */
            if (d0 >= 1 && d1 >= 1 && d2 >= 1 && d3 >= 1) {
                VALID_R[A][VALID_R_N[A]++] = B;
            }
        }
    }
}

/* -------------------------------------------------------------------------- */
/* Digit extraction from packed product                                        */
/* -------------------------------------------------------------------------- */
#define DIGIT0(p) (((p) >> 24) & 0xFF)
#define DIGIT1(p) (((p) >> 16) & 0xFF)
#define DIGIT2(p) (((p) >>  8) & 0xFF)
#define DIGIT3(p) (((p)      ) & 0xFF)

/* -------------------------------------------------------------------------- */
/* Validity check                                                              */
/* -------------------------------------------------------------------------- */
static int is_valid_2digit_nozero(int x) {
    return (x >= 11 && x <= 99 && x/10 != 0 && x%10 != 0);
}

/* -------------------------------------------------------------------------- */
/* Full 8x8 matrix validation                                                  */
/* -------------------------------------------------------------------------- */
static int validate_8x8(int M[8][8]) {
    int i, j, L, R, mid;
    for (i = 0; i < 8; i++) {
        /* row i */
        L = 10*M[i][0] + M[i][1];
        R = 10*M[i][6] + M[i][7];
        mid = M[i][2]*1000 + M[i][3]*100 + M[i][4]*10 + M[i][5];
        if (L * R != mid) return 0;
        /* no zeros on edges */
        for (j = 0; j < 8; j++) {
            if ((i < 2 || i >= 6 || j < 2 || j >= 6) && M[i][j] == 0) return 0;
        }
    }
    for (j = 0; j < 8; j++) {
        /* col j */
        L = 10*M[0][j] + M[1][j];
        R = 10*M[6][j] + M[7][j];
        mid = M[2][j]*1000 + M[3][j]*100 + M[4][j]*10 + M[5][j];
        if (L * R != mid) return 0;
    }
    return 1;
}

/* -------------------------------------------------------------------------- */
/* Print matrix                                                                */
/* -------------------------------------------------------------------------- */
static void print_matrix(int M[8][8]) {
    int i, j;
    for (i = 0; i < 8; i++) {
        if (i == 2 || i == 6) printf("  ┼────────────────────────┼\n");
        for (j = 0; j < 8; j++) {
            if (j == 2 || j == 6) printf(" │");
            printf(" %d", M[i][j]);
        }
        printf("\n");
    }
}

/* -------------------------------------------------------------------------- */
/* Main search                                                                  */
/* -------------------------------------------------------------------------- */
static long long found_count = 0;
static long long outer_count = 0;
static long long inner_count = 0;

static void search_tl(int a, int b, int c, int d) {
    int row0L = 10*a+b, row1L = 10*c+d;
    int col0T = 10*a+c, col1T = 10*b+d;

    if (VALID_R_N[row0L] == 0 || VALID_R_N[row1L] == 0) return;
    if (VALID_R_N[col0T] == 0 || VALID_R_N[col1T] == 0) return;

    int itr, ibl;
    int e, f, g, h;
    int row0R, row1R;
    int r0m_packed, r1m_packed;
    int TOP[4];
    int col6T, col7T;

    /* Iterate over valid TR */
    for (itr = 0; itr < VALID_R_N[row0L] * VALID_R_N[row1L]; itr++) {
        /* Decompose index */
        int i0 = itr / VALID_R_N[row1L];
        int i1 = itr % VALID_R_N[row1L];
        row0R = VALID_R[row0L][i0];
        row1R = VALID_R[row1L][i1];

        /* Reconstruct TR digits */
        e = row0R / 10; f = row0R % 10;
        g = row1R / 10; h = row1R % 10;

        r0m_packed = PROD4[row0L][row0R];
        r1m_packed = PROD4[row1L][row1R];
        if (r0m_packed < 0 || r1m_packed < 0) continue;

        /* TOP[ci] = 10*row0_mid[ci] + row1_mid[ci] */
        TOP[0] = 10*DIGIT0(r0m_packed) + DIGIT0(r1m_packed);
        TOP[1] = 10*DIGIT1(r0m_packed) + DIGIT1(r1m_packed);
        TOP[2] = 10*DIGIT2(r0m_packed) + DIGIT2(r1m_packed);
        TOP[3] = 10*DIGIT3(r0m_packed) + DIGIT3(r1m_packed);

        if (!is_valid_2digit_nozero(TOP[0]) || !is_valid_2digit_nozero(TOP[1]) ||
            !is_valid_2digit_nozero(TOP[2]) || !is_valid_2digit_nozero(TOP[3])) continue;

        col6T = 10*e + g;
        col7T = 10*f + h;

        if (VALID_R_N[col6T] == 0 || VALID_R_N[col7T] == 0) continue;

        /* Iterate over valid (col6B, col7B) */
        int ic6, ic7;
        for (ic6 = 0; ic6 < VALID_R_N[col6T]; ic6++) {
            int col6B = VALID_R[col6T][ic6];
            int m = col6B / 10, o = col6B % 10;

            for (ic7 = 0; ic7 < VALID_R_N[col7T]; ic7++) {
                int col7B = VALID_R[col7T][ic7];
                outer_count++;

                int n = col7B / 10, p = col7B % 10;
                int row6R = 10*m + n;
                int row7R = 10*o + p;

                if (!is_valid_2digit_nozero(row6R) || !is_valid_2digit_nozero(row7R)) continue;

                int c6i_packed = PROD4[col6T][col6B];
                int c7i_packed = PROD4[col7T][col7B];
                if (c6i_packed < 0 || c7i_packed < 0) continue;
                if (DIGIT0(c6i_packed)==0 || DIGIT1(c6i_packed)==0 ||
                    DIGIT2(c6i_packed)==0 || DIGIT3(c6i_packed)==0) continue;
                if (DIGIT0(c7i_packed)==0 || DIGIT1(c7i_packed)==0 ||
                    DIGIT2(c7i_packed)==0 || DIGIT3(c7i_packed)==0) continue;

                int RIGHT[4];
                RIGHT[0] = 10*DIGIT0(c6i_packed) + DIGIT0(c7i_packed);
                RIGHT[1] = 10*DIGIT1(c6i_packed) + DIGIT1(c7i_packed);
                RIGHT[2] = 10*DIGIT2(c6i_packed) + DIGIT2(c7i_packed);
                RIGHT[3] = 10*DIGIT3(c6i_packed) + DIGIT3(c7i_packed);

                if (!is_valid_2digit_nozero(RIGHT[0]) || !is_valid_2digit_nozero(RIGHT[1]) ||
                    !is_valid_2digit_nozero(RIGHT[2]) || !is_valid_2digit_nozero(RIGHT[3])) continue;

                /* Inner loop over valid (col0B, col1B) */
                for (ibl = 0; ibl < VALID_R_N[col0T] * VALID_R_N[col1T]; ibl++) {
                    int i2 = ibl / VALID_R_N[col1T];
                    int i3 = ibl % VALID_R_N[col1T];
                    int col0B = VALID_R[col0T][i2];
                    int col1B = VALID_R[col1T][i3];

                    inner_count++;

                    int c0i_packed = PROD4[col0T][col0B];
                    int c1i_packed = PROD4[col1T][col1B];
                    if (c0i_packed < 0 || c1i_packed < 0) continue;
                    if (DIGIT0(c0i_packed)==0 || DIGIT1(c0i_packed)==0 ||
                        DIGIT2(c0i_packed)==0 || DIGIT3(c0i_packed)==0) continue;
                    if (DIGIT0(c1i_packed)==0 || DIGIT1(c1i_packed)==0 ||
                        DIGIT2(c1i_packed)==0 || DIGIT3(c1i_packed)==0) continue;

                    int LEFT[4];
                    LEFT[0] = 10*DIGIT0(c0i_packed) + DIGIT0(c1i_packed);
                    LEFT[1] = 10*DIGIT1(c0i_packed) + DIGIT1(c1i_packed);
                    LEFT[2] = 10*DIGIT2(c0i_packed) + DIGIT2(c1i_packed);
                    LEFT[3] = 10*DIGIT3(c0i_packed) + DIGIT3(c1i_packed);

                    if (!is_valid_2digit_nozero(LEFT[0]) || !is_valid_2digit_nozero(LEFT[1]) ||
                        !is_valid_2digit_nozero(LEFT[2]) || !is_valid_2digit_nozero(LEFT[3])) continue;

                    /* Compute IC from LEFT x RIGHT */
                    int row_prods[4];
                    row_prods[0] = LEFT[0] * RIGHT[0];
                    row_prods[1] = LEFT[1] * RIGHT[1];
                    row_prods[2] = LEFT[2] * RIGHT[2];
                    row_prods[3] = LEFT[3] * RIGHT[3];

                    /* N_col[ci] = from_digits(IC[*][ci]) */
                    /* IC[ri][ci] = digit(ci) of row_prods[ri] */
                    /* N_col[0] = thousands of row_prods[*] */
                    int N0 = (row_prods[0]/1000)*1000 + (row_prods[1]/1000)*100 +
                             (row_prods[2]/1000)*10   + (row_prods[3]/1000);
                    if (N0 % TOP[0] != 0) continue;
                    int B0 = N0 / TOP[0];
                    if (!is_valid_2digit_nozero(B0)) continue;

                    int N1 = ((row_prods[0]/100)%10)*1000 + ((row_prods[1]/100)%10)*100 +
                             ((row_prods[2]/100)%10)*10   + ((row_prods[3]/100)%10);
                    if (N1 % TOP[1] != 0) continue;
                    int B1 = N1 / TOP[1];
                    if (!is_valid_2digit_nozero(B1)) continue;

                    int N2 = ((row_prods[0]/10)%10)*1000 + ((row_prods[1]/10)%10)*100 +
                             ((row_prods[2]/10)%10)*10   + ((row_prods[3]/10)%10);
                    if (N2 % TOP[2] != 0) continue;
                    int B2 = N2 / TOP[2];
                    if (!is_valid_2digit_nozero(B2)) continue;

                    int N3 = (row_prods[0]%10)*1000 + (row_prods[1]%10)*100 +
                             (row_prods[2]%10)*10   + (row_prods[3]%10);
                    if (N3 % TOP[3] != 0) continue;
                    int B3 = N3 / TOP[3];
                    if (!is_valid_2digit_nozero(B3)) continue;

                    /* row6_mid = [B0//10, B1//10, B2//10, B3//10] */
                    /* row7_mid = [B0%10, B1%10, B2%10, B3%10]   */
                    int r6m0=B0/10, r6m1=B1/10, r6m2=B2/10, r6m3=B3/10;
                    int r7m0=B0%10, r7m1=B1%10, r7m2=B2%10, r7m3=B3%10;

                    if (r6m0==0||r6m1==0||r6m2==0||r6m3==0) continue;
                    if (r7m0==0||r7m1==0||r7m2==0||r7m3==0) continue;

                    int N_row6 = r6m0*1000 + r6m1*100 + r6m2*10 + r6m3;
                    int N_row7 = r7m0*1000 + r7m1*100 + r7m2*10 + r7m3;

                    if (N_row6 % row6R != 0) continue;
                    int row6L = N_row6 / row6R;
                    if (!is_valid_2digit_nozero(row6L)) continue;

                    if (N_row7 % row7R != 0) continue;
                    int row7L = N_row7 / row7R;
                    if (!is_valid_2digit_nozero(row7L)) continue;

                    /* Check BL consistency */
                    if (10*(row6L/10) + (row7L/10) != col0B) continue;
                    if (10*(row6L%10) + (row7L%10) != col1B) continue;

                    /* FOUND A VALID SQUARE! Build and print it. */
                    found_count++;

                    /* Reconstruct full 8x8 matrix */
                    int M[8][8] = {{0}};

                    /* Corner blocks */
                    M[0][0]=a; M[0][1]=b; M[1][0]=c; M[1][1]=d;            /* TL */
                    M[0][6]=e; M[0][7]=f; M[1][6]=g; M[1][7]=h;            /* TR */
                    M[6][0]=row6L/10; M[6][1]=row6L%10;                     /* BL */
                    M[7][0]=row7L/10; M[7][1]=row7L%10;
                    M[6][6]=m; M[6][7]=n; M[7][6]=o; M[7][7]=p;            /* BR */

                    /* Edge rows */
                    int ri;
                    M[0][2]=DIGIT0(r0m_packed); M[0][3]=DIGIT1(r0m_packed);
                    M[0][4]=DIGIT2(r0m_packed); M[0][5]=DIGIT3(r0m_packed);
                    M[1][2]=DIGIT0(r1m_packed); M[1][3]=DIGIT1(r1m_packed);
                    M[1][4]=DIGIT2(r1m_packed); M[1][5]=DIGIT3(r1m_packed);

                    int r6m_packed = PROD4[10*(M[6][0])+M[6][1]][row6R];
                    int r7m_packed = PROD4[10*(M[7][0])+M[7][1]][row7R];
                    M[6][2]=DIGIT0(r6m_packed); M[6][3]=DIGIT1(r6m_packed);
                    M[6][4]=DIGIT2(r6m_packed); M[6][5]=DIGIT3(r6m_packed);
                    M[7][2]=DIGIT0(r7m_packed); M[7][3]=DIGIT1(r7m_packed);
                    M[7][4]=DIGIT2(r7m_packed); M[7][5]=DIGIT3(r7m_packed);

                    /* Edge cols */
                    for (ri = 0; ri < 4; ri++) {
                        M[2+ri][0] = DIGIT0(c0i_packed + (ri<<24)); /* wrong, need proper indexing */
                    }
                    /* Actually let me just use the packed values directly */
                    M[2][0]=DIGIT0(c0i_packed); M[3][0]=DIGIT1(c0i_packed);
                    M[4][0]=DIGIT2(c0i_packed); M[5][0]=DIGIT3(c0i_packed);
                    M[2][1]=DIGIT0(c1i_packed); M[3][1]=DIGIT1(c1i_packed);
                    M[4][1]=DIGIT2(c1i_packed); M[5][1]=DIGIT3(c1i_packed);
                    M[2][6]=DIGIT0(c6i_packed); M[3][6]=DIGIT1(c6i_packed);
                    M[4][6]=DIGIT2(c6i_packed); M[5][6]=DIGIT3(c6i_packed);
                    M[2][7]=DIGIT0(c7i_packed); M[3][7]=DIGIT1(c7i_packed);
                    M[4][7]=DIGIT2(c7i_packed); M[5][7]=DIGIT3(c7i_packed);

                    /* Inner center from rows */
                    for (ri = 0; ri < 4; ri++) {
                        int rp = row_prods[ri];
                        M[2+ri][2] = rp/1000;
                        M[2+ri][3] = (rp/100)%10;
                        M[2+ri][4] = (rp/10)%10;
                        M[2+ri][5] = rp%10;
                    }

                    /* Validate */
                    if (!validate_8x8(M)) {
                        fprintf(stderr, "VALIDATION FAILED for square #%lld!\n", found_count);
                        continue;
                    }

                    printf("# Square %lld  (outer=%lld, inner=%lld)\n",
                           found_count, outer_count, inner_count);
                    printf("TL=(%d,%d,%d,%d) TR=(%d,%d,%d,%d) BL=(%d,%d,%d,%d) BR=(%d,%d,%d,%d)\n",
                           a,b,c,d, e,f,g,h,
                           row6L/10,row6L%10,row7L/10,row7L%10,
                           m,n,o,p);
                    print_matrix(M);
                    printf("\n");
                    fflush(stdout);
                }
            }
        }
    }
}

int main(int argc, char *argv[]) {
    init_tables();

    int tl_start = 0, tl_end = 6561;
    if (argc >= 3) {
        tl_start = atoi(argv[1]);
        tl_end   = atoi(argv[2]);
    }

    printf("# Searching TL indices [%d, %d)\n", tl_start, tl_end);
    fflush(stdout);

    time_t t0 = time(NULL);

    int idx = 0;
    int a, b, c, d;
    for (a = 1; a <= 9; a++) {
        for (b = 1; b <= 9; b++) {
            for (c = 1; c <= 9; c++) {
                for (d = 1; d <= 9; d++, idx++) {
                    if (idx < tl_start || idx >= tl_end) continue;
                    search_tl(a, b, c, d);

                    if (idx % 100 == 99) {
                        time_t now = time(NULL);
                        fprintf(stderr, "TL[%d]  elapsed=%lds  outer=%lldM  inner=%lldM  found=%lld\n",
                                idx, (long)(now-t0),
                                outer_count/1000000, inner_count/1000000,
                                found_count);
                        fflush(stderr);
                    }
                }
            }
        }
    }

    printf("# DONE: found=%lld  outer=%lld  inner=%lld  time=%lds\n",
           found_count, outer_count, inner_count, (long)(time(NULL)-t0));
    return 0;
}
