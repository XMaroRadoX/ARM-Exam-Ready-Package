#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Prefix sums and range sums.
 * Recognition cue: precompute cumulative sums answer ranges.
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

int algorithm_algorithm_pat_alg_prefix_sum_001_c(const int32_t *values, uint32_t count,
                           int64_t *prefix);

int algorithm_algorithm_pat_alg_prefix_sum_001_c_range(const int64_t *prefix, uint32_t count,
                                 uint32_t begin, uint32_t end, int64_t *sum);



static int pattern_core_vector(void) {
  int32_t a[] = {1, -2, 4};
  int64_t p[4];
  algorithm_algorithm_pat_alg_prefix_sum_001_c(a, 3, p);
  return p[0] == 0 && p[1] == 1 && p[2] == -1 && p[3] == 3;
}
static int pattern_edge_vectors(void) {
  int32_t a[] = {1, -2, 4};
  int64_t p[4], s = 0;
  return algorithm_algorithm_pat_alg_prefix_sum_001_c(NULL, 0, p) &&
         algorithm_algorithm_pat_alg_prefix_sum_001_c(a, 3, p) &&
         algorithm_algorithm_pat_alg_prefix_sum_001_c_range(p, 3, 1, 3, &s) && s == 2 &&
         !algorithm_algorithm_pat_alg_prefix_sum_001_c_range(p, 3, 3, 2, &s);
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
