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
uint32_t pat_alg_knapsack_001(const uint16_t *wt, const uint16_t *val,
                              uint32_t n, uint32_t cap, uint32_t *dp) {
  uint32_t i, c;
  if (!dp || ((!wt || !val) && n) || cap >= UINT32_MAX / 4u || n > 65535u) return 0;
  for (c = 0; c <= cap; c++)
    dp[c] = 0;
  for (i = 0; i < n; i++)
    for (c = cap + 1; c > wt[i];) {
      uint32_t x = --c, v = dp[x - wt[i]] + val[i];
      if (v > dp[x])
        dp[x] = v;
    }
  return dp[cap];
}

#ifdef PATTERN_HOST_TEST
static int pattern_core_vector(void) {
  uint16_t w[] = {2, 3}, v[] = {3, 4};
  uint32_t d[4];
  return pat_alg_knapsack_001(w, v, 2, 3, d) == 4;
}
static int pattern_edge_vectors(void) {
  uint16_t w[] = {1}, v[] = {2};
  uint32_t d[2];
  return pat_alg_knapsack_001(w, v, 0, 1, d) == 0 &&
         pat_alg_knapsack_001(w, v, 1, 0, d) == 0 &&
         pat_alg_knapsack_001(w, v, 1, 1, d) == 2;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int main(void) { return pattern_test_suite(); }
#endif
