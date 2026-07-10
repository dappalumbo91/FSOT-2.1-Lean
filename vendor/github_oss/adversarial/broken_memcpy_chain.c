/* Adversarial — chained unsafe C patterns for codon-hole stress test. */
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

void adv_copy_loop(const char *src) {
    char *buf = (char *)malloc(32);
    if (!buf) return;
    strcpy(buf, src);
    char stack[16];
    sprintf(stack, "tag:%s", buf);
    memcpy(buf, stack, sizeof(stack));
    free(buf);
}