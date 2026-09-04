#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Stable merge sort.
 * Recognition cue: stable divide merge with scratch buffer.
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
void merge(int32_t *a, int32_t *t, uint32_t l, uint32_t m, uint32_t r);
void ms(int32_t *a, int32_t *t, uint32_t l, uint32_t r);
void algorithm_stable_merge_sort(int32_t *a, uint32_t n, int32_t *scratch);

static int pattern_core_vector(void) {
  int32_t a[] = {3, -1, 2}, t[3];
  algorithm_stable_merge_sort(a, 3, t);
  return a[0] == -1 && a[1] == 2 && a[2] == 3;
}
static int pattern_edge_vectors(void) {
  int32_t halves[] = {1, 3, 2, 4, 987654}, work[5] = {0, 0, 0, 0, 987654};
  merge(halves, work, 0, 2, 4);
  if (halves[0] != 1 || halves[1] != 2 || halves[2] != 3 || halves[3] != 4 ||
      halves[4] != 987654 || work[4] != 987654)
    return 0;
  int32_t a[] = {2, 2, 1}, t[3];
  algorithm_stable_merge_sort(a, 0, t);
  algorithm_stable_merge_sort(a, 3, t);
  return a[0] == 1 && a[1] == 2 && a[2] == 2;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
