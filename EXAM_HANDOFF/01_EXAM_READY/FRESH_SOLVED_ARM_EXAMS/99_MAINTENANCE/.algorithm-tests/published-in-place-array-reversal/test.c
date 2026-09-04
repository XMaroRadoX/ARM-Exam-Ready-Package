#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: In-place array reversal.
 * Recognition cue: reverse array in place.
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
void algorithm_in_place_array_reversal(int32_t *a, uint32_t n);

static int pattern_core_vector(void) {
  int32_t a[] = {1, 2, 3};
  algorithm_in_place_array_reversal(a, 3);
  return a[0] == 3 && a[1] == 2 && a[2] == 1;
}
static int pattern_edge_vectors(void) {
  int32_t a[] = {9};
  algorithm_in_place_array_reversal(a, 0);
  algorithm_in_place_array_reversal(a, 1);
  return a[0] == 9;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
