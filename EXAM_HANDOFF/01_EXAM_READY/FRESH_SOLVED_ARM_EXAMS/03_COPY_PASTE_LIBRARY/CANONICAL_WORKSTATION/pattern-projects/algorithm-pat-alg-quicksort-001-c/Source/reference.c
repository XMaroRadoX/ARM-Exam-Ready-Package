#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Partition-based quicksort.
 * Recognition cue: partition around pivot and recurse bounded.
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
void qs(int32_t *a, int32_t l, int32_t r) {
  int32_t i = l, j = r, p = a[l + (r - l) / 2];
  while (i <= j) {
    while (a[i] < p)
      i++;
    while (a[j] > p)
      j--;
    if (i <= j) {
      int32_t t = a[i];
      a[i++] = a[j];
      a[j--] = t;
    }
  }
  if (l < j)
    qs(a, l, j);
  if (i < r)
    qs(a, i, r);
}
void algorithm_algorithm_pat_alg_quicksort_001_c(int32_t *a, uint32_t n) {
  if (a && n && n <= INT32_MAX)
    qs(a, 0, (int32_t)n - 1);
}

