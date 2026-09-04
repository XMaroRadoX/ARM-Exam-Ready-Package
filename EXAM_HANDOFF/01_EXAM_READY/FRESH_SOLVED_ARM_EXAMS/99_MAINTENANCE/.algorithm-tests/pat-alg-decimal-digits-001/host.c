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

uint32_t pat_alg_decimal_digits_001(uint32_t value) {
  uint32_t digit_sum = 0u;
  uint32_t reversed = 0u;

  do {
    uint32_t digit = value % 10u;
    digit_sum += digit;
    reversed = reversed * 10u + digit;
    value /= 10u;
  } while (value != 0u);
  return (digit_sum << 16u) | (reversed & UINT32_C(0xFFFF));
}

uint32_t pat_alg_decimal_digits_001_extract(uint32_t value, uint8_t *digits,
                                            uint32_t capacity) {
  uint32_t count = 0u;

  if ((digits == NULL) || (capacity == 0u)) {
    return 0u;
  }
  do {
    if (count >= capacity) {
      return 0u;
    }
    digits[count++] = (uint8_t)(value % 10u);
    value /= 10u;
  } while (value != 0u);
  return count;
}

uint32_t pat_alg_decimal_digits_001_reconstruct(const uint8_t *digits,
                                                uint32_t count) {
  uint32_t value = 0u;

  while ((digits != NULL) && (count != 0u)) {
    --count;
    value = value * 10u + digits[count];
  }
  return value;
}

int pat_alg_decimal_digits_001_is_palindrome(uint32_t value) {
  uint32_t original=value;
  uint64_t reversed=0;
  do { reversed=reversed*10u+value%10u; value/=10u; } while(value);
  return reversed==original;
}

uint32_t pat_alg_decimal_digits_001_kaprekar_4(uint32_t value) {
  uint8_t digits[4];
  uint32_t ascending;
  uint32_t descending;
  uint32_t outer;
  uint32_t inner;

  for (outer = 0u; outer < 4u; ++outer) {
    digits[outer] = (uint8_t)(value % 10u);
    value /= 10u;
  }
  for (outer = 0u; outer < 4u; ++outer) {
    for (inner = outer + 1u; inner < 4u; ++inner) {
      if (digits[inner] < digits[outer]) {
        uint8_t temporary = digits[outer];
        digits[outer] = digits[inner];
        digits[inner] = temporary;
      }
    }
  }
  ascending = 0u;
  descending = 0u;
  for (outer = 0u; outer < 4u; ++outer) {
    ascending = ascending * 10u + digits[outer];
    descending = descending * 10u + digits[3u - outer];
  }
  return descending - ascending;
}


#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>


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

uint32_t pat_alg_decimal_digits_001(uint32_t value);

uint32_t pat_alg_decimal_digits_001_extract(uint32_t value, uint8_t *digits,
                                            uint32_t capacity);

uint32_t pat_alg_decimal_digits_001_reconstruct(const uint8_t *digits,
                                                uint32_t count);

int pat_alg_decimal_digits_001_is_palindrome(uint32_t value);

uint32_t pat_alg_decimal_digits_001_kaprekar_4(uint32_t value);



static int pattern_core_vector(void) {
  return pat_alg_decimal_digits_001(123) == ((6u << 16) | 321u);
}
static int pattern_edge_vectors(void) {
  if (!pat_alg_decimal_digits_001_is_palindrome(123321u) || !pat_alg_decimal_digits_001_is_palindrome(4000000004u) || pat_alg_decimal_digits_001_is_palindrome(UINT32_MAX)) return 0;
  uint8_t d[10];
  uint32_t n = pat_alg_decimal_digits_001_extract(1203, d, 10);
  return n == 4 && pat_alg_decimal_digits_001_reconstruct(d, n) == 1203 &&
         pat_alg_decimal_digits_001_is_palindrome(1221) &&
         !pat_alg_decimal_digits_001_is_palindrome(123) &&
         pat_alg_decimal_digits_001_kaprekar_4(3524) == 3087;
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
