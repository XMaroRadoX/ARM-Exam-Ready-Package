#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Bounded string primitives.
 * Recognition cue: length comparison search bounded copy.
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

uint32_t algorithm_lexicographic_byte_comparison_length(const char *text,
                                                        uint32_t limit);

int32_t algorithm_lexicographic_byte_comparison_compare(const char *first,
                                                        const char *second,
                                                        uint32_t limit);

uint32_t algorithm_lexicographic_byte_comparison_copy(char *destination,
                                                      uint32_t capacity,
                                                      const char *source);

int32_t algorithm_lexicographic_byte_comparison(const char *text, const char *needle,
                                                uint32_t limit);

static int pattern_core_vector(void) {
  return algorithm_lexicographic_byte_comparison("abcabc", "cab", 6) == 2 &&
         algorithm_lexicographic_byte_comparison("abc", "z", 3) == -1;
}
static int pattern_edge_vectors(void) {
  char out[4];
  return algorithm_lexicographic_byte_comparison_length("abc", 2) == 2 &&
         algorithm_lexicographic_byte_comparison_compare("a", "b", 2) < 0 &&
         algorithm_lexicographic_byte_comparison_copy(out, 4, "abcd") == 3 &&
         out[3] == '\0' && algorithm_lexicographic_byte_comparison("", "", 1) == 0 &&
         algorithm_lexicographic_byte_comparison(NULL, "a", 1) == -1;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
