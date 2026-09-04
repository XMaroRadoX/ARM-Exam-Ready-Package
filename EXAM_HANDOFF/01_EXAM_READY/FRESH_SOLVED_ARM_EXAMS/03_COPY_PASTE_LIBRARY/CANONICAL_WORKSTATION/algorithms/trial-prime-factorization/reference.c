#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Prime testing and trial factorization.
 * Recognition cue: test prime using divisors through square root.
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

int algorithm_trial_prime_factorization(uint32_t value) {
  uint32_t divisor;

  if (value < 2u) {
    return 0;
  }
  if ((value & 1u) == 0u) {
    return value == 2u;
  }
  for (divisor = 3u; divisor <= value / divisor; divisor += 2u) {
    if ((value % divisor) == 0u) {
      return 0;
    }
  }
  return 1;
}

uint32_t algorithm_trial_prime_factorization_factorize(uint32_t value,
                                                       uint32_t *factors,
                                                       uint32_t capacity) {
  uint32_t divisor = 2u;
  uint32_t count = 0u;

  if ((factors == NULL) && (capacity != 0u)) {
    return 0u;
  }
  while ((value > 1u) && (divisor <= value / divisor)) {
    while ((value % divisor) == 0u) {
      if (count < capacity) {
        factors[count] = divisor;
      }
      ++count;
      value /= divisor;
    }
    divisor = (divisor == 2u) ? 3u : divisor + 2u;
  }
  if (value > 1u) {
    if (count < capacity) {
      factors[count] = value;
    }
    ++count;
  }
  return count;
}
