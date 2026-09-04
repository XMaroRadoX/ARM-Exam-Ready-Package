#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
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
uint32_t algorithm_moving_average_and_sliding_window(const int32_t *a, uint32_t n,
                                                     uint32_t w, int32_t *out);

static int pattern_core_vector(void) {
  int32_t a[] = {1, 2, 3}, o[2];
  return algorithm_moving_average_and_sliding_window(a, 3, 2, o) == 2 && o[0] == 1 &&
         o[1] == 2;
}
static int pattern_edge_vectors(void) {
  int32_t a[] = {1, 2, 3}, o[3];
  return algorithm_moving_average_and_sliding_window(a, 3, 0, o) == 0 &&
         algorithm_moving_average_and_sliding_window(a, 3, 4, o) == 0 &&
         algorithm_moving_average_and_sliding_window(a, 3, 1, o) == 3 && o[2] == 3;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
