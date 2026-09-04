#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
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
int algorithm_bounded_counting_sort(uint8_t *a, uint32_t n, uint32_t range,
                                    uint32_t *count);

static int pattern_core_vector(void) {
  uint8_t a[] = {3, 1, 2, 1};
  uint32_t c[4];
  return algorithm_bounded_counting_sort(a, 4, 4, c) && a[0] == 1 && a[1] == 1 &&
         a[2] == 2 && a[3] == 3;
}
static int pattern_edge_vectors(void) {
  uint8_t check_a[3] = {2, 0, 2};
  uint32_t check_c[3];
  if (!algorithm_bounded_counting_sort(check_a, 3, 3, check_c) || check_c[0] ||
      check_c[1] || check_c[2])
    return 0;
  uint8_t a[] = {0, 3};
  uint32_t c[4];
  return algorithm_bounded_counting_sort(a, 0, 4, c) &&
         !algorithm_bounded_counting_sort(a, 2, 3, c) &&
         !algorithm_bounded_counting_sort(NULL, 1, 4, c);
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
