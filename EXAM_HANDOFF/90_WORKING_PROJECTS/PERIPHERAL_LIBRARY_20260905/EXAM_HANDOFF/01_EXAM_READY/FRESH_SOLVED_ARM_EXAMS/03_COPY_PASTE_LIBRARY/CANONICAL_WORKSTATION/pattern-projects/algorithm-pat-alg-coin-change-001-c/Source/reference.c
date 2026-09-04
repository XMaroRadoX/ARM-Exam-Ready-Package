#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Coin change.
 * Recognition cue: minimum coins or number of ways.
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
uint32_t algorithm_algorithm_pat_alg_coin_change_001_c(const uint16_t *coin, uint32_t n,
                                 uint32_t amount, uint32_t *dp) {
  uint32_t i, x;
  if (!dp || (!coin && n) || amount >= UINT32_MAX / 4u) return UINT32_MAX;
  for (x = 0; x <= amount; x++)
    dp[x] = 0xffffffffu;
  dp[0] = 0;
  for (x = 1; x <= amount; x++)
    for (i = 0; i < n; i++)
      if (coin[i] <= x && dp[x - coin[i]] != 0xffffffffu &&
          dp[x - coin[i]] + 1 < dp[x])
        dp[x] = dp[x - coin[i]] + 1;
  return dp[amount];
}

