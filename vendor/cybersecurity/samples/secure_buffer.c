/* FSOT code-genome sample — bounded buffer (secure pattern). */
#include <string.h>
#include <stddef.h>

int fsot_copy_bounded(char *dst, size_t dst_sz, const char *src) {
    if (!dst || !src || dst_sz == 0) return -1;
    size_t n = 0;
    while (src[n] && n + 1 < dst_sz) {
        dst[n] = src[n];
        n++;
    }
    dst[n] = '\0';
    return (int)n;
}