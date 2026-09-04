#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Consume-once duplicate-safe matching.
 * Recognition cue: Bulls and Cows Mastermind duplicate-safe match.
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
uint32_t algorithm_algorithm_pat_alg_consume_once_match_001_assembly(const uint8_t *secret,
                                        const uint8_t *guess, uint32_t n,
                                        uint32_t *cows);



static int pattern_core_vector(void) {
  uint8_t s[] = {1, 1, 2, 3}, g[] = {1, 2, 1, 4};
  uint32_t c = 0;
  return algorithm_algorithm_pat_alg_consume_once_match_001_assembly(s, g, 4, &c) == 1 && c == 2;
}
static int pattern_edge_vectors(void) {
  uint8_t a[] = {1}, b[] = {2};
  uint32_t c = 9;
  return algorithm_algorithm_pat_alg_consume_once_match_001_assembly(a, b, 0, &c) == 0 && c == 0 &&
         algorithm_algorithm_pat_alg_consume_once_match_001_assembly(a, b, 1, &c) == 0 && c == 0 &&
         algorithm_algorithm_pat_alg_consume_once_match_001_assembly(a, b, 33, &c) == 0;
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
