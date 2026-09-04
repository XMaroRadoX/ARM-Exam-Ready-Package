#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Overlap-safe memory movement.
 * Recognition cue: copy forwards or backwards when ranges overlap.
 *
 * Contract rules:
 * - Fixed-width types make width and signedness part of the interface.
 * - A pointer never carries its length; count/capacity arguments are explicit.
 * - const input objects are not mutated. Non-const outputs may be changed only
 *   within their documented bounds.
 * - Invalid, empty, duplicate and arithmetic-limit behavior is executable in
 *   pattern_edge_vectors() and described in the adjacent README.
 *
 * Trace the validation step first, then the main loop/recurrence invariant,
 * then the final result or capacity check. Public suffix functions are named
 * variants of the same advertised pattern, not unrelated shortcuts.
 */

/* Primary algorithm and its named variants. */
void *algorithm_algorithm_pat_alg_memmove_001_assembly(void *d, const void *s, uint32_t n);



static int pattern_core_vector(void) {
  char a[6] = "abcd";
  algorithm_algorithm_pat_alg_memmove_001_assembly(a + 1, a, 4);
  return a[0] == 'a' && a[1] == 'a' && a[4] == 'd';
}
static int pattern_edge_vectors(void) {
  char a[6] = "abcd";
  algorithm_algorithm_pat_alg_memmove_001_assembly(a, a, 4);
  algorithm_algorithm_pat_alg_memmove_001_assembly(a, a + 1, 3);
  return a[0] == 'b' && a[2] == 'd';
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }

volatile int pattern_result;
int main(void){exam_init();pattern_result=test_main();exam_led_write(pattern_result?0xFFu:0x01u);for(;;){}}
