#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Longest increasing subsequence.
 * Recognition cue: longest strictly increasing subsequence.
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
uint32_t algorithm_algorithm_pat_alg_lis_001_assembly(const int32_t *a, uint32_t n, uint32_t *dp);



static int pattern_core_vector(void) {
  int32_t a[] = {3, 1, 2, 5};
  uint32_t d[4];
  return algorithm_algorithm_pat_alg_lis_001_assembly(a, 4, d) == 3;
}
static int pattern_edge_vectors(void) {
  int32_t a[] = {2, 2, 2};
  uint32_t d[3];
  return algorithm_algorithm_pat_alg_lis_001_assembly(a, 0, d) == 0 && algorithm_algorithm_pat_alg_lis_001_assembly(a, 3, d) == 1;
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
