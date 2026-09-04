#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Bounded look-and-say generation.
 * Recognition cue: emit count value pairs with output capacity.
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
uint32_t algorithm_bounded_look_and_say_generation_focused_method(const uint8_t *in,
                                                                  uint32_t n,
                                                                  uint8_t *out,
                                                                  uint32_t cap);

static int pattern_core_vector(void) {
  uint8_t a[] = {1, 1, 2}, o[6] = {0};
  return algorithm_bounded_look_and_say_generation_focused_method(a, 3, o, 6) == 4 &&
         o[0] == 2 && o[1] == 1 && o[2] == 1 && o[3] == 2;
}
static int pattern_edge_vectors(void) {
  uint8_t a[] = {7}, o[2];
  return algorithm_bounded_look_and_say_generation_focused_method(a, 0, o, 2) == 0 &&
         algorithm_bounded_look_and_say_generation_focused_method(a, 1, o, 2) == 2 &&
         o[0] == 1 && o[1] == 7 &&
         algorithm_bounded_look_and_say_generation_focused_method(a, 1, o, 1) == 0;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
