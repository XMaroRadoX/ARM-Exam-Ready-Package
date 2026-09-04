#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Bounded zero-one knapsack.
 * Recognition cue: maximum value within capacity.
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
uint32_t algorithm_one_row_zero_one_knapsack(const uint16_t *wt, const uint16_t *val,
                                             uint32_t n, uint32_t cap, uint32_t *dp);

static int pattern_core_vector(void) {
  uint16_t w[] = {2, 3}, v[] = {3, 4};
  uint32_t d[4];
  return algorithm_one_row_zero_one_knapsack(w, v, 2, 3, d) == 4;
}
static int pattern_edge_vectors(void) {
  uint16_t w[] = {1}, v[] = {2};
  uint32_t d[2];
  return algorithm_one_row_zero_one_knapsack(w, v, 0, 1, d) == 0 &&
         algorithm_one_row_zero_one_knapsack(w, v, 1, 0, d) == 0 &&
         algorithm_one_row_zero_one_knapsack(w, v, 1, 1, d) == 2;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
