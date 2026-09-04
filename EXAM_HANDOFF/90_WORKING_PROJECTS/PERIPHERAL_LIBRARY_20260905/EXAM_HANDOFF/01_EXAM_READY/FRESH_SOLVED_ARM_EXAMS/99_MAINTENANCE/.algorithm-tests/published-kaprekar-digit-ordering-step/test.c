#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Decimal digit algorithms.
 * Recognition cue: extract reconstruct sum palindrome Kaprekar digits.
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

uint32_t algorithm_kaprekar_digit_ordering_step(uint32_t value);

uint32_t algorithm_kaprekar_digit_ordering_step_extract(uint32_t value, uint8_t *digits,
                                                        uint32_t capacity);

uint32_t algorithm_kaprekar_digit_ordering_step_reconstruct(const uint8_t *digits,
                                                            uint32_t count);

int algorithm_kaprekar_digit_ordering_step_is_palindrome(uint32_t value);

uint32_t algorithm_kaprekar_digit_ordering_step_kaprekar_4(uint32_t value);

static int pattern_core_vector(void) {
  return algorithm_kaprekar_digit_ordering_step(123) == ((6u << 16) | 321u);
}
static int pattern_edge_vectors(void) {
  if (!algorithm_kaprekar_digit_ordering_step_is_palindrome(123321u) ||
      !algorithm_kaprekar_digit_ordering_step_is_palindrome(4000000004u) ||
      algorithm_kaprekar_digit_ordering_step_is_palindrome(UINT32_MAX))
    return 0;
  uint8_t d[10];
  uint32_t n = algorithm_kaprekar_digit_ordering_step_extract(1203, d, 10);
  return n == 4 && algorithm_kaprekar_digit_ordering_step_reconstruct(d, n) == 1203 &&
         algorithm_kaprekar_digit_ordering_step_is_palindrome(1221) &&
         !algorithm_kaprekar_digit_ordering_step_is_palindrome(123) &&
         algorithm_kaprekar_digit_ordering_step_kaprekar_4(3524) == 3087;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
