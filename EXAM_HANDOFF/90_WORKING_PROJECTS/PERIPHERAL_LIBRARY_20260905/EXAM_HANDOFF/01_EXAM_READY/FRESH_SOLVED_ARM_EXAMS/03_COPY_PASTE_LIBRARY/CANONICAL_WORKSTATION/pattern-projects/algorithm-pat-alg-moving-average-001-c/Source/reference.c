#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Moving average and sliding window.
 * Recognition cue: fixed window running sum average.
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
uint32_t algorithm_algorithm_pat_alg_moving_average_001_c(const int32_t *a, uint32_t n, uint32_t w,
                                    int32_t *out) {
  uint32_t i, o = 0;
  int64_t s = 0;
  if (!a || !out || !w || w > n || w > INT32_MAX)
    return 0;
  for (i = 0; i < n; i++) {
    s += a[i];
    if (i >= w)
      s -= a[i - w];
    if (i + 1 >= w)
      out[o++] = (int32_t)(s / (int32_t)w);
  }
  return o;
}

