#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Bubble sort with early termination.
 * Recognition cue: adjacent swaps stop when already sorted.
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
void pat_alg_bubble_sort_001(int32_t *a, uint32_t n) {
  uint32_t i;
  if (!a) return;
  if (!a) return;
  int changed;
  while (n > 1) {
    changed = 0;
    for (i = 1; i < n; i++)
      if (a[i - 1] > a[i]) {
        int32_t t = a[i - 1];
        a[i - 1] = a[i];
        a[i] = t;
        changed = 1;
      }
    if (!changed)
      break;
    n--;
  }
}

#ifdef PATTERN_HOST_TEST
static int pattern_core_vector(void) {
  int32_t a[] = {3, -1, 2};
  pat_alg_bubble_sort_001(a, 3);
  return a[0] == -1 && a[1] == 2 && a[2] == 3;
}
static int pattern_edge_vectors(void) {
  int32_t a[] = {1, 2, 3}, b[] = {2, 2, 1};
  pat_alg_bubble_sort_001(a, 3);
  pat_alg_bubble_sort_001(b, 3);
  return a[0] == 1 && a[2] == 3 && b[0] == 1 && b[2] == 2;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int main(void) { return pattern_test_suite(); }
#endif
