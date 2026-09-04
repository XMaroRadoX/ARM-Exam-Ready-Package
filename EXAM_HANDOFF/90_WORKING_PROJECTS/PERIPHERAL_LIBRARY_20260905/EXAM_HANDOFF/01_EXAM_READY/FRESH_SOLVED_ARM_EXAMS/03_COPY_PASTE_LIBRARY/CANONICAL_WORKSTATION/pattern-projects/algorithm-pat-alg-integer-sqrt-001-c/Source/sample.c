#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Integer square root.
 * Recognition cue: floor square root without floating point.
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
uint32_t algorithm_algorithm_pat_alg_integer_sqrt_001_c(uint32_t n);



static int pattern_core_vector(void) {
  return algorithm_algorithm_pat_alg_integer_sqrt_001_c(0) == 0 &&
         algorithm_algorithm_pat_alg_integer_sqrt_001_c(15) == 3 && algorithm_algorithm_pat_alg_integer_sqrt_001_c(16) == 4;
}
static int pattern_edge_vectors(void) {
  return algorithm_algorithm_pat_alg_integer_sqrt_001_c(1) == 1 &&
         algorithm_algorithm_pat_alg_integer_sqrt_001_c(UINT32_MAX) == 65535u;
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
