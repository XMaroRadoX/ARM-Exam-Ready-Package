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
uint32_t algorithm_algorithm_pat_alg_lis_001_c(const int32_t *a, uint32_t n, uint32_t *dp) {
  uint32_t i, j, best = 0;
  if ((!a || !dp) && n) return 0;
  for (i = 0; i < n; i++) {
    dp[i] = 1;
    for (j = 0; j < i; j++)
      if (a[j] < a[i] && dp[j] + 1 > dp[i])
        dp[i] = dp[j] + 1;
    if (dp[i] > best)
      best = dp[i];
  }
  return best;
}

