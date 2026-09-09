#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Selection sort.
 * Recognition cue: select minimum and swap.
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
void algorithm_selection_sort(int32_t *a, uint32_t n) {
  uint32_t i, j, m;
  if (!a)
    return;
  if (!a)
    return;
  for (i = 0; i < n; i++) {
    m = i;
    for (j = i + 1; j < n; j++)
      if (a[j] < a[m])
        m = j;
    if (m != i) {
      int32_t t = a[i];
      a[i] = a[m];
      a[m] = t;
    }
  }
}
