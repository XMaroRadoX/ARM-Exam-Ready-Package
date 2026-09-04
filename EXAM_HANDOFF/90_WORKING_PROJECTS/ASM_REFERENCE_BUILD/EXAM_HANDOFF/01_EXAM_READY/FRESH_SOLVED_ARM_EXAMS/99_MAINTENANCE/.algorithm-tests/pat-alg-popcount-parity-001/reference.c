#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Population count and parity.
 * Recognition cue: count set bits parity.
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

uint32_t pat_alg_popcount_parity_001(uint32_t value) {
  uint32_t count = 0u;
  while (value != 0u) {
    value &= value - 1u;
    ++count;
  }
  return count;
}

uint32_t pat_alg_popcount_parity_001_parity(uint32_t value) {
  return pat_alg_popcount_parity_001(value) & 1u;
}

