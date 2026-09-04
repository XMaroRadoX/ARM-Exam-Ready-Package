#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Histogram frequency and mode.
 * Recognition cue: count bounded values choose mode.
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
uint32_t algorithm_algorithm_pat_alg_histogram_mode_001_c(const uint8_t *a, uint32_t n,
                                    uint32_t range, uint32_t *freq) {
  uint32_t i, mode = 0;
  if (!freq || (!a && n) || !range || range > 256u) return 0;
  for (i = 0; i < range; i++)
    freq[i] = 0;
  for (i = 0; i < n; i++)
    if (a[i] < range)
      freq[a[i]]++;
  for (i = 1; i < range; i++)
    if (freq[i] > freq[mode])
      mode = i;
  return mode;
}

