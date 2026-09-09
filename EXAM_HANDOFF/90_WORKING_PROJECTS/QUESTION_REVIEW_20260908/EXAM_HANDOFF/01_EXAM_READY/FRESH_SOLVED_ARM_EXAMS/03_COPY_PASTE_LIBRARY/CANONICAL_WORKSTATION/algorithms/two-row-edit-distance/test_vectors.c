#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Edit distance.
 * Recognition cue: insert delete substitute dynamic programming.
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

static uint32_t algorithm_two_row_edit_distance_min3(uint32_t first, uint32_t second,
                                                     uint32_t third);

uint32_t algorithm_two_row_edit_distance(const char *first, const char *second,
                                         uint32_t first_length, uint32_t second_length,
                                         uint32_t *previous, uint32_t *current);

uint32_t algorithm_two_row_edit_distance_full(const char *first, const char *second,
                                              uint32_t first_length,
                                              uint32_t second_length, uint32_t *table,
                                              uint32_t table_elements);

static int pattern_core_vector(void) {
  uint32_t p[8], c[8];
  return algorithm_two_row_edit_distance("kitten", "sitting", 6, 7, p, c) == 3;
}
static int pattern_edge_vectors(void) {
  uint32_t p[4], c[4], t[16];
  return algorithm_two_row_edit_distance("", "abc", 0, 3, p, c) == 3 &&
         algorithm_two_row_edit_distance("abc", "", 3, 0, p, c) == 3 &&
         algorithm_two_row_edit_distance_full("abc", "adc", 3, 3, t, 16) == 1 &&
         algorithm_two_row_edit_distance_full("a", "b", 1, 1, t, 3) == UINT32_MAX;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
