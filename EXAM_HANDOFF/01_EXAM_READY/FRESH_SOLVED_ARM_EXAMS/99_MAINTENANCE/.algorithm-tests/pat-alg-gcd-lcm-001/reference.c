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

uint32_t pat_alg_gcd_lcm_001(uint32_t first, uint32_t second) {
  while (second != 0u) {
    uint32_t remainder = first % second;
    first = second;
    second = remainder;
  }
  return first;
}

int pat_alg_gcd_lcm_001_lcm(uint32_t first, uint32_t second, uint32_t *result) {
  uint32_t divisor;
  uint32_t reduced_first;

  if (result == NULL) {
    return 0;
  }
  if ((first == 0u) || (second == 0u)) {
    *result = 0u;
    return 1;
  }
  divisor = pat_alg_gcd_lcm_001(first, second);
  reduced_first = first / divisor;
  if (reduced_first > UINT32_MAX / second) {
    return 0;
  }
  *result = reduced_first * second;
  return 1;
}

