/* Recommended exam template: C calls an AAPCS assembly routine. */
#include "asm_sum.h"

uint32_t call_assembly_example(void) {
    static const uint32_t values[] = {3u, 5u, 7u, 11u};
    return asm_sum_words(values, 4u);
}
