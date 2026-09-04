#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Exponentiation by squaring.
 * Recognition cue: fast power modular exponentiation.
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

uint32_t algorithm_exponentiation_by_squaring(uint32_t base, uint32_t exponent,
                                              uint32_t modulus) {
  uint64_t result = 1u;
  uint64_t factor = base;

  if (modulus != 0u) {
    result %= modulus;
    factor %= modulus;
  }
  while (exponent != 0u) {
    if ((exponent & 1u) != 0u) {
      result =
          (modulus != 0u) ? (result * factor) % modulus : (uint32_t)(result * factor);
    }
    factor =
        (modulus != 0u) ? (factor * factor) % modulus : (uint32_t)(factor * factor);
    exponent >>= 1u;
  }
  return (uint32_t)result;
}

int algorithm_exponentiation_by_squaring_checked(uint32_t base, uint32_t exponent,
                                                 uint32_t *result) {
  uint32_t accumulated = 1u;

  if (result == NULL) {
    return 0;
  }
  while (exponent != 0u) {
    if ((exponent & 1u) != 0u) {
      if ((base != 0u) && (accumulated > UINT32_MAX / base)) {
        return 0;
      }
      accumulated *= base;
    }
    exponent >>= 1u;
    if (exponent != 0u) {
      if ((base != 0u) && (base > UINT32_MAX / base)) {
        return 0;
      }
      base *= base;
    }
  }
  *result = accumulated;
  return 1;
}
