/* FSOT code-genome sample — legacy unsafe pattern (hole detection target). */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char *fsot_legacy_dup(const char *input) {
    char *buf = (char *)malloc(64);
    if (!buf) return NULL;
    strcpy(buf, input);
    return buf;
}

void fsot_legacy_echo(const char *msg) {
    char stack[32];
    sprintf(stack, "echo:%s", msg);
    puts(stack);
}