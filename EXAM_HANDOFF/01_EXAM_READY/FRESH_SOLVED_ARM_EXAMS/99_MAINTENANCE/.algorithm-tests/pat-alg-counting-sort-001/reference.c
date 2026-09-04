#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Bounded counting sort.
 * Recognition cue: sort keys in known small range.
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
int pat_alg_counting_sort_001(uint8_t *a, uint32_t n, uint32_t range,
                              uint32_t *count) {
  uint32_t i, k = 0;
  if (!a || !count || range > 256)
    return 0;
  for (i = 0; i < range; i++)
    count[i] = 0;
  for (i = 0; i < n; i++) {
    if (a[i] >= range)
      return 0;
    count[a[i]]++;
  }
  for (i = 0; i < range; i++)
    while (count[i] != 0u) {
      --count[i];
      a[k++] = (uint8_t)i;
    }
  return 1;
}

