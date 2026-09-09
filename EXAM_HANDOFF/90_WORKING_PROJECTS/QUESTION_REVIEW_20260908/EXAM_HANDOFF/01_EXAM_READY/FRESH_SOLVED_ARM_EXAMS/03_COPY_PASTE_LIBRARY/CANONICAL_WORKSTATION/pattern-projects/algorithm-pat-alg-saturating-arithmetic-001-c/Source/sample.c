#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Clamp absolute saturation and overflow.
 * Recognition cue: clamp signed arithmetic without overflow.
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

int32_t algorithm_algorithm_pat_alg_saturating_arithmetic_001_c(int64_t value, int32_t minimum,
                                          int32_t maximum);

uint32_t algorithm_algorithm_pat_alg_saturating_arithmetic_001_c_abs_i32(int32_t value);

int32_t algorithm_algorithm_pat_alg_saturating_arithmetic_001_c_add_i32(int32_t first,
                                                  int32_t second);



static int pattern_core_vector(void) {
  return algorithm_algorithm_pat_alg_saturating_arithmetic_001_c(50, 0, 10) == 10 &&
         algorithm_algorithm_pat_alg_saturating_arithmetic_001_c(-2, 0, 10) == 0;
}
static int pattern_edge_vectors(void) {
  return algorithm_algorithm_pat_alg_saturating_arithmetic_001_c(5, 10, 0) == 10 &&
         algorithm_algorithm_pat_alg_saturating_arithmetic_001_c_abs_i32(INT32_MIN) ==
             UINT32_C(2147483648) &&
         algorithm_algorithm_pat_alg_saturating_arithmetic_001_c_add_i32(INT32_MAX, 1) == INT32_MAX &&
         algorithm_algorithm_pat_alg_saturating_arithmetic_001_c_add_i32(INT32_MIN, -1) == INT32_MIN;
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
