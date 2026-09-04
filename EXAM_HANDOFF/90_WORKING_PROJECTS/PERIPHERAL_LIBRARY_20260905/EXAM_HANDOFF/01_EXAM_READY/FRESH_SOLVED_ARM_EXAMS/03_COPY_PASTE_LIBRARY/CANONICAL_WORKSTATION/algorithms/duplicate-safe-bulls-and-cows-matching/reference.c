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
uint32_t algorithm_duplicate_safe_bulls_and_cows_matching(const uint8_t *secret,
                                                          const uint8_t *guess,
                                                          uint32_t n, uint32_t *cows) {
  uint8_t used_s[32] = {0}, used_g[32] = {0};
  uint32_t i, j, b = 0, c = 0;
  if (!secret || !guess || !cows || n > 32)
    return 0;
  for (i = 0; i < n; i++)
    if (secret[i] == guess[i]) {
      used_s[i] = used_g[i] = 1;
      b++;
    }
  for (i = 0; i < n; i++)
    if (!used_g[i])
      for (j = 0; j < n; j++)
        if (!used_s[j] && guess[i] == secret[j]) {
          used_g[i] = used_s[j] = 1;
          c++;
          break;
        }
  *cows = c;
  return b;
}
