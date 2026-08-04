/*
 * FSOT thin C parity — pack / collapse θ only.
 * Not theory authority (that is Lean + fsot_compute). Portable evidence that
 * trinary packing on binary hosts matches golden multiprover values.
 *
 * Build: gcc -O2 -std=c11 fsot_pack_parity.c -o fsot_pack_parity -lm
 */
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

/* Archive seeds (vendor/fsot_compute) */
static const double C_EFF = 0.9577022026205613;
static const double P_VAR = 0.9579871226722757;
static const double COLLAPSE_THETA = C_EFF * P_VAR; /* 0.9174663774653723 */
static const double COHERENCE_GATE = 0.5;
static const uint64_t GOLDEN_PACK_WORD = 5270498306774157604ULL;

static int collapse_trit(double x) {
    if (x > COLLAPSE_THETA) return 1;
    if (x < -COLLAPSE_THETA) return -1;
    return 0;
}

static uint64_t pack_trits32(const uint8_t codes[32]) {
    uint64_t word = 0;
    for (int i = 0; i < 32; i++) {
        uint64_t c = (uint64_t)(codes[i] % 3u);
        word |= c << (2 * i);
    }
    return word;
}

static void unpack_trits32(uint64_t word, uint8_t codes[32]) {
    for (int i = 0; i < 32; i++) {
        codes[i] = (uint8_t)((word >> (2 * i)) & 0x3u);
    }
}

int main(void) {
    uint8_t codes[32];
    uint8_t back[32];
    int i;
    int pack_ok = 1;
    int theta_ok;
    int collapse_ok = 1;
    uint64_t word;

    for (i = 0; i < 32; i++) {
        codes[i] = (uint8_t)(i % 3);
    }
    word = pack_trits32(codes);
    unpack_trits32(word, back);
    for (i = 0; i < 32; i++) {
        if (back[i] != codes[i]) pack_ok = 0;
    }

    theta_ok = (fabs(COLLAPSE_THETA - 0.9174663774653723) < 1e-12);
    /* collapse spot checks */
    if (collapse_trit(2.0) != 1) collapse_ok = 0;
    if (collapse_trit(-2.0) != -1) collapse_ok = 0;
    if (collapse_trit(0.0) != 0) collapse_ok = 0;
    if (collapse_trit(COLLAPSE_THETA + 0.01) != 1) collapse_ok = 0;

    printf("FSOT_C_COLLAPSE_THETA=%.17g\n", COLLAPSE_THETA);
    printf("FSOT_C_C_EFF=%.17g\n", C_EFF);
    printf("FSOT_C_P_VAR=%.17g\n", P_VAR);
    printf("FSOT_C_COHERENCE_GATE=%.17g\n", COHERENCE_GATE);
    printf("FSOT_C_STATES_PER_U64=%d\n", 64 / 2);
    printf("FSOT_C_PACK_WORD=%llu\n", (unsigned long long)word);
    printf("FSOT_C_GOLDEN_WORD=%llu\n", (unsigned long long)GOLDEN_PACK_WORD);
    printf("FSOT_C_PACK_MATCH=%d\n", word == GOLDEN_PACK_WORD ? 1 : 0);
    printf("FSOT_C_ROUNDTRIP=%d\n", pack_ok);
    printf("FSOT_C_THETA_OK=%d\n", theta_ok);
    printf("FSOT_C_COLLAPSE_OK=%d\n", collapse_ok);

    if (pack_ok && theta_ok && collapse_ok && word == GOLDEN_PACK_WORD) {
        printf("FSOT_C_OVERALL=ok\n");
        return 0;
    }
    printf("FSOT_C_OVERALL=fail\n");
    return 1;
}
