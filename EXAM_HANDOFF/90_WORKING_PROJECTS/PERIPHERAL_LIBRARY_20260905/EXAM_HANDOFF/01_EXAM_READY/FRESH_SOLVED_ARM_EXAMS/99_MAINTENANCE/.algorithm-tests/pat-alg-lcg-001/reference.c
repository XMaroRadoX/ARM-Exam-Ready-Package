#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Five-argument linear congruential generator.
 * Recognition cue: LCG modulo shifts and unsigned wraparound.
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
uint32_t pat_alg_lcg_001(uint32_t x, uint32_t a, uint32_t c, uint32_t m,
                         uint32_t shift) {
  uint32_t y = a * x + c;
  if (m)
    y %= m;
  return shift < 32u ? (y >> shift) : 0u;
}

