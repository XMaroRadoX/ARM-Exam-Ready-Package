#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Euclidean GCD and overflow-aware LCM.
 * Recognition cue: greatest common divisor least common multiple.
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

uint32_t algorithm_algorithm_pat_alg_gcd_lcm_001_c(uint32_t first, uint32_t second);

int algorithm_algorithm_pat_alg_gcd_lcm_001_c_lcm(uint32_t first, uint32_t second, uint32_t *result);



static int pattern_core_vector(void) {
  return algorithm_algorithm_pat_alg_gcd_lcm_001_c(48, 18) == 6;
}
static int pattern_edge_vectors(void) {
  uint32_t l = 9;
  return algorithm_algorithm_pat_alg_gcd_lcm_001_c(0, 0) == 0 && algorithm_algorithm_pat_alg_gcd_lcm_001_c(7, 0) == 7 &&
         algorithm_algorithm_pat_alg_gcd_lcm_001_c_lcm(12, 18, &l) && l == 36 &&
         algorithm_algorithm_pat_alg_gcd_lcm_001_c_lcm(0, 18, &l) && l == 0 &&
         !algorithm_algorithm_pat_alg_gcd_lcm_001_c_lcm(UINT32_MAX, 2, &l);
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
