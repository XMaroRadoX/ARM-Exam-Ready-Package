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
                                                     uint32_t third) {
  uint32_t minimum = (first < second) ? first : second;
  return (third < minimum) ? third : minimum;
}

uint32_t algorithm_two_row_edit_distance(const char *first, const char *second,
                                         uint32_t first_length, uint32_t second_length,
                                         uint32_t *previous, uint32_t *current) {
  uint32_t row;
  uint32_t column;

  if ((first == NULL) || (second == NULL) || (previous == NULL) || (current == NULL) ||
      (current == previous) || first_length == UINT32_MAX ||
      second_length >= UINT32_MAX / 4u) {
    return UINT32_MAX;
  }
  for (column = 0u; column <= second_length; ++column) {
    previous[column] = column;
  }
  for (row = 1u; row <= first_length; ++row) {
    current[0] = row;
    for (column = 1u; column <= second_length; ++column) {
      uint32_t deletion = previous[column] + 1u;
      uint32_t insertion = current[column - 1u] + 1u;
      uint32_t substitution =
          previous[column - 1u] + (first[row - 1u] != second[column - 1u]);
      current[column] =
          algorithm_two_row_edit_distance_min3(deletion, insertion, substitution);
    }
    for (column = 0u; column <= second_length; ++column) {
      previous[column] = current[column];
    }
  }
  return previous[second_length];
}

uint32_t algorithm_two_row_edit_distance_full(const char *first, const char *second,
                                              uint32_t first_length,
                                              uint32_t second_length, uint32_t *table,
                                              uint32_t table_elements) {
  uint32_t row;
  uint32_t column;
  uint32_t columns = second_length + 1u;

  if ((first == NULL) || (second == NULL) || (table == NULL) || (columns == 0u) ||
      first_length == UINT32_MAX || (first_length + 1u > UINT32_MAX / 4u / columns) ||
      (table_elements < (first_length + 1u) * columns)) {
    return UINT32_MAX;
  }
  for (row = 0u; row <= first_length; ++row) {
    table[row * columns] = row;
  }
  for (column = 0u; column <= second_length; ++column) {
    table[column] = column;
  }
  for (row = 1u; row <= first_length; ++row) {
    for (column = 1u; column <= second_length; ++column) {
      uint32_t deletion = table[(row - 1u) * columns + column] + 1u;
      uint32_t insertion = table[row * columns + column - 1u] + 1u;
      uint32_t substitution = table[(row - 1u) * columns + column - 1u] +
                              (first[row - 1u] != second[column - 1u]);
      table[row * columns + column] =
          algorithm_two_row_edit_distance_min3(deletion, insertion, substitution);
    }
  }
  return table[first_length * columns + second_length];
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>


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

int main(void){return test_main();}
