/* Adversarial — use-after-free / double-free motif. */
#include <stdlib.h>

void adv_double_free(char *p) {
    if (p) {
        free(p);
        free(p);
    }
    void *q = malloc(64);
    if (q) free(q);
}