#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Overlap-safe memory movement.
 * Recognition cue: copy forwards or backwards when ranges overlap.
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
void *pat_alg_memmove_001(void *d, const void *s, uint32_t n) {
  uint8_t *o = d;
  const uint8_t *i = s;
  if (!d || !s) return d;
  if ((uintptr_t)o < (uintptr_t)i) {
    uint32_t k;
    for (k = 0; k < n; k++)
      o[k] = i[k];
  } else if ((uintptr_t)o > (uintptr_t)i) {
    while (n) {
      n--;
      o[n] = i[n];
    }
  }
  return d;
}

